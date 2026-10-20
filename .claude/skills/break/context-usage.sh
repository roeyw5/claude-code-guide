#!/usr/bin/env bash
# Prints how full this session's context is, read from the transcript's last
# assistant usage record. Usage: context-usage.sh [session_id]
# Window defaults to 1M tokens (sessions here run past 600k); override with
# BREAK_CONTEXT_WINDOW. Threshold for a full handoff prompt: BREAK_LONG_PERCENT (40).
window=${BREAK_CONTEXT_WINDOW:-1000000}
long_percent=${BREAK_LONG_PERCENT:-40}
project_dir="$HOME/.claude/projects/$(pwd | sed 's|[/.]|-|g')"

transcript="$project_dir/$1.jsonl"
if [ -z "$1" ] || [ ! -f "$transcript" ]; then
  # Session id unavailable: fall back to the most recently written transcript.
  transcript=$(ls -t "$project_dir"/*.jsonl 2>/dev/null | head -1)
fi
if [ -z "$transcript" ] || [ ! -f "$transcript" ]; then
  echo "context: unknown (no transcript found) - treat the session as LONG"
  exit 0
fi

tokens=$(tac "$transcript" | jq -r 'select(.type=="assistant" and .message.usage) | .message.usage | (.input_tokens + (.cache_read_input_tokens // 0) + (.cache_creation_input_tokens // 0))' 2>/dev/null | head -1)
compactions=$(rg -c '"compact_boundary"' "$transcript" 2>/dev/null || echo 0)
tokens=${tokens:-0}
percent=$(( tokens * 100 / window ))

if [ "$percent" -ge "$long_percent" ] || [ "$compactions" -gt 0 ]; then
  verdict=LONG
else
  verdict=SHORT
fi
echo "context: ${tokens} tokens of ${window} (${percent}%), compactions: ${compactions} -> ${verdict}"
