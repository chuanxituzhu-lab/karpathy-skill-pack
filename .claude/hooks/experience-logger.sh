#!/usr/bin/env bash
# Experience Logger - PostToolUse Hook
# Logs file modification events to the evolution log for self-evolution analysis.
# This is Layer 0 (Observe) of the self-evolution OODA loop.

read -r INPUT

TOOL=$(echo "$INPUT" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
FILE=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)
LOG_FILE=".claude/evolution/log.jsonl"

if [ "$TOOL" = "Edit" ] || [ "$TOOL" = "Write" ]; then
  if [ -n "$FILE" ]; then
    EXT="${FILE##*.}"
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "{\"type\":\"file_edit\",\"ts\":\"$TIMESTAMP\",\"tool\":\"$TOOL\",\"file\":\"$FILE\",\"ext\":\"$EXT\"}" >> "$LOG_FILE"
  fi
fi
