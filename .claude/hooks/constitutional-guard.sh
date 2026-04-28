#!/usr/bin/env bash
# Constitutional Guard - UserPromptSubmit Hook
# Checks user prompt for constitutional triggers and injects skill suggestions.
# Reads JSON from stdin, outputs reminders to stdout.

read -r INPUT

SESSION_ID=$(echo "$INPUT" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
PROMPT=$(echo "$INPUT" | grep -o '"prompt":"[^"]*"' | cut -d'"' -f4)

# Detect relevant skills based on prompt keywords
SKILL_HINTS=""

if echo "$PROMPT" | grep -qiE "review|audit|quality|naming|refactor|clean"; then
  SKILL_HINTS="$SKILL_HINTS [evaluating-code-clarity]"
fi

if echo "$PROMPT" | grep -qiE "react|next|component|hook|state|render"; then
  SKILL_HINTS="$SKILL_HINTS [building-react-next]"
fi

if echo "$PROMPT" | grep -qiE "vue|composition|pinia"; then
  SKILL_HINTS="$SKILL_HINTS [composing-vue-apps]"
fi

if echo "$PROMPT" | grep -qiE "test|spec|playwright|cypress|vitest"; then
  SKILL_HINTS="$SKILL_HINTS [testing-full-pyramid]"
fi

if echo "$PROMPT" | grep -qiE "docker|container|compose|dockerfile"; then
  SKILL_HINTS="$SKILL_HINTS [containerizing-environments]"
fi

if echo "$PROMPT" | grep -qiE "database|schema|sql|table|index|migration"; then
  SKILL_HINTS="$SKILL_HINTS [designing-database-schemas]"
fi

if [ -n "$SKILL_HINTS" ]; then
  echo "[Constitutional Guard] Relevant skills detected:$SKILL_HINTS"
  echo "Use /constitutional-audit for explicit Karpathy principle check."
fi

# Constitutional reminders for high-risk operations
if echo "$PROMPT" | grep -qiE "refactor|rewrite|migrate|convert|redesign"; then
  echo "[Principle 2 Reminder] Start minimal. Can you do this with fewer changes?"
fi

if echo "$PROMPT" | grep -qiE "install|add|create|generate"; then
  echo "[Principle 3 Reminder] Surgical only: touch nothing beyond the request."
fi
