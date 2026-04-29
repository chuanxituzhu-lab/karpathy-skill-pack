#!/usr/bin/env bash
# Quality Gate - PostToolUse Hook
# After edits, checks if constitutional principles were maintained.
# Also logs quality events to the evolution log for self-evolution analysis.

read -r INPUT

TOOL=$(echo "$INPUT" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
FILE=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)
LOG_FILE=".claude/evolution/log.jsonl"

# Only check file modifications
if [ "$TOOL" = "Edit" ] || [ "$TOOL" = "Write" ]; then
  if [ -n "$FILE" ]; then
    FILENAME=$(basename "$FILE")

    # Check for commented-out code (potential P2 violation: left clutter)
    if [ -f "$FILE" ]; then
      COMMENTED_COUNT=$(grep -cE "^\s*//\s*old|^\s*//\s*TODO|^\s*//\s*FIXME" "$FILE" 2>/dev/null || echo "0")
      TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
      if [ "$COMMENTED_COUNT" -gt 5 ]; then
        echo "[Quality Gate] ⚠️ $FILENAME has $COMMENTED_COUNT stale comments. Principle 2: keep it clean."
        echo "{\"type\":\"quality_gate\",\"ts\":\"$TIMESTAMP\",\"file\":\"$FILE\",\"warning\":\"stale_comments\",\"count\":$COMMENTED_COUNT}" >> "$LOG_FILE" 2>/dev/null || true
      fi
    fi

    echo "[Quality Gate] ✓ $FILENAME modified. Verify: Was this change surgical? (P3)"
  fi
fi
