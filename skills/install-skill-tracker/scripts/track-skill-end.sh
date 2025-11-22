#!/bin/bash
# Track skill completion and calculate duration

HOOK_INPUT=$(cat)
TOOL_NAME=$(echo "$HOOK_INPUT" | jq -r '.tool_name')
SKILL_NAME=$(echo "$HOOK_INPUT" | jq -r '.tool_input.skill')
SESSION_ID=$(echo "$HOOK_INPUT" | jq -r '.session_id')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
EPOCH=$(date '+%s')

# Create log directory if it doesn't exist
LOG_DIR="${CLAUDE_PROJECT_DIR:-.}/.claude/activity-logs"
mkdir -p "$LOG_DIR"

# Calculate duration if start time exists
TEMP_FILE="$LOG_DIR/skill-start-${SESSION_ID}-${SKILL_NAME}.tmp"
DURATION="unknown"
if [ -f "$TEMP_FILE" ]; then
  START_EPOCH=$(cat "$TEMP_FILE")
  DURATION=$((EPOCH - START_EPOCH))
  # Clean up temp file
  rm -f "$TEMP_FILE"
fi

# Log skill completion with duration
LOG_FILE="$LOG_DIR/skill-usage.jsonl"
jq -n \
  --arg ts "$TIMESTAMP" \
  --arg epoch "$EPOCH" \
  --arg sid "$SESSION_ID" \
  --arg skill "$SKILL_NAME" \
  --arg event "end" \
  --arg dur "$DURATION" \
  '{timestamp: $ts, epoch: $epoch, session: $sid, skill: $skill, event: $event, duration_seconds: $dur}' >> "$LOG_FILE"

# Allow normal completion (exit 0 = success)
exit 0
