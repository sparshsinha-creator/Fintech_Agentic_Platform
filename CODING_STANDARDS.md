# CODING_STANDARDS.md

# MyFinance - Coding Standards

## Purpose

This document defines the official coding standards for the MyFinance platform.

Every contributor, AI coding assistant, and future developer should follow these standards to maintain consistency, readability, and long-term maintainability.

---

# General Principles

Always write code that is:

- Readable
- Maintainable
- Modular
- Testable
- Scalable
- Well Documented

Code is written for humans first and computers second.

---

# Software Engineering Principles

Always follow:

- Clean Architecture
- SOLID Principles
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple)
- YAGNI (You Aren't Gonna Need It)
- Separation of Concerns
- Composition over Inheritance

---

# Python Version

Python 3.12+

All new language features supported by Python 3.12 may be used when they improve readability.

---

# Naming Conventions

## Variables

Use descriptive snake_case names.

Good

```python
user_profile
monthly_income
financial_score
```

Bad

```python
x
a1
temp
```

---

## Functions

Use snake_case.

Functions should describe actions.

Examples

```python
calculate_budget()
generate_report()
load_transactions()
classify_expenses()
```

---

## Classes

Use PascalCase.

Examples

```python
ExpenseAnalyzer
InvestmentAdvisor
FinancialPlanner
UserService
```

---

## Constants

Use UPPER_CASE.

Examples

```python
MAX_RETRIES
DEFAULT_TIMEOUT
API_VERSION
```

---

## Files

Use lowercase with underscores.

Examples

```text
expense_service.py
investment_agent.py
database_config.py
```

---

## Packages

Lowercase only.

Examples

```text
services
repositories
database
config
```

---

# Function Guidelines

Functions should:

- Have one responsibility.
- Be easy to test.
- Return predictable results.

Prefer functions under 40 lines whenever practical.

Avoid deeply nested logic.

---

# Class Guidelines

Classes should:

- Represent one concept.
- Follow the Single Responsibility Principle.
- Be loosely coupled.
- Use dependency injection where appropriate.

Avoid God Classes.

---

# Type Hints

Always use type hints.

Example

```python
def calculate_score(income: float, expenses: float) -> float:
    ...
```

Avoid untyped public functions.

---

# Docstrings

Every public module, class, and function should have a docstring.

Use Google-style docstrings.

Example

```python
def calculate_budget(income: float, expenses: float) -> float:
    """
    Calculate the remaining monthly budget.

    Args:
        income: Monthly income.
        expenses: Monthly expenses.

    Returns:
        Remaining budget.
    """
```

---

# Imports

Import order:

1. Standard Library
2. Third-Party Libraries
3. Local Imports

Example

```python
import os
from pathlib import Path

from fastapi import FastAPI

from app.services.user_service import UserService
```

Avoid wildcard imports.

Never use:

```python
from module import *
```

---

# Error Handling

Always:

- Validate inputs.
- Raise meaningful exceptions.
- Catch expected errors.
- Log unexpected failures.

Avoid bare `except:` blocks.

Preferred

```python
except ValueError:
    ...
```

Avoid

```python
except:
    ...
```

---

# Logging

Use Python's logging module.

Log:

- Startup events
- Configuration loading
- Errors
- Warnings
- Important business events

Do not log:

- Passwords
- API keys
- Sensitive financial information

---

# Configuration

Never hardcode:

- API Keys
- Secrets
- Passwords
- URLs
- Model names

Always use:

`.env`

---

# Business Logic

Business logic belongs only in:

```text
services/
```

Do not place business logic inside:

- api/
- routers/
- config/
- middleware/

---

# API Design

Routes should:

- Validate requests.
- Call services.
- Return responses.

Routes should not:

- Query databases directly.
- Implement financial calculations.
- Call AI models directly.

---

# Database Rules

Repositories should:

- Handle persistence.
- Not contain business logic.

Services should:

- Call repositories.
- Apply business rules.

---

# AI Development Rules

Prompt templates belong in:

```text
prompts/
```

AI orchestration belongs in:

```text
workflows/
```

Specialized AI logic belongs in:

```text
agents/
```

Never mix AI logic with API routes.

---

# Testing Standards

Every important service should have unit tests.

Preferred framework:

- pytest

Tests should be:

- Independent
- Repeatable
- Fast

---

# Performance Guidelines

Prefer:

- Async operations where beneficial.
- Efficient queries.
- Reusable components.

Avoid premature optimization.

---

# Git Commit Convention

Use meaningful commit messages.

Examples

```text
feat: add expense analysis service

fix: resolve Redis connection issue

docs: update architecture documentation

refactor: simplify investment engine

test: add unit tests for goal planner
```

---

# Code Review Checklist

Before submitting code, verify:

- Follows PEP 8
- Uses type hints
- Has docstrings
- Handles errors
- Includes logging where appropriate
- No duplicated code
- No unused imports
- No commented-out code
- Passes tests

---

# AI Assistant Guidelines

When generating code:

- Follow existing project architecture.
- Avoid unnecessary dependencies.
- Preserve consistency.
- Explain significant design decisions.
- Do not modify unrelated files.
- Ask for clarification when requirements are unclear.

---

# Guiding Philosophy

The project values:

- Simplicity over cleverness.
- Readability over brevity.
- Maintainability over speed.
- Consistency over personal preference.

Every line of code should make the project easier to understand and extend.