---
name: constitutional-audit
description: Audit recent code changes against Karpathy's 4 constitutional principles. Checks for unnecessary complexity, naming violations, scope creep, and missing goal definitions.
argument-hint: [optional file or scope]
disable-model-invocation: true
---

# Constitutional Audit

Audits the working tree against the 4 Karpathy constitutional principles defined in CLAUDE.md.

## Audit Checklist

### Principle 1: Think Before Coding
- [ ] Were there assumptions made without verification?
- [ ] Were ambiguous situations resolved silently?
- [ ] Are there trade-offs that should be documented?

### Principle 2: Simplicity First
- [ ] Can any code be removed without changing behavior?
- [ ] Are there abstractions for single-use cases?
- [ ] Is there dead code, unused imports, or commented-out code?
- [ ] Are there unnecessary error handling paths for impossible scenarios?

### Principle 3: Surgical Changes
- [ ] Does every changed line trace back to the original request?
- [ ] Are there "drive-by fixes" to unrelated code?
- [ ] Was existing formatting/styling preserved?
- [ ] Did we delete pre-existing dead code without being asked? (Wrong!)

### Principle 4: Goal-Driven Execution
- [ ] Was there a clear success criterion?
- [ ] Did we loop to verify the goal was met?

## Report Format

Output a concise report:
```
## Constitutional Audit: [scope]
### ✅ PASS / ⚠️ WARN / ❌ FAIL
- Violation 1: ...
- Violation 2: ...

### Action Items
- [ ] Suggested fix for each violation
```
