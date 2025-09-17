#!/usr/bin/env bash
set -euo pipefail
BACKUP=/etc/hosts.backup-cursor
if [ ! -f "$BACKUP" ]; then
  sudo cp /etc/hosts "$BACKUP"
fi
apply_line() {
  local host=$1
  local line="127.0.0.1 ${host}"
  if ! grep -qE "^[#]*\s*127\.0\.0\.1\s+${host}(\s|$)" /etc/hosts; then
    echo "$line" | sudo tee -a /etc/hosts >/dev/null
  fi
}
apply_line api.openai.com
apply_line oai.hf.space
apply_line api.anthropic.com
apply_line api.together.xyz
apply_line api-inference.huggingface.co
apply_line api2.cursor.sh

echo "[Hosts] Applied local overrides. Backup at $BACKUP"
