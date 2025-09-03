#!/bin/bash

echo "🧟 ZombieCoder Simple Launcher for Linux"
echo "========================================"

# Check if virtual environment exists
if [ ! -d "zombie_env" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv zombie_env
    source zombie_env/bin/activate
    pip install Flask Flask-CORS python-dotenv requests PyYAML psutil transformers torch numpy
else
    echo "✅ Virtual environment found"
fi

# Check if Ollama is running
if pgrep -x "ollama" > /dev/null; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Ollama not running. Please start Ollama first:"
    echo "   ollama serve"
    echo ""
fi

# Start the Unified Agent System
echo "🚀 Starting ZombieCoder Unified Agent System..."
cd core-server
source ../zombie_env/bin/activate
python3 unified_agent_system.py
