#!/bin/bash

# ZombieCoder Global Launcher - Fixed Version
# Starts all ZombieCoder services with proper directory handling

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored status
print_status() {
    local status=$1
    local message=$2
    
    case $status in
        "OK")
            echo -e "${GREEN}✅ $message${NC}"
            ;;
        "ERROR")
            echo -e "${RED}❌ $message${NC}"
            ;;
        "WARN")
            echo -e "${YELLOW}⚠️  $message${NC}"
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️  $message${NC}"
            ;;
        "STARTING")
            echo -e "${BLUE}🚀 $message${NC}"
            ;;
    esac
}

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to start service with proper directory handling
start_service() {
    local service_name=$1
    local directory=$2
    local script_name=$3
    local port=$4
    local log_file=$5

    print_status "STARTING" "Starting $service_name..."

    if [ -n "$port" ] && check_port $port; then
        print_status "WARN" "$service_name port $port is already in use"
        return 1
    fi

    if [ ! -f "$directory/$script_name" ]; then
        print_status "ERROR" "$script_name not found in $directory"
        return 1
    fi

    # Create logs directory if it doesn't exist
    mkdir -p logs

    # Start service with proper directory handling
    cd "$directory"
    nohup python3 "$script_name" > "../logs/$log_file" 2>&1 &
    local pid=$!
    cd ..

    sleep 2

    if kill -0 $pid 2>/dev/null; then
        print_status "OK" "$service_name started successfully (PID: $pid)"
        return 0
    else
        print_status "ERROR" "$service_name failed to start"
        return 1
    fi
}

# Main execution
echo "🧟 ZombieCoder Global Launcher - Fixed Version"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "zombie_env" ]; then
    print_status "ERROR" "Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source zombie_env/bin/activate

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    print_status "WARN" "Ollama is not running. Please start Ollama first:"
    echo "   ollama serve"
    echo ""
fi

# Start services
echo ""
echo "🚀 Starting ZombieCoder Services..."
echo "=================================="

# 1. Main Server (Unified Agent System)
start_service "Main Server" "core-server" "unified_agent_system.py" "12345" "main_server.log"

# 2. Proxy Server
start_service "Proxy Server" "core-server" "proxy_server.py" "8080" "proxy_server.log"

# 3. Multi-Project Manager
start_service "Multi-Project Manager" "core-server" "multi_project_manager.py" "8001" "multi_project.log"

# 4. Truth Checker
start_service "Truth Checker" "local_ai_integration" "truth_checker.py" "8002" "truth_checker.log"

# 5. Editor Integration
start_service "Editor Integration" "local_ai_integration" "editor_integration.py" "8003" "editor_integration.log"

# 6. Advanced Agent System
start_service "Advanced Agent System" "core-server" "advanced_agent_system.py" "8004" "advanced_agent.log"

echo ""
echo "🎉 ZombieCoder Services Started!"
echo "================================"
echo ""
echo "📊 Service Status:"
echo "   • Main Server: http://localhost:12345"
echo "   • Proxy Server: http://localhost:8080"
echo "   • Multi-Project Manager: http://localhost:8001"
echo "   • Truth Checker: http://localhost:8002"
echo "   • Editor Integration: http://localhost:8003"
echo "   • Advanced Agent System: http://localhost:8004"
echo "   • Ollama Server: http://localhost:11434"
echo ""
echo "🔧 Management Commands:"
echo "   • Check status: ./SYSTEM_CHECKER.sh"
echo "   • Stop all services: pkill -f 'python3.*zombiecoder'"
echo "   • View logs: tail -f logs/*.log"
echo ""
print_status "INFO" "To stop all services: pkill -f 'python3.*zombiecoder'"
print_status "INFO" "To check system status: ./SYSTEM_CHECKER.sh"
