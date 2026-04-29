# Evolution Proposal P002: Auto-update event schema and add session tracking

**Generated**: 2026-04-29T09:55:00Z
**Status**: applied 2026-04-29T10:06:00Z
**Confidence**: high

## Observation

Analysis of 29 log events reveals:

1. **Stale metrics**: `metrics.json` shows 14 events, actual is 29 (107% growth)
2. **Unknown event type**: `session_record` appeared in log but is not in the schema (line 27)
3. **Zero audits**: `constitutional-audit` has never been run — 0 `audit_result` events
4. **Missing `evolution_applied` log**: P001 was applied but no entry was appended to log
5. **Single skill trigger**: Only `testing-full-pyramid` ever triggered a suggestion

## Reasoning (P1: Think)

The system is growing organically beyond its original schema. The `session_record` event shows that other sessions are using the log for cross-session tracking. The metrics need to reflect all event types to remain accurate.

## Recommended Changes

1. **Update `metrics.json` schema** to include `session_record` and `evolution_applied` event tracking
2. **Add auto-update note** to evolving-system SKILL.md: `/evolve status` should recompute from raw log, not cached metrics
3. **Document `session_record`** in the log schema table in evolving-system SKILL.md

## Success Criterion (P4: Goal-Driven)

After applying: `metrics.json` accurately reflects all 29 events, and `/evolve status` shows the complete breakdown including `session_record` events.

## Files to Modify

- `.claude/evolution/metrics.json` — update counts
- `.claude/skills/evolving-system/SKILL.md` — add session_record to schema table
