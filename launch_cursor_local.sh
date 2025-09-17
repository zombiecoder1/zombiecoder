#!/usr/bin/env bash
set -euo pipefail
export OPENAI_BASE_URL="http://localhost:8080/v1"
export OPENAI_API_KEY="local-ollama"
# Optional: make Cursor prefer local-compatible model name
export CURSOR_TELEMETRY_OPTOUT=1

echo "[Launcher] Using OPENAI_BASE_URL=$OPENAI_BASE_URL"
echo "[Launcher] Starting Cursor..."
# Try common launch commands; adjust if needed
if command -v cursor >/dev/null 2>&1; then
  cursor &
elif command -v AppRun >/dev/null 2>&1; then
  AppRun &
else
  echo "Could not find 'cursor' in PATH. Please start Cursor manually from UI while keeping this terminal open so env vars apply."
fi
