# API_GUIDELINES.md

# MyFinance - API Design Guidelines

## Purpose

This document defines the API standards for the MyFinance platform.

Every API developed in this project must follow these guidelines to ensure consistency, maintainability, scalability, and ease of integration.

---

# API Design Principles

Every API should be:

- RESTful
- Predictable
- Versioned
- Stateless
- Secure
- Well Documented
- Consistent

---

# Base URL

```
/api/v1
```

Future versions

```
/api/v2
```

```
/api/v3
```

Never introduce breaking changes inside the same version.

---

# HTTP Methods

Use the appropriate HTTP method.

| Method | Purpose |
|---------|----------|
| GET | Retrieve data |
| POST | Create new resources |
| PUT | Replace a resource |
| PATCH | Partial update |
| DELETE | Remove a resource |

---

# Endpoint Naming

Use nouns instead of verbs.

Good

```
GET /users

GET /transactions

POST /transactions

GET /goals

POST /reports
```

Avoid

```
/getUsers

/createUser

/updateExpense

/deleteTransaction
```

---

# URL Naming Rules

- Lowercase only
- Hyphen-separated when necessary
- No spaces
- No verbs

Example

```
/financial-goals

/monthly-reports

/expense-analysis
```

---

# Request Format

Use JSON.

Example

```json
{
    "income": 80000,
    "expenses": 35000
}
```

---

# Response Format

All successful responses should follow a consistent structure.

Example

```json
{
    "success": true,
    "message": "Operation completed successfully.",
    "data": {}
}
```

---

# Error Response Format

All errors should follow the same structure.

Example

```json
{
    "success": false,
    "message": "Validation failed.",
    "error": {
        "code": "INVALID_INPUT",
        "details": "Monthly income must be greater than zero."
    }
}
```

---

# HTTP Status Codes

Use standard HTTP status codes.

| Code | Meaning |
|------|----------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

Avoid returning 200 for failed operations.

---

# Request Validation

Use Pydantic models for all request validation.

Validate:

- Required fields
- Data types
- Value ranges
- Enum values
- String lengths

Never trust client input.

---

# Response Validation

All API responses should use response models.

Benefits

- Consistency
- Documentation
- Type Safety

---

# Pagination

Large collections must support pagination.

Example

```
GET /transactions?page=1&limit=20
```

Recommended defaults

```
Page Size = 20

Maximum Page Size = 100
```

---

# Filtering

Use query parameters.

Example

```
GET /transactions?category=Food

GET /transactions?year=2026

GET /transactions?month=July
```

---

# Sorting

Example

```
GET /transactions?sort=date

GET /transactions?sort=-amount
```

Ascending

```
sort=amount
```

Descending

```
sort=-amount
```

---

# Authentication

Future authentication should support

- JWT
- OAuth
- Google Login

Authentication middleware should protect private endpoints.

---

# Authorization

Every request should verify:

- User identity
- Resource ownership
- Access permissions

---

# API Versioning

Always version APIs.

Example

```
/api/v1

/api/v2
```

Do not remove previous versions without a migration strategy.

---

# File Upload

Supported formats

- PDF
- CSV
- XLSX
- DOCX

Maximum size should be configurable through environment variables.

---

# Rate Limiting

Future implementation should support

- User-based limits
- IP-based limits

Example

```
100 requests / minute
```

---

# Logging

Log

- Request ID
- Endpoint
- Execution Time
- Response Status

Do not log

- Passwords
- API Keys
- Financial secrets

---

# API Documentation

FastAPI should automatically generate

```
/docs

/redoc
```

Every endpoint must include

- Summary
- Description
- Request model
- Response model
- Status codes
- Example requests

---

# Naming Conventions

Use

```
snake_case
```

for JSON fields.

Example

```json
{
    "monthly_income": 75000,
    "monthly_expenses": 25000
}
```

---

# Idempotency

PUT operations should be idempotent.

POST operations should create new resources.

DELETE operations should safely handle repeated requests.

---

# Performance Guidelines

- Minimize database queries.
- Use pagination.
- Cache expensive responses.
- Compress large responses when appropriate.

---

# Security Guidelines

Always

- Validate input
- Sanitize user data
- Use HTTPS
- Protect sensitive endpoints
- Return generic internal server errors

Never expose

- Stack traces
- Database errors
- Internal implementation details

---

# Future API Modules

The API should support modules such as

- Authentication
- Users
- Transactions
- Budgets
- Goals
- Investments
- Reports
- AI Chat
- Finance IQ
- Notifications
- Document Upload
- RAG Search

Each module should be implemented as an independent router.

---

# Guiding Philosophy

APIs should be

- Easy to understand
- Easy to consume
- Easy to maintain
- Backward compatible
- Consistent across the entire platform

This document is the official API design standard for the MyFinance platform.