# Customer Service Automation Agent

A multi-agent customer service automation system built with LangGraph and LangChain that intelligently routes customer inquiries between specialized agents to provide comprehensive support.

## 🎯 What This Agent Does

This system automates customer service interactions by:

1. **Analyzing customer queries** using a supervisor agent
2. **Routing requests** to the most appropriate specialized agent
3. **Providing comprehensive responses** through agent collaboration
4. **Automatically terminating** conversations when issues are resolved

### **Real Example**
```
Input: "Help me reset my password."

Output:
Routing to: Query_Agent
Query_Agent: To reset your password, follow these steps:
1. Go to the website login page
2. Click "Forgot Password"
3. Enter your email address...

Routing to: Resolution_Agent  
Resolution_Agent: I can provide additional technical guidance...

Routing to: FINISH
```

## 🏗️ System Architecture

```
Customer Query → Supervisor Agent → Specialized Agents → Response → FINISH
                      ↑                    ↓
                      ←-------- Feedback -------
```

### **Agent Roles**

#### **Supervisor Agent**
- **Function**: Intelligent query router and conversation manager
- **Technology**: Llama 3.3 70B via GROQ API with structured output
- **Decision Making**: Uses Pydantic models for reliable routing choices

#### **Query_Agent** 🔍
- **Purpose**: Information lookup, research, and general questions
- **Tools**: Tavily Search (real-time web search, max 5 results)
- **Best For**: Current information, "How to" questions, general inquiries

#### **Resolution_Agent** 🛠️
- **Purpose**: Technical problem-solving and step-by-step solutions
- **Tools**: Python REPL for calculations and technical solutions
- **Best For**: Password resets, technical troubleshooting, code generation

#### **Escalation_Agent** 📞
- **Purpose**: Complex issues requiring human intervention
- **Tools**: Python REPL for documentation and escalation procedures
- **Best For**: Account issues, billing problems, complex technical cases

## 🚀 Key Features

- ✅ **Automatic Routing**: Supervisor intelligently directs queries to appropriate agents
- ✅ **Clean Output**: User-friendly display without technical clutter
- ✅ **Smart Termination**: Conversation ends automatically when resolved
- ✅ **Real-time Research**: Live web search via Tavily API
- ✅ **Technical Solutions**: Python-powered problem solving
- ✅ **Infinite Loop Protection**: 10-step recursion limit with clear error handling

## 📋 Prerequisites

- **Python 3.8+**
- **API Keys Required**:
  - `GROQ_API_KEY` - For Llama 3.3 70B language model
  - `TAVILY_API_KEY` - For web search functionality

## 🛠️ Installation & Setup

### **1. Project Setup**
```bash
# Navigate to your project directory
cd customer-service-automation-agent

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### **2. Install Dependencies**
```bash
# Install required packages
pip install langchain-groq langchain-tavily langchain-experimental langgraph python-dotenv pydantic
```

### **3. Environment Configuration**
Create a `.env` file in your project root:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

**Get your API keys:**
- **GROQ API**: [console.groq.com](https://console.groq.com) (Free tier available)
- **Tavily API**: [tavily.com](https://tavily.com) (Free tier: 1000 searches/month)

## 🎯 How to Run the Agent

### **Basic Usage**
```bash
# Ensure virtual environment is active
source venv/bin/activate

# Run the agent with default query
python3 agent.py
```

**Default behavior**: The agent will process "Help me reset my password." and show the complete interaction flow.

### **Customizing Queries**
Edit line 90 in `agent.py`:
```python
# Change this line to test different queries
inputs_cs = {"messages": [HumanMessage(content="Your question here")]}
```

**Example queries to try:**
```python
# Information lookup
inputs_cs = {"messages": [HumanMessage(content="What is the latest news about AI?")]}

# Technical problem
inputs_cs = {"messages": [HumanMessage(content="Generate a secure password for me")]}

# Escalation scenario
inputs_cs = {"messages": [HumanMessage(content="I want to cancel my subscription and get a refund")]}
```

### **Expected Output Format**
```
Routing to: Query_Agent
Query_Agent: [Agent response with helpful information]

Routing to: Resolution_Agent
Resolution_Agent: [Technical solution or additional guidance]

Routing to: FINISH
```

## ⚙️ Configuration Options

### **Modify Recursion Limit**
```python
# In agent.py line 95, adjust the limit
for output in graph_cs.stream(inputs_cs, config={"recursion_limit": 15}):
```

### **Change LLM Model**
```python
# Line 49 - Switch to different GROQ models
llm = ChatGroq(model="mixtral-8x7b-32768", api_key=GROQ_API_KEY)
# Available: "llama-3.1-70b-versatile", "mixtral-8x7b-32768"
```

### **Adjust Search Results**
```python
# Line 60 - Modify Tavily search parameters
query_agent = create_react_agent(llm, tools=[TavilySearch(api_key=TAVILY_API_KEY, max_results=3)])
```

## 🔒 Security & Local Access

### **Agent Access Levels**

| Agent | Internet Access | Python Execution | File System |
|-------|----------------|------------------|------------|
| Supervisor | ❌ | ❌ | ❌ |
| Query_Agent | ✅ (Tavily only) | ❌ | ❌ |
| Resolution_Agent | ❌ | ✅ (Sandboxed) | ❌ |
| Escalation_Agent | ❌ | ✅ (Sandboxed) | ❌ |

### **What the Agent CAN Do**
- Search the web for current information
- Execute Python code for calculations and text processing
- Generate responses and technical solutions
- Process customer service scenarios

### **What the Agent CANNOT Do**
- Access your personal files or system settings
- Install software or modify system configurations
- Execute shell commands or system operations
- Access sensitive information outside the project

## 📁 Project Structure

```
customer-service-automation-agent/
├── agent.py                 # Main application (this is what you run)
├── .env                     # API keys (create this file)
├── venv/                    # Virtual environment
├── README.md               # This documentation
└── assistant-rules.md      # Development guidelines
```

## 🐛 Troubleshooting

### **Common Issues**

#### **1. Missing API Keys**
```
ValueError: GROQ_API_KEY environment variable is not set
```
**Solution**: Create `.env` file with valid API keys

#### **2. Module Not Found**
```
ModuleNotFoundError: No module named 'langchain_tavily'
```
**Solution**: 
```bash
pip install langchain-tavily
# or install all dependencies again
```

#### **3. Recursion Limit Reached**
```
GraphRecursionError: Recursion limit of 10 reached
```
**Solution**: Increase limit in config or improve agent prompts

#### **4. Agent Stuck in Loop**
**Symptoms**: Same agent keeps getting called repeatedly
**Solution**: The supervisor will automatically terminate after 10 steps

### **Debug Mode**
To see full technical output, modify lines 97-108 in `agent.py`:
```python
# Replace the cleaned output section with:
print(f"Full output: {output}")
```

## 🎛️ Advanced Customization

### **Adding New Query Types**
```python
# Test different customer service scenarios
test_queries = [
    "How do I update my billing information?",
    "My account is locked, help me unlock it",
    "I need technical support for your mobile app",
    "Calculate the compound interest on my savings"
]

for query in test_queries:
    inputs_cs = {"messages": [HumanMessage(content=query)]}
    # Run the agent...
```

### **Monitoring Agent Performance**
```python
# Add timing and tracking
import time
start_time = time.time()

for output in graph_cs.stream(inputs_cs, config={"recursion_limit": 10}):
    # Your existing output processing...
    
print(f"Total processing time: {time.time() - start_time:.2f} seconds")
```

## 🔮 How It Works Internally

1. **Query Input**: Customer message enters the system
2. **Supervisor Analysis**: LLM analyzes query and selects appropriate agent
3. **Agent Processing**: Selected agent uses its tools to generate response
4. **Response Evaluation**: Supervisor determines if issue is resolved
5. **Routing Decision**: Either route to another agent or FINISH
6. **Clean Output**: System displays only relevant information to user

## 📊 Performance Notes

- **Average Response Time**: 3-10 seconds depending on query complexity
- **API Costs**: ~$0.001-0.01 per query (varies by model and search usage)
- **Success Rate**: High accuracy for routing and termination decisions

## 🤝 Contributing

When modifying the code:
1. Follow existing code structure and comments
2. Test with various query types
3. Ensure proper error handling
4. Document changes with `# edited by assistant:` comments

## 📄 License

Educational and development use. Comply with GROQ and Tavily API terms of service.

---

**Ready to run**: Just set up your API keys and execute `python3 agent.py`  
**Last Updated**: December 2024  
**Agent Version**: LangGraph-based multi-agent systemewtrs
