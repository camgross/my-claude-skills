#!/bin/bash
# Debug hook to see what data is available from PostToolUse

HOOK_INPUT=$(cat)
LOG_DIR="${CLAUDE_PROJECT_DIR:-.}/.claude/activity-logs"
mkdir -p "$LOG_DIR"

# Save the full hook input for inspection (pretty-printed)
TIMESTAMP=$(date +%s)
echo "$HOOK_INPUT" | jq '.' > "$LOG_DIR/debug-hook-$TIMESTAMP.json"

# Also save a compact version with timestamp
echo "$HOOK_INPUT" | jq -c '. + {debug_timestamp: "'$TIMESTAMP'"}' >> "$LOG_DIR/debug-hook-data.jsonl"

# Extract and log key fields for quick inspection
TOOL_NAME=$(echo "$HOOK_INPUT" | jq -r '.tool_name // "unknown"')
SKILL_NAME=$(echo "$HOOK_INPUT" | jq -r '.tool_input.skill // "N/A"')
echo "[DEBUG] Tool: $TOOL_NAME, Skill: $SKILL_NAME, Timestamp: $TIMESTAMP" >> "$LOG_DIR/debug-summary.log"

exit 0
