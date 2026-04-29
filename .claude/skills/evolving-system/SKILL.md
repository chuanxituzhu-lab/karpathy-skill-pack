---
name: evolving-system
description: Self-evolution engine. Analyzes experience logs, generates improvement proposals, and applies system-level optimizations. Invoked via /evolve.
argument-hint: [status | propose | apply <id>]
disable-model-invocation: true
---

# Evolving System — Self-Evolution Engine

Constitutional self-evolution following the OODA loop:
**Observe** → **Orient** → **Decide** → **Act**

## Commands

### `/evolve status`

Compute and display system health metrics from the evolution log.

**Dashboard Output:**
```
Evolution System Status
━━━━━━━━━━━━━━━━━━━━━━
Events: 11 total (since 2026-04-29)
  ├─ file_edit:       10 (91%)
  ├─ skill_suggestion: 0  (0%)
  ├─ quality_gate:     0  (0%)
  ├─ audit_result:     0  (0%)
  └─ evolution_applied:0  (0%)

File Type Distribution (Top 3):
  ├─ md:  8 (73%)
  ├─ sh:  1 (9%)
  └─ json: 1 (9%)

Skill Invocation Frequency (last 7d): No data yet
Trigger Effectiveness: No data yet
Quality Gate Warnings: 0 total — trend: stable
Audit Pass Rate: No audits run yet
Pending Proposals: 1 (P001-evolution-dashboard)
Evolution Applied: 0
```

**Metrics computed from `.claude/evolution/log.jsonl`:**
- Total events by type (count + % breakdown)
- File type distribution (top 3 extensions by edit count)
- Per-skill invocation frequency (last 7d / 30d)
- Trigger effectiveness (hit rate per skill from skill_suggestion events)
- Quality gate warning trends (total, per-file-type)
- Constitutional audit pass rate (P1-P4 pass/warn/fail from audit_result events)
- Pending proposal count
- Evolution history (recent evolution_applied events)

### `/evolve propose`

Analyze the experience log and auto-generate evolution proposals.

**Detection Rules:**
| Observation | Proposal |
|---|---|
| Skill with 0 activations in 30 days | Demote priority or remove triggers |
| File type edited 10+ times with no matching skill | Add new trigger patterns |
| Trigger pattern never matched | Remove or replace pattern |
| Quality gate warnings >5 on same file type | Add specialized quality rules |
| Audit failures cluster on one principle | Add targeted constitutional reminder |
| Single skill dominates >60% of activations | Consider splitting |

Proposals saved to `.claude/evolution/proposals/<id>.md`.

### `/evolve apply <id>`

Apply a specific evolution proposal from `.claude/evolution/proposals/`.

**Safety Checks (Constitutional):**
1. Will this change break existing functionality? (P3 — Surgical)
2. Can the same goal be achieved with fewer changes? (P2 — Simplicity)
3. Is the observation backed by log data? (P1 — Think)
4. What is the success criterion? (P4 — Goal-Driven)

## Auto-Evolution (Cowork Mode)

In cowork mode, auto-orchestrator triggers `/evolve propose` when:
- Every 20 log entries accumulated since last proposal
- After applying an evolution proposal (verification cycle)
- On `/auto-scan full` if evolution data exists

## Evolution Log

All events stored in `.claude/evolution/log.jsonl` (append-only JSONL):

| Event Type | When | Data |
|---|---|---|
| `file_edit` | PostToolUse | file path, extension, tool |
| `skill_suggestion` | UserPromptSubmit | matched skill, trigger keyword |
| `quality_gate` | PostToolUse | file, warning count |
| `audit_result` | /constitutional-audit | P1-P4 pass/warn/fail |
| `evolution_applied` | /evolve apply | proposal ID, changes |

## Constitutional Constraints

Self-evolution MUST obey the 4 principles:

1. **Think** — Every proposal states the observation and reasoning
2. **Simplicity** — Remove dead weight before adding new features
3. **Surgical** — One proposal = one change. Never bundle.
4. **Goal-Driven** — Every proposal has a success criterion; verify after apply
