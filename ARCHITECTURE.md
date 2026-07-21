# ARCHITECTURE.md

# MyFinance - AI Financial Intelligence Platform

## Overview

MyFinance is an enterprise-grade AI Financial Intelligence Platform designed using modern software engineering principles and modular AI architecture.

The platform is designed to be scalable, maintainable, secure, and extensible. Every component has a single responsibility and can evolve independently.

---

# High-Level Architecture

```text
                           +----------------------+
                           |        User          |
                           +----------+-----------+
                                      |
                                      |
                              HTTP / REST API
                                      |
                                      ▼
                           +----------------------+
                           |      FastAPI API     |
                           +----------+-----------+
                                      |
                         Dependency Injection Layer
                                      |
                                      ▼
                           +----------------------+
                           |   Service Layer      |
                           +----------+-----------+
                                      |
          -------------------------------------------------------
          |            |             |            |             |
          ▼            ▼             ▼            ▼             ▼

 Expense Engine  Investment   Tax Engine   Risk Engine   Goal Engine
                   Engine

          |            |             |            |             |
          -------------------------------------------------------
                                      |
                                      ▼
                           Finance IQ Engine
                                      |
                                      ▼
                        Financial Planner Agent
                                      |
                                      ▼
                            LangGraph Workflow
                                      |
                  ----------------------------------
                  |                                |
                  ▼                                ▼

          RAG Retrieval                  External Tools

                  |                                |
                  ▼                                ▼

                FAISS                     Gemini LLM

                  |
                  ▼

               MySQL

                  |

               Redis Cache
```

---

# Layered Architecture

The platform follows Clean Architecture.

```
Presentation Layer

↓

Application Layer

↓

Business Layer

↓

AI Layer

↓

Data Layer

↓

Infrastructure Layer
```

---

# Presentation Layer

Responsible for:

- API endpoints
- Request validation
- Response serialization
- Authentication
- Authorization

Technology

- FastAPI

No business logic should exist here.

---

# Application Layer

Coordinates requests.

Responsibilities

- Service orchestration
- Dependency Injection
- Workflow execution
- Validation

---

# Business Layer

Contains all financial business logic.

Examples

- Expense Analysis
- Budget Calculation
- Financial Planning
- Investment Logic
- Tax Rules

This layer should remain independent of FastAPI.

---

# AI Layer

Responsible for all AI-related functionality.

Includes

- LangGraph
- Agents
- Prompt Templates
- Tool Calling
- Memory
- Planning
- Reasoning

Future Components

- Planner Agent
- Expense Agent
- Investment Agent
- Tax Agent
- Risk Agent
- Goal Planning Agent
- Finance IQ Agent

---

# RAG Layer

Responsible for knowledge retrieval.

Pipeline

```
PDFs

↓

Chunking

↓

Embeddings

↓

FAISS

↓

Retriever

↓

Gemini

↓

Answer Generation
```

Knowledge Sources

- RBI Reports
- Financial Books
- Tax Documents
- Investment Guides
- User Documents

---

# Data Layer

Responsible for persistent storage.

Database

MySQL

Stores

- Users
- Transactions
- Goals
- Budgets
- Reports
- Investments

---

# Cache Layer

Technology

Redis

Responsibilities

- Session Cache
- API Cache
- LangGraph State
- Frequently Used Data
- Rate Limiting
- Temporary Storage

---

# Vector Database

Technology

FAISS

Stores

- Financial embeddings
- User document embeddings
- Knowledge embeddings

Used for

- Semantic Search
- RAG
- Context Retrieval

---

# AI Agent Architecture

```
                    Planner Agent

                           |

---------------------------------------------------------

Expense     Investment     Tax      Risk      Goal

Agent         Agent        Agent    Agent     Agent

                           |

                    Finance IQ Agent
```

Planner Agent decides which specialized agent should handle the task.

---

# Request Lifecycle

```
User Request

↓

FastAPI

↓

Router

↓

Service

↓

Planner Agent

↓

Required AI Agent

↓

RAG (Optional)

↓

Gemini

↓

Response

↓

User
```

---

# Folder Responsibilities

```
app/

api/
HTTP Endpoints

config/
Application Configuration

database/
Database Connection

repositories/
Database Operations

services/
Business Logic

schemas/
Pydantic Models

models/
Database Models

ai/
AI Components

agents/
Specialized AI Agents

workflows/
LangGraph Workflows

prompts/
Prompt Templates

memory/
AI Memory

rag/
Retrieval-Augmented Generation

utils/
Reusable Utilities

middleware/
FastAPI Middleware

tests/
Unit Tests

docs/
Project Documentation
```

---

# Scalability Principles

Every module should be:

- Independent
- Replaceable
- Testable
- Reusable
- Loosely Coupled

---

# Security Principles

Never expose

- API Keys
- Passwords
- Secrets

Always use

- Environment Variables
- Input Validation
- Error Handling

---

# Error Handling Strategy

Every layer should

- Validate Input
- Raise Meaningful Exceptions
- Log Errors
- Return Standardized Responses

---

# Logging Strategy

Log

- Application Startup
- Requests
- Errors
- Exceptions
- AI Calls
- Database Events

Avoid logging sensitive user information.

---

# Future Expansion

The architecture should support future integration of:

- Multi-LLM Support
- MCP Servers
- Bank APIs
- OCR
- Voice Assistant
- Financial Forecasting
- Mobile Applications
- Notification Services
- WebSockets
- Real-Time Dashboards

No major architectural changes should be required to add these features.

---

# Guiding Principles

- Build one module at a time.
- Keep every module independent.
- Prefer composition over inheritance.
- Write readable code.
- Prioritize maintainability.
- Avoid unnecessary complexity.
- Design for long-term scalability.

---

# Current Architecture Status

Current Phase

✅ Project Foundation

Next Step

Backend Foundation using FastAPI.

The architecture defined in this document should be treated as the project's technical blueprint. All future development should remain consistent with this design.