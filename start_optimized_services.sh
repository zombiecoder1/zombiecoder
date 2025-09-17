#!/bin/bash
# ZombieCoder Optimized Launcher
# Starts all services with optimized configurations

echo "🚀 Starting ZombieCoder Optimized System..."

# Create necessary directories
mkdir -p logs memory config

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)/core-server"
export ZOMBIECODER_CONFIG_DIR="$(pwd)/config"
export ZOMBIECODER_MEMORY_DIR="$(pwd)/memory"

# Start services in background
echo "📡 Starting Proxy Server..."
python3 core-server/proxy_server.py > logs/proxy_server.log 2>&1 &
PROXY_PID=$!

echo "🤖 Starting Unified Agent System..."
python3 core-server/unified_agent_system.py > logs/unified_agent.log 2>&1 &
UNIFIED_PID=$!

echo "🔧 Starting Multi Project Manager..."
python3 core-server/multi_project_manager.py > logs/multi_project.log 2>&1 &
MULTI_PID=$!

echo "🎨 Starting Editor Chat Server..."
python3 core-server/editor_chat_server.py > logs/editor_chat.log 2>&1 &
EDITOR_PID=$!

echo "👨‍💻 Starting Friendly Programmer Agent..."
python3 core-server/friendly_programmer_agent.py > logs/friendly_programmer.log 2>&1 &
FRIENDLY_PID=$!

# Save PIDs for later cleanup
echo $PROXY_PID > logs/proxy_server.pid
echo $UNIFIED_PID > logs/unified_agent.pid
echo $MULTI_PID > logs/multi_project.pid
echo $EDITOR_PID > logs/editor_chat.pid
echo $FRIENDLY_PID > logs/friendly_programmer.pid

echo "✅ All services started!"
echo "📊 Check status: curl http://localhost:8001/health"
echo "🛑 Stop services: ./stop_services.sh"
