from dotenv import load_dotenv
import os 
from functools import partial
import operator
from typing import Annotated, Sequence, TypedDict, Literal
from langchain_tavily import TavilySearch
from langchain_experimental.tools import PythonREPLTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, BaseMessage
from pydantic import BaseModel
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import create_react_agent

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY environment variable is not set.")

# Define RouteResponse for customer service supervisor
class RouteResponseCS(BaseModel):
    next: Literal["Query_Agent", "Resolution_Agent", "Escalation_Agent", "FINISH"]

# Setup for Customer Service Supervisor
members_cs = ["Query_Agent", "Resolution_Agent", "Escalation_Agent"]
system_prompt_cs = f"You are a customer service supervisor managing agents: {', '.join(members_cs)}. "
system_prompt_cs += "Route the customer query to the appropriate agent based on the query type."

#create prompt template for the supervisor with correctly formatted options
prompt_cs = ChatPromptTemplate.from_messages([
    ("system", system_prompt_cs),
    MessagesPlaceholder(variable_name="messages"),
    ("system", "Choose the next agent to act from {options}."),
]).partial(options=str(members_cs))

# Define LLM and Supervisor function
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

def supervisor_agent_cs(state):
    supervisor_chain_cs = prompt_cs | llm.with_structured_output(RouteResponseCS)
    return supervisor_chain_cs.invoke(state)

# Agent node function to handle message flow to each agent
def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name=name)]
    }

# Define agents for Customer Service tasks with realistic tools
query_agent = create_react_agent(llm, tools=[TavilySearch(api_key=TAVILY_API_KEY, max_results=5)])
resolution_agent = create_react_agent(llm, tools=[PythonREPLTool()])
escalation_agent = create_react_agent(llm, tools=[PythonREPLTool()])

# Create nodes for each agent with valid names
query_node = partial(agent_node, agent=query_agent, name="Query_Agent")
resolution_node = partial(agent_node, agent=resolution_agent, name="Resolution_Agent")
escalation_node = partial(agent_node, agent=escalation_agent, name="Escalation_Agent")

# Define Customer Service graph state and workflow
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

# Initialize StateGraph and add nodes
workflow_cs = StateGraph(AgentState)
workflow_cs.add_node("Query_Agent", query_node)
workflow_cs.add_node("Resolution_Agent", resolution_node)
workflow_cs.add_node("Escalation_Agent", escalation_node)
workflow_cs.add_node("Supervisor", supervisor_agent_cs)

# Define edges for agents to return to the supervisor
for member in members_cs:
    workflow_cs.add_edge(member, "Supervisor")

# Define conditional map for routing
conditional_map_cs = {k:k for k in members_cs}
conditional_map_cs["FINISH"] = END
workflow_cs.add_conditional_edges("Supervisor", lambda x:x["next"], conditional_map_cs)
workflow_cs.add_edge(START, "Supervisor")

# Compile and test the graph
graph_cs = workflow_cs.compile()

#Example input for testing 
inputs_cs = {"messages": [HumanMessage(content="Help me reset my password.")]}

for output in graph_cs.stream(inputs_cs):
    if "__end__" not in output:
        print(output)
