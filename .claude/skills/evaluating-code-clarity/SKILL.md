---
name: evaluating-code-clarity
description: This skill should be used when the user asks to "review code", "improve naming", "refactor functions", "check code quality", "apply TypeScript type patterns", or discusses "code structure", "clean code", or "naming conventions". Complements native `review` and `security-review` skills by adding naming convention heuristics, function design principles, code structure best practices, and advanced TypeScript type patterns.
version: 1.0.0
---

# Code Quality Review

## Purpose

Enhance Claude Code's native review capability with structured code quality heuristics: naming, function design, code structure, and TypeScript type mastery. Acts as an additional lens on top of `review` and `security-review`.

## When to Use

Auto-activates when:
- Reviewing pull requests or code changes
- Designing new functions or APIs
- Refactoring existing code
- Writing complex TypeScript types
- Discussing code architecture or naming

## Quick Reference

### Naming Conventions

- **Boolean**: prefix with `is`/`has`/`should`/`can` (`isLoading`, `hasPermission`)
- **Functions**: verb + noun (`getUserById`, `sendNotification`)
- **Variables**: nouns reflecting content (`userList`, `errorMessage`)
- **Classes/PascalCase**: `UserRepository`, `AuthService`
- **Avoid**: abbreviations (`usr` → `user`), Hungarian notation, single-letter (except loop indices)

### Function Design

- **Single Responsibility**: One function, one job. Max 20 lines. Extract if exceeding.
- **Pure Functions**: Prefer pure → impure. Isolate I/O and side effects at boundaries.
- **Parameters**: Max 3 params. Use options object for more.
- **Return Types**: Always explicit. Never return `any`.
- **Early Return**: Guard clauses over nested ifs.

```typescript
// Good
function processOrder(
  order: Order,
  payment: Payment,
): Result<OrderConfirmation, OrderError> {
  if (!isValidOrder(order)) return fail(OrderError.Invalid);
  if (!isPaymentAuthorized(payment)) return fail(OrderError.PaymentFailed);
  // ... main logic
}

// Bad
function process(data: any, cb: any) {
  // ...
}
```

### TypeScript Type Mastery

- **Discriminated Unions** over optional fields for state machines
- **`satisfies`** over type assertions for validation
- **`as const`** for literal types and enum alternatives
- **Generic constraints** with `extends` for type-safe abstractions
- **Template literal types** for string manipulation at type level

```typescript
// Discriminated union > optional fields
type Result<T, E> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: E };

// satisfies > as
const Colors = {
  primary: '#0070f3',
  secondary: '#ff0080',
} as const satisfies Record<string, `#${string}`>;
```

### Code Structure

- **Layered Architecture**: routes → controllers → services → repositories
- **Dependency Injection**: pass dependencies explicitly, no global singletons
- **Error Handling**: Result types or custom errors, not bare throws
- **Constants**: extract magic numbers/strings, group by domain
- **Imports**: group (external → internal → relative), sort alphabetically

### Resource Files

- [TypeScript Advanced Patterns](resources/typescript-advanced.md) — mapped types, conditional types, template literals, branded types
- [Anti-Patterns Catalog](resources/anti-patterns.md) — common code smells and their fixes

## Related Native Skills

- Use **`review`** for PR-level analysis, then apply this skill's heuristics
- Use **`security-review`** for security concerns, this skill for quality concerns
- These three skills together cover: security + quality + process
