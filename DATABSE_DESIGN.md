# DATABASE_DESIGN.md

# MyFinance - Database Design

## Purpose

This document defines the relational database architecture for the MyFinance platform.

The database is designed to be:

- Scalable
- Normalized
- Secure
- Extensible
- Production Ready

The first implementation will use MySQL 8+.

---

# Database Overview

Database Name

```text
myfinance_db
```

Database Engine

```text
MySQL 8+
```

Character Set

```text
utf8mb4
```

Collation

```text
utf8mb4_unicode_ci
```

Storage Engine

```text
InnoDB
```

Timezone

```text
UTC
```

---

# Database Design Principles

Always:

- Normalize data where practical.
- Avoid duplicate information.
- Use foreign keys.
- Create indexes for frequently queried columns.
- Store timestamps in UTC.
- Keep tables focused on a single responsibility.

---

# Entity Relationship Overview

```text
Users
│
├── Financial Profiles
│
├── Transactions
│
├── Budgets
│
├── Financial Goals
│
├── Investments
│
├── AI Conversations
│
├── AI Reports
│
└── Uploaded Documents
```

---

# Core Tables

## Users

Purpose

Stores user account information.

Fields

- id
- full_name
- email
- password_hash
- phone_number
- created_at
- updated_at
- is_active

Primary Key

```text
id
```

Unique Keys

```text
email
```

---

## Financial Profile

Purpose

Stores user financial information.

Fields

- id
- user_id
- monthly_income
- monthly_expenses
- occupation
- city
- country
- risk_profile

Relationship

```text
One User
↓

One Financial Profile
```

---

## Transactions

Purpose

Stores financial transactions.

Fields

- id
- user_id
- category_id
- amount
- transaction_type
- payment_method
- description
- transaction_date
- created_at

Examples

Income

Expense

Transfer

Investment

---

## Categories

Purpose

Expense categorization.

Examples

- Food
- Rent
- Travel
- Entertainment
- Healthcare
- Investment
- Salary

---

## Budgets

Purpose

Monthly budget planning.

Fields

- user_id
- category_id
- monthly_limit
- month
- year

---

## Financial Goals

Purpose

Stores financial goals.

Examples

- Buy House
- Retirement
- Emergency Fund
- Vacation
- Education

Fields

- target_amount
- saved_amount
- deadline
- status

---

## Investments

Purpose

Investment portfolio.

Examples

- Stocks
- Mutual Funds
- Fixed Deposit
- Gold
- Crypto
- Bonds

---

## AI Conversations

Purpose

Stores user conversations with AI.

Fields

- user_id
- question
- response
- created_at

---

## AI Reports

Purpose

Stores generated financial reports.

Examples

- Monthly Report
- Investment Report
- Tax Report
- Risk Report
- Finance IQ Report

---

## Uploaded Documents

Purpose

Stores metadata of uploaded files.

Examples

- Bank Statement
- Salary Slip
- Income Tax Document
- Investment Statement

---

# Relationships

```text
User

↓

Financial Profile

↓

Transactions

↓

Categories

↓

Budgets

↓

Financial Goals

↓

Investments

↓

AI Reports

↓

AI Conversations
```

---

# Indexing Strategy

Create indexes on:

- email
- user_id
- transaction_date
- category_id
- created_at

Composite indexes may be added after performance analysis.

---

# Data Integrity

Use:

- Primary Keys
- Foreign Keys
- NOT NULL
- CHECK Constraints
- UNIQUE Constraints

Avoid orphan records.

---

# Soft Delete Policy

Instead of deleting important records,

prefer:

```text
is_deleted

deleted_at
```

This preserves historical data.

---

# Audit Fields

Every major table should include:

```text
created_at

updated_at
```

Optional

```text
created_by

updated_by
```

---

# Future Tables

The architecture should support future addition of:

- Notifications
- AI Memory
- User Preferences
- Bank Accounts
- Loans
- Insurance
- Tax Records
- Rewards
- Subscriptions
- Financial Forecasts

No redesign should be required.

---

# Repository Pattern

Every table should have a dedicated repository.

Example

```text
UserRepository

TransactionRepository

BudgetRepository

InvestmentRepository

GoalRepository
```

Repositories should contain only database operations.

Business logic belongs in services.

---

# Transactions

Use database transactions for:

- Money transfer
- Investment updates
- Goal updates
- Budget updates

Never leave the database in an inconsistent state.

---

# Performance Guidelines

Prefer:

- Indexed lookups
- Pagination
- Batch inserts
- Prepared statements

Avoid:

- SELECT *
- Unnecessary joins
- Repeated queries inside loops

---

# Security Guidelines

Never store:

- Plain text passwords
- API Keys
- Financial secrets

Passwords should always be hashed.

Sensitive fields should be encrypted where appropriate.

---

# Backup Strategy

Future production deployment should support:

- Daily backups
- Point-in-time recovery
- Disaster recovery
- Replication

---

# Current Database Status

Current Phase

Planning

Implementation will begin during the Database Layer phase of the project roadmap.

Until then, this document serves as the official database blueprint.