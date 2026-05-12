# Langgraph-Ai-Agent-Assignment-Solution
# LangGraph Research Assistant Agent

## Description

This project demonstrates a sophisticated AI agent built using LangGraph.

The agent:
- Searches for information
- Summarizes findings
- Reflects on summary quality
- Retries if the summary is weak
- Saves the final report to a file
- Maintains conversation memory

---

# Features

- Stateful workflow
- Tool calling
- Conditional cyclic routing
- Error recovery loop
- Persistent memory

---

# Installation

```bash
pip install -r requirements.txt
```

---

# Environment Setup

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

# Run the Project

```bash
python main.py
```

---

# Example Prompt

```text
Research the benefits of renewable energy.
```

---

# Workflow

```text
Search → Summarize → Reflect
                    ↓
               Retry Needed?
                 ↙      ↘
              Yes        No
              ↓          ↓
           Search      Save
```

This demonstrates cyclic routing using LangGraph.

---

# Assignment Requirements Covered

| Requirement | Status |
|---|---|
| LangGraph Framework | ✅ |
| At least 3 Tools | ✅ |
| Cyclic Routing | ✅ |
| State & Memory | ✅ |
| Final Synthesized Output | ✅ |
