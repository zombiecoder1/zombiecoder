#!/usr/bin/env bash
unset OPENAI_BASE_URL || true
unset OPENAI_API_KEY || true
unset CURSOR_TELEMETRY_OPTOUT || true
echo "[Revert] Unset local Cursor env vars."
