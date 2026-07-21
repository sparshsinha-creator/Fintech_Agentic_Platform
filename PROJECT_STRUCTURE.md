# PROJECT_STRUCTURE.md

# MyFinance - Project Structure

## Purpose

This document defines the official directory structure for the MyFinance platform.

A consistent project structure improves maintainability, scalability, collaboration, and developer onboarding. Every new module should follow these conventions.

---

# Project Architecture

The project follows a modular, layered architecture.

```
myfinance/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── config/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── database/
│   ├── ai/
│   ├── rag/
│   ├── langgraph/
│   ├── prompts/
│   ├── utils/
│   ├── middleware/
│   ├── exceptions/
│   └── main.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── embeddings/
│   └── uploads/
│
├── docs/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── api/
│   ├── rag/
│   └── ai/
│
├── scripts/
│
├── logs/
│
├── .env.example
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Directory Responsibilities

## app/

Contains all application source code.

---

## api/

Contains FastAPI routers.

Example

```
users.py
transactions.py
goals.py
reports.py
chat.py
```

Routers should only handle:

- Request validation
- Response formatting
- Calling services

Business logic must not be implemented here.

---

## core/

Contains application-wide utilities.

Examples

- Constants
- Enums
- Security helpers
- Shared dependencies

---

## config/

Contains configuration management.

Examples

```
settings.py
logging.py
database.py
```

All configuration should be loaded from environment variables.

---

## models/

Database models.

Example

```
user.py
transaction.py
goal.py
investment.py
```

Each file should define one primary model.

---

## schemas/

Pydantic request and response models.

Examples

```
user_schema.py
transaction_schema.py
goal_schema.py
```

These should be separate from database models.

---

## services/

Contains business logic.

Examples

```
expense_service.py
investment_service.py
tax_service.py
goal_service.py
```

Services should never access HTTP request objects directly.

---

## repositories/

Responsible for database interaction.

Responsibilities

- CRUD operations
- Queries
- Transactions

Repositories should not contain business logic.

---

## database/

Database connection and session management.

Examples

```
connection.py
session.py
base.py
```

---

## ai/

Contains AI-specific logic.

Examples

```
expense_agent.py
planner_agent.py
risk_agent.py
finance_iq.py
```

Each AI agent should have a single responsibility.

---

## rag/

Contains Retrieval-Augmented Generation components.

Examples

```
loader.py
chunker.py
embedder.py
retriever.py
vector_store.py
```

---

## langgraph/

Contains workflow orchestration.

Examples

```
graph.py
nodes.py
state.py
router.py
```

Business logic should remain inside services or AI agents.

---

## prompts/

Stores prompt templates.

Examples

```
planner_prompt.txt
expense_prompt.txt
risk_prompt.txt
```

Prompt files should not contain application logic.

---

## middleware/

Custom middleware.

Examples

- Authentication
- Logging
- Request tracing
- Rate limiting

---

## exceptions/

Centralized exception handling.

Examples

```
custom_exceptions.py
handlers.py
```

---

## utils/

Shared helper functions.

Examples

```
date_utils.py
currency.py
validators.py
```

Utilities should remain generic and reusable.

---

## data/

Stores local datasets and uploaded documents.

Subdirectories

```
raw/
processed/
embeddings/
uploads/
```

Do not commit sensitive data to version control.

---

## docs/

Project documentation.

This directory contains all Markdown documentation files describing architecture, standards, workflows, and development practices.

---

## tests/

Automated tests.

Structure

```
unit/
integration/
api/
rag/
ai/
```

Tests should mirror the application structure where practical.

---

## scripts/

Development and maintenance scripts.

Examples

```
seed_database.py
build_embeddings.py
backup_database.py
```

Scripts should be idempotent whenever possible.

---

## logs/

Application log files.

Logs should be rotated and excluded from version control.

---

# Naming Conventions

Directories

```
snake_case
```

Python Files

```
snake_case.py
```

Classes

```
PascalCase
```

Functions

```
snake_case()
```

Variables

```
snake_case
```

Constants

```
UPPER_CASE
```

---

# Dependency Flow

The dependency direction should always move downward.

```
API

↓

Services

↓

Repositories

↓

Database
```

AI modules may call services but should not directly manipulate database sessions.

---

# Separation of Concerns

Each layer has one responsibility.

| Layer | Responsibility |
|--------|----------------|
| API | HTTP communication |
| Services | Business logic |
| Repositories | Data access |
| Database | Persistence |
| AI | Financial intelligence |
| LangGraph | Workflow orchestration |
| RAG | Knowledge retrieval |

---

# Future Expansion

The structure should support additional modules such as:

- OCR
- Voice Assistant
- Stock Market Integration
- Notification Engine
- Mobile API
- Admin Dashboard

without major restructuring.

---

# Guiding Principles

- Keep modules small and focused.
- One responsibility per file where practical.
- Avoid circular dependencies.
- Prefer composition over duplication.
- Keep AI components independent from API routing.
- Organize code for long-term maintainability.

---

# Current Status

Current Phase

Project Foundation

This document defines the official repository structure for the MyFinance platform and should be followed throughout development.