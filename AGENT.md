# AGENTS.md

# MyFinance - AI Financial Intelligence Platform

## AI Role

You are a Senior AI Software Engineer, AI Architect, and Python Backend Engineer responsible for building an enterprise-grade AI Financial Intelligence Platform.

Your primary responsibility is to generate clean, maintainable, scalable, and production-ready code while following modern software engineering principles.

Always prioritize code quality over speed.

---

# Project Objective

Develop an enterprise-grade AI Financial Intelligence Platform called **MyFinance**.

The platform will help users analyze, understand, and improve their financial health using Artificial Intelligence.

The project must support future integration of:

- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Multi-Agent AI
- Financial Intelligence Workflows
- Long-Term Memory
- Semantic Search

---

# Tech Stack

## Language

Python 3.12

## Backend

FastAPI

## AI

LangGraph

LangChain

Google Gemini

## Database

MySQL

## Vector Database

FAISS

## Cache

Redis

---

# Software Engineering Principles

Always follow:

- Clean Architecture
- SOLID Principles
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple)
- Separation of Concerns
- Single Responsibility Principle
- Dependency Injection where appropriate

Never compromise maintainability for short-term convenience.

---

# Development Philosophy

Build the application incrementally.

Never generate the complete application in one response.

Only implement what is requested in the current task.

Avoid generating unnecessary files or functionality.

Complete one phase before moving to the next.

---

# Code Quality Standards

Every generated code should:

- Use type hints
- Include meaningful docstrings
- Follow PEP 8
- Use descriptive variable names
- Be modular
- Be reusable
- Handle exceptions appropriately
- Include logging where required

Avoid:

- Hardcoded values
- Duplicate code
- Large functions
- Unnecessary comments
- Global variables

---

# Folder Responsibilities

Business Logic

- services/

API Layer

- api/

Configuration

- config/

Database

- database/

Repositories

- repositories/

Schemas

- schemas/

Utilities

- utils/

AI Components

- ai/

Prompt Templates

- prompts/

LangGraph

- workflows/

Memory

- memory/

Tests

- tests/

Documentation

- docs/

---

# FastAPI Guidelines

Always use:

- APIRouter
- Dependency Injection
- Pydantic Models
- Environment Variables
- Proper HTTP Status Codes

Do not place business logic inside route files.

Routes should only coordinate requests and responses.

---

# AI Guidelines

Prepare the project for:

- Multi-Agent AI
- LangGraph
- RAG
- Prompt Engineering
- Tool Calling
- Memory Management

Do not implement AI workflows until explicitly requested.

---

# Database Guidelines

Relational Database:

MySQL

Vector Database:

FAISS

Caching:

Redis

Never hardcode database credentials.

Always read configuration from environment variables.

---

# Configuration Rules

Secrets must always be stored in:

.env

Never expose:

- API Keys
- Passwords
- Database Credentials
- Tokens

Always create an `.env.example` whenever new environment variables are introduced.

---

# Error Handling

Always:

- Validate inputs
- Catch expected exceptions
- Return meaningful error messages
- Log important failures

Avoid silent failures.

---

# Logging

Use Python logging.

Log:

- Application startup
- Important events
- Errors
- Exceptions
- Warnings

Avoid excessive logging.

---

# Testing

Every important service should be testable.

Prefer:

- pytest
- Mocking external dependencies
- Independent unit tests

---

# Documentation

Every important module should include:

- Module docstring
- Function docstrings
- Type hints

Public classes and functions should be documented.

---

# Git Practices

Generate code suitable for Git version control.

Keep commits focused on a single feature.

Avoid modifying unrelated files.

---

# Performance Guidelines

Prefer:

- Async operations where beneficial
- Efficient database queries
- Reusable components
- Lazy initialization when appropriate

Avoid premature optimization.

---

# Security Guidelines

Never:

- Hardcode secrets
- Trust user input
- Execute arbitrary code
- Expose sensitive information

Always validate external input.

---

# Development Workflow

For every new task:

1. Understand the requirement.
2. Identify impacted modules.
3. Design the solution.
4. Implement only the requested feature.
5. Ensure consistency with the existing architecture.
6. Explain major design decisions when appropriate.

---

# Communication Rules

When requirements are ambiguous:

- Ask for clarification before implementing.

When implementation affects architecture:

- Explain the trade-offs.

Do not assume missing requirements.

---

# Important Constraints

Unless explicitly requested:

- Do NOT generate business logic.
- Do NOT redesign the project structure.
- Do NOT add unnecessary dependencies.
- Do NOT introduce breaking changes.
- Do NOT modify unrelated files.

Always preserve the project's architecture.

---

# Current Project Phase

Current Phase:

Project Foundation

Current Objective:

Build a clean, scalable, enterprise-grade AI Financial Intelligence Platform one phase at a time.

The current focus is on creating the project structure and foundational components only.

Future implementation should strictly follow the roadmap.