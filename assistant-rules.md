# 🧠 VSCode Assistant Editing Rules

This file defines the rules that must be followed by any coding assistant or AI agent before editing code in this repository.

---

## ✅ General Behavior

1. **Understand the full context**  
   - Read the entire file and surrounding logic before making any edits.
   - Recognize project-specific conventions, configurations, and architecture.

2. **Avoid assumptions**  
   - Do not guess developer intent. Ask clarifying questions when unsure.

3. **Respect existing code structure**  
   - 🔒 **Do not change the overall file/folder architecture.**
   - 🔒 **Do not move functions, files, or components unless explicitly requested.**

4. **Follow project-specific standards**  
   - Match the existing formatting, naming conventions, and language style.
   - Adhere to linting rules and formatting tools (e.g., Prettier, Black, ESLint, etc.).

---

## ✍️ Editing Rules

1. **Only make improvements**  
   - 🔒 **Do not refactor for stylistic reasons alone.**
   - ✅ Only improve clarity, efficiency, readability, or fix bugs.

2. **Explain every change**  
   - 🗒️ Use clear inline comments like `// edited by assistant: reason here`.
   - If multiple lines are changed, include a block comment summarizing the edit above the section.

3. **Do not introduce dependencies**  
   - 🔒 Never import or add new libraries/packages without explicit permission.

4. **Respect variable/function names**  
   - Preserve existing naming unless renaming clearly improves clarity and is explained.

5. **Never remove developer notes**  
   - 🔒 Keep all `TODO`, `FIXME`, or custom tags unless the task is completed.

6. **Maintain logical flow**  
   - 🔒 Do not rearrange control structures, function order, or logic unless improving functionality and explaining why.

---

## 🔍 Review Checklist (Agent Must Confirm Before Submitting Edits)

- [ ] Have I respected the project’s folder/file structure?
- [ ] Have I avoided unnecessary refactoring or style edits?
- [ ] Is each change clearly explained in comments?
- [ ] Does the code compile or run correctly after changes?
- [ ] Did I edit only the necessary sections?
- [ ] Are all changes traceable and reversible?

---

## 📌 Summary for All AI/Agent-Based Tools

- ✅ Maintain the **codebase structure** exactly as is.
- ✅ Only **improve clarity, efficiency, or correctness** — no stylistic rewrites.
- ✅ **Comment every change** with a reason.
- 🔒 Never restructure files, folders, or logic unless explicitly instructed.
- 🔒 Never add or remove dependencies without permission.

---

