#!/bin/bash
# 🔓 ZombieCoder unblock script

echo "📂 Backing up hosts file..."
sudo cp /etc/hosts /etc/hosts.bak.$(date +%F-%H%M)

echo "🧹 Removing block entries..."
sudo sed -i '/cursor/d;/openai/d;/anthropic/d;/huggingface/d;/azure/d' /etc/hosts

echo "♻️ Restarting NetworkManager..."
sudo systemctl restart NetworkManager

echo "🔎 Testing connection..."
curl -I https://api.cursor.sh --max-time 5

