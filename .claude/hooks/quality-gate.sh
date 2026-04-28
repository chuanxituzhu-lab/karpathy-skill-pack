#!/usr/bin/env bash
# Quality Gate - PostToolUse Hook
# After edits, checks if constitutional principles were maintained.

read -r INPUT

TOOL=$(echo "$INPUT" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
FILE=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)

# Only check file modifications
if [ "$TOOL" = "Edit" ] || [ "$TOOL" = "Write" ]; then
  if [ -n "$FILE" ]; then
    FILENAME=$(basename "$FILE")

    # Check for commented-out code (potential P2 violation: left clutter)
    if [ -f "$FILE" ]; then
      COMMENTED_COUNT=$(grep -cE "^\s*//\s*old|^\s*//\s*TODO|^\s*//\s*FIXME" "$FILE" 2>/dev/null || echo "0")
      if [ "$COMMENTED_COUNT" -gt 5 ]; then
        echo "[Quality Gate] ⚠️ $FILENAME has $COMMENTED_COUNT stale comments. Principle 2: keep it clean."
      fi
    fi

    echo "[Quality Gate] ✓ $FILENAME modified. Verify: Was this change surgical? (P3)"
  fi
fi
