---
name: auto-orchestrator
description: Intelligent automation orchestrator. Coordinates the 6 skills based on detected file changes and project state. Invoked automatically in cowork mode or manually via /auto-scan.
argument-hint: [scan | audit | full]
disable-model-invocation: true
---

# Auto Orchestrator

Intelligent automation that coordinates the 6 skills based on detected file changes.

## Modes

### `scan` (Quick)
Detect changed files, map to relevant skills, output a suggested action plan.

```json
{
  "detected_changes": ["src/components/*.tsx"],
  "relevant_skills": ["building-react-next"],
  "suggested_actions": ["Run /react-review for component audit"],
  "constitutional_concerns": []
}
```

### `audit` (Targeted Run)
Run the relevant skill(s) against changed files.
- `.ts` `.tsx` changes → `evaluating-code-clarity` + `building-react-next`
- `.test.` changes → `testing-full-pyramid`
- `Dockerfile`/`compose` changes → `containerizing-environments`
- `.sql`/`prisma/`/`schema` changes → `designing-database-schemas`
- `.vue` changes → `composing-vue-apps`

### `full` (Comprehensive)
Run all applicable skills across the entire project.

## Automation Rules (Cowork Mode)

In cowork mode (`.claude/current-mode.txt` contains "cowork"), auto-execute after significant file changes:

1. Detect changed file types via `git diff --name-only`
2. Map to relevant skill
3. If `scan` mode flags a `constitutional_concern`, run `constitutional-audit`
4. If number of changed files > 5, suggest `/auto-scan full`

### Self-Evolution Integration

In cowork mode, auto-orchestrator also drives the evolution loop:

- Every 20 log entries in `.claude/evolution/log.jsonl` → auto-run `/evolve propose`
- After `/constitutional-audit` finds a failure → log to evolution log
- After applying any evolution proposal → verify and log the result
- On `/auto-scan full` → include evolution metrics in the comprehensive report

This creates a closed loop: every action feeds the evolution log, and the evolution system feeds back improved triggers and rules.

## Integration

- Works with `skill-rules.json` for trigger-based activation
- Falls back to `/constitutional-audit` for violation checks
- Drives `/evolve` cycle from cowork mode
- Reports results to user as actionable summaries
