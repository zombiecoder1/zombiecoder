#!/usr/bin/env bash
set -euo pipefail
BACKUP=/etc/hosts.backup-cursor
if [ -f "$BACKUP" ]; then
  sudo mv "$BACKUP" /etc/hosts
  echo "[Hosts] Reverted to backup."
else
  echo "[Hosts] Backup not found; no changes made."
fi
