---
name: testing-full-pyramid
description: This skill should be used when the user asks to "write unit tests", "add integration tests", "set up E2E testing", "configure Playwright", "configure Cypress", "mock API calls", "fix flaky tests", "improve test coverage", or discusses "test strategy", "Vitest", "Jest", "testing pyramid", "TDD", "test fixtures", "MSW", "page objects", or "CI test pipeline". Unifies unit testing, integration testing, and E2E automation patterns into a single testing strategy reference.
version: 1.0.0
---

# Testing Mastery

## Purpose

Unified testing strategy covering the full test pyramid: unit tests (Vitest/Jest), integration tests, and E2E automation (Playwright/Cypress). Eliminates duplication between testing-patterns and e2e-testing-patterns sources.

## When to Use

Auto-activates when:
- Writing unit or integration tests
- Setting up E2E test suites
- Designing mock/stub strategies
- Debugging flaky tests
- Configuring CI test pipelines
- Deciding what to test at each level

## Test Pyramid Strategy

```
    ╱╲
   ╱E2E╲         ← Few: critical user journeys
  ╱─────╲
 ╱Integration╲   ← Some: API/DB interactions
╱─────────────╲
╱  Unit Tests   ╲  ← Many: business logic, utils
╱─────────────────╲
```

### 1. Unit Tests (Vitest/Jest)

```typescript
import { describe, it, expect, vi } from 'vitest'
import { calculateDiscount } from './pricing'

describe('calculateDiscount', () => {
  it('applies 10% discount for orders over $100', () => {
    expect(calculateDiscount(150)).toBe(15)
  })

  it('returns 0 for orders under $100', () => {
    expect(calculateDiscount(50)).toBe(0)
  })

  it('throws on negative amounts', () => {
    expect(() => calculateDiscount(-1)).toThrow('Invalid amount')
  })
})
```

### 2. Integration Tests

```typescript
import { describe, it, expect, beforeAll } from 'vitest'
import { createUser, getUserById } from './user-service'
import { db } from './test-setup'

describe('UserService Integration', () => {
  beforeAll(async () => {
    await db.migrate()
  })

  it('persists and retrieves user', async () => {
    const user = await createUser({ name: 'Alice', email: 'alice@test.com' })
    const found = await getUserById(user.id)
    expect(found?.name).toBe('Alice')
  })
})
```

### 3. E2E Tests (Playwright)

```typescript
import { test, expect } from '@playwright/test'

test('user completes checkout flow', async ({ page }) => {
  await page.goto('/products')
  await page.click('[data-testid="add-to-cart"]')
  await page.click('[data-testid="checkout"]')
  await page.fill('[name="email"]', 'user@test.com')
  await page.click('[data-testid="submit-order"]')
  await expect(page.locator('[data-testid="order-confirmation"]'))
    .toBeVisible()
})
```

## Core Principles

- **FIRST**: Fast, Isolated, Repeatable, Self-validating, Timely
- **Mock Boundaries**: mock at I/O boundaries (HTTP, DB, filesystem), not internals
- **Test Behavior, Not Implementation**: test what, not how
- **Flakiness**: prefer `toBeVisible()` over `toBeInTheDocument()`, use retry-ability
- **Coverage**: critical paths > coverage %; 100% is a trap

### Resource Files
- [E2E Testing Patterns](resources/e2e-patterns.md) — Playwright advanced, Cypress, visual testing, CI integration
- [Mocking Strategies](resources/mocking-strategies.md) — MSW, vi.mock, test fixtures, factories
