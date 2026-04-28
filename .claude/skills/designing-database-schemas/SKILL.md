---
name: designing-database-schemas
description: This skill should be used when the user asks to "design database schema", "create tables", "add indexes", "optimize SQL queries", "model relationships", "plan migrations", or discusses "ERD", "normalization", "denormalization", "PostgreSQL", "MySQL", "SQLite", "Prisma", "Drizzle", "query performance", "EXPLAIN ANALYZE", "index strategy", or "database design patterns". Covers relational database design including table structure, relationship modeling, index optimization, query performance tuning, and safe migration patterns.
version: 1.0.0
---

# Database Designer

## Purpose

Database design guide for optimal schema structure, relationship modeling, and index strategy. Covers normalization trade-offs, query optimization, and migration patterns.

## When to Use

Auto-activates when:
- Designing database schemas or tables
- Modeling entity relationships
- Writing or optimizing SQL queries
- Adding indexes or analyzing query performance
- Planning data migrations
- Discussing normalization strategies

## Core Principles

### 1. Schema Design

- **Normalize until it hurts, denormalize until it works** — start with 3NF, denormalize for read performance only when measured
- **Primary Keys**: UUIDv7 > auto-increment (distributed-friendly, no contention)
- **Foreign Keys**: always enforce at DB level (not just app-level)
- **Timestamps**: `created_at`/`updated_at` on every table, use DB defaults
- **Soft Delete**: `deleted_at TIMESTAMP` for recoverability, unique partial indexes

```sql
CREATE TABLE users (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email      TEXT NOT NULL UNIQUE,
  name       TEXT NOT NULL,
  role       TEXT NOT NULL DEFAULT 'user'
             CHECK (role IN ('admin', 'user', 'viewer')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_users_email_active
  ON users (email)
  WHERE deleted_at IS NULL;
```

### 2. Index Strategy

| Index Type | When to Use | Example |
|---|---|---|
| B-tree | Equality + range queries, default choice | `WHERE status = 'active'` |
| Composite | Multi-column queries, order matters | `WHERE org_id = ? AND status = ?` |
| Partial | Filtered queries on subset | `WHERE deleted_at IS NULL` |
| Covering | Index-only scans for hot queries | Include `INCLUDE (name)` |
| GIN | JSONB / array / full-text search | `WHERE tags @> ['urgent']` |

```sql
-- Composite index: order = equality cols first, then range
CREATE INDEX idx_orders_org_status_date
  ON orders (org_id, status, created_at DESC);

-- Covering index for index-only scan
CREATE INDEX idx_users_email_cover
  ON users (email) INCLUDE (name, role);
```

### 3. Relationship Modeling

- **One-to-Many**: FK on child table
- **Many-to-Many**: junction table with composite PK
- **One-to-One**: FK with UNIQUE constraint, or same PK
- **Polymorphic**: prefer separate join tables over `type` + nullable FK

### 4. Migration Patterns

```sql
-- Safe migration: add column as nullable, backfill, then add NOT NULL
ALTER TABLE users ADD COLUMN timezone TEXT;
UPDATE users SET timezone = 'UTC' WHERE timezone IS NULL;
ALTER TABLE users ALTER COLUMN timezone SET NOT NULL;
```

### Resource Files
- [Query Optimization](resources/query-optimization.md) — EXPLAIN ANALYZE, CTE vs subqueries, pagination strategies, N+1 prevention
- [Migrations Guide](resources/migrations.md) — zero-downtime migrations, rollback strategies, Prisma/Knex patterns
