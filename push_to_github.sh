#!/bin/bash

# 🚀 ZombieCoder GitHub Push Script
echo "🚀 Starting ZombieCoder GitHub Push..."

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Not in ZombieCoder directory"
    exit 1
fi

# Check git status
echo "📊 Checking git status..."
git status

# Check if we have commits to push
COMMITS_AHEAD=$(git rev-list --count HEAD ^origin/main 2>/dev/null || echo "0")
echo "📈 Commits ahead of origin: $COMMITS_AHEAD"

if [ "$COMMITS_AHEAD" -eq 0 ]; then
    echo "✅ Nothing to push"
    exit 0
fi

# Try different push methods
echo "🔄 Attempting to push to GitHub..."

# Method 1: Direct push with credential helper
echo "📤 Method 1: Direct push..."
if git push -u origin main; then
    echo "✅ Successfully pushed with git!"
    exit 0
fi

# Method 2: Force push (if needed)
echo "📤 Method 2: Force push..."
if git push -u origin main --force; then
    echo "✅ Successfully force pushed!"
    exit 0
fi

# Method 3: GitHub CLI
echo "📤 Method 3: GitHub CLI..."
if command -v gh &> /dev/null; then
    echo "🔐 Please authenticate with GitHub CLI first:"
    echo "Run: gh auth login"
    echo "Then run this script again"
    
    # Try to push with gh
    if gh repo sync zombiecoder1/zombiecoder --source . --destination .; then
        echo "✅ Successfully synced with GitHub CLI!"
        exit 0
    fi
fi

# Method 4: Create archive and manual upload
echo "📦 Method 4: Creating archive for manual upload..."
tar -czf zombiecoder-backup.tar.gz --exclude='.git' --exclude='zombie_env' --exclude='node_modules' .
echo "📁 Archive created: zombiecoder-backup.tar.gz"
echo "📋 Manual upload instructions:"
echo "1. Go to https://github.com/zombiecoder1/zombiecoder"
echo "2. Click 'uploading an existing file'"
echo "3. Upload zombiecoder-backup.tar.gz"
echo "4. Extract and commit"

echo "❌ All push methods failed. Please check authentication."
echo "🔑 Authentication options:"
echo "1. Personal Access Token: GitHub → Settings → Developer settings → Personal access tokens"
echo "2. SSH Key: ssh-keygen -t ed25519 -C 'zombiecoder58@gmail.com'"
echo "3. GitHub CLI: gh auth login"

exit 1
