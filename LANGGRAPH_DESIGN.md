# LANGGRAPH_DESIGN.md

# MyFinance - LangGraph Workflow Design

## Purpose

This document defines the workflow architecture of the MyFinance AI platform using LangGraph.

LangGraph is responsible for orchestrating multiple AI agents, maintaining workflow state, handling conditional routing, and coordinating intelligent decision-making across the platform.

The objective is to build a scalable and modular Multi-Agent AI system.

---

# Design Principles

Every workflow should be:

- Modular
- Reusable
- Deterministic
- Fault Tolerant
- Easy to Extend
- Easy to Debug

LangGraph should orchestrate the system, not contain business logic.

---

# High-Level Workflow

```text
                    User Request
                          │
                          ▼
                Input Validation Node
                          │
                          ▼
                  Planner Agent Node
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
 Expense Agent     Investment Agent    Tax Agent
          │               │                │
          └───────────────┼────────────────┘
                          ▼
                 Risk Intelligence Agent
                          ▼
                 Goal Planning Agent
                          ▼
                  Finance IQ Agent
                          ▼
                 Report Generation Agent
                          ▼
                  Response Formatter
                          ▼
                      User Response
```

---

# Workflow Components

## Entry Node

Responsibilities:

- Accept user request
- Validate request
- Initialize workflow state
- Create execution context

---

## Planner Node

Responsibilities:

- Understand user intent
- Decide which agents are required
- Build execution plan
- Route execution

Example

User asks:

> "How can I save ₹10,000 every month?"

Planner activates:

- Expense Agent
- Goal Planning Agent

Investment Agent is skipped.

---

## Expense Agent Node

Responsibilities

- Analyze spending
- Categorize expenses
- Detect unnecessary expenses
- Generate savings recommendations

Output

Structured JSON

---

## Investment Agent Node

Responsibilities

- Portfolio analysis
- Asset allocation
- Risk analysis
- Investment recommendations

---

## Tax Planning Node

Responsibilities

- Tax calculations
- Deduction analysis
- Tax-saving recommendations

---

## Risk Intelligence Node

Responsibilities

- Debt analysis
- Cash flow analysis
- Emergency fund analysis
- Financial risk score

---

## Goal Planning Node

Responsibilities

- Savings roadmap
- Goal feasibility
- Monthly target calculation

---

## Finance IQ Node

Responsibilities

Generate:

- Financial Health Score
- Improvement Suggestions

---

## RAG Retrieval Node

Purpose

Retrieve financial knowledge.

Knowledge Sources

- RBI Reports
- Tax Rules
- Investment Documents
- User Documents

The retrieved context is passed to downstream agents.

---

## Memory Node

Responsibilities

- Load user preferences
- Retrieve previous conversations
- Maintain workflow context

Memory Sources

- Redis
- Long-term memory
- Conversation history

---

## Report Generation Node

Responsibilities

Generate:

- Financial Report
- Investment Report
- Tax Report
- Risk Report
- Finance IQ Report

---

## Output Node

Responsibilities

- Combine agent outputs
- Format response
- Return final answer

---

# LangGraph State

The workflow state should contain:

```python
{
    "user_id": "",
    "query": "",
    "intent": "",
    "financial_profile": {},
    "transactions": [],
    "selected_agents": [],
    "retrieved_documents": [],
    "agent_outputs": {},
    "finance_score": None,
    "final_response": "",
    "errors": []
}
```

State should be immutable where practical.

---

# Conditional Routing

Planner Agent decides execution path.

Examples

Expense Question

```
Planner

↓

Expense Agent

↓

Finance IQ

↓

Response
```

Investment Question

```
Planner

↓

Investment Agent

↓

Risk Agent

↓

Response
```

Tax Question

```
Planner

↓

Tax Agent

↓

Response
```

---

# Parallel Execution

Independent agents should execute in parallel when possible.

Example

```
Planner

↓

Expense Agent

Investment Agent

Risk Agent

↓

Merge Results

↓

Finance IQ
```

Benefits

- Faster response
- Better scalability

---

# Error Handling

Each node should:

- Catch expected exceptions
- Return structured errors
- Preserve workflow state
- Allow recovery when possible

Planner decides whether to retry, skip, or terminate.

---

# Logging

Log:

- Workflow start
- Active nodes
- Routing decisions
- Execution time
- Errors

Avoid logging sensitive user data.

---

# Future Nodes

The architecture supports adding:

- OCR Node
- Voice Node
- Stock Market Node
- Fraud Detection Node
- Notification Node
- Recommendation Node
- Bank API Node

No major redesign should be required.

---

# Best Practices

- Keep nodes focused on one responsibility.
- Avoid direct communication between agents.
- Route all decisions through the Planner.
- Keep workflow definitions declarative.
- Reuse nodes whenever possible.

---

# Current Status

Current Phase

Architecture Planning

Implementation will begin after:

- FastAPI Foundation
- Database Layer
- AI Agent Implementation

This document serves as the official workflow blueprint for all LangGraph orchestration in MyFinance.