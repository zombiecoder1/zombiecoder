#!/bin/bash

echo "🧟 ZombieCoder Global Launcher - Complete System Startup"
echo "========================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "OK" ]; then
        echo -e "${GREEN}✅ $message${NC}"
    elif [ "$status" = "WARN" ]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    elif [ "$status" = "ERROR" ]; then
        echo -e "${RED}❌ $message${NC}"
    elif [ "$status" = "INFO" ]; then
        echo -e "${BLUE}ℹ️  $message${NC}"
    elif [ "$status" = "STARTING" ]; then
        echo -e "${CYAN}🚀 $message${NC}"
    elif [ "$status" = "RUNNING" ]; then
        echo -e "${PURPLE}🔄 $message${NC}"
    fi
}

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to start service
start_service() {
    local service_name=$1
    local command=$2
    local port=$3
    local log_file=$4
    
    print_status "STARTING" "Starting $service_name..."
    
    if [ -n "$port" ] && check_port $port; then
        print_status "WARN" "$service_name port $port is already in use"
        return 1
    fi
    
    if [ -n "$log_file" ]; then
        nohup bash -c "$command" > "$log_file" 2>&1 &
    else
        nohup bash -c "$command" > /dev/null 2>&1 &
    fi
    
    local pid=$!
    sleep 2
    
    if kill -0 $pid 2>/dev/null; then
        print_status "OK" "$service_name started successfully (PID: $pid)"
        return 0
    else
        print_status "ERROR" "$service_name failed to start"
        return 1
    fi
}

# Step 1: Check and setup virtual environment
echo ""
print_status "INFO" "Step 1: Setting up Python environment..."

if [ ! -d "zombie_env" ]; then
    print_status "WARN" "Virtual environment not found. Creating..."
    python3 -m venv zombie_env
    print_status "OK" "Virtual environment created"
fi

# Activate virtual environment
source zombie_env/bin/activate

# Step 2: Install all required packages
echo ""
print_status "INFO" "Step 2: Installing required packages..."

# Core packages
CORE_PACKAGES=("Flask" "Flask-CORS" "python-dotenv" "requests" "PyYAML" "psutil")
# AI/LLM packages
AI_PACKAGES=("transformers" "torch" "numpy")
# Additional packages
EXTRA_PACKAGES=("cryptography" "pyOpenSSL" "pytest" "black" "flake8")

# Install core packages
for package in "${CORE_PACKAGES[@]}"; do
    if ! python3 -c "import $package" 2>/dev/null; then
        print_status "WARN" "Installing $package..."
        pip install "$package" > /dev/null 2>&1
        if python3 -c "import $package" 2>/dev/null; then
            print_status "OK" "$package installed"
        else
            print_status "ERROR" "Failed to install $package"
        fi
    else
        print_status "OK" "$package already installed"
    fi
done

# Install AI packages
for package in "${AI_PACKAGES[@]}"; do
    if ! python3 -c "import $package" 2>/dev/null; then
        print_status "WARN" "Installing $package..."
        pip install "$package" > /dev/null 2>&1
        if python3 -c "import $package" 2>/dev/null; then
            print_status "OK" "$package installed"
        else
            print_status "ERROR" "Failed to install $package"
        fi
    else
        print_status "OK" "$package already installed"
    fi
done

# Step 3: Check Ollama
echo ""
print_status "INFO" "Step 3: Checking Ollama..."

if pgrep -x "ollama" > /dev/null; then
    print_status "OK" "Ollama is running"
    if curl -s http://localhost:11434/api/tags > /dev/null; then
        print_status "OK" "Ollama API is responding"
    else
        print_status "WARN" "Ollama API not responding"
    fi
else
    print_status "WARN" "Ollama is not running"
    print_status "INFO" "Please start Ollama: ollama serve"
fi

# Step 4: Start Proxy Server
echo ""
print_status "INFO" "Step 4: Starting Proxy Server..."

if [ -f "core-server/proxy_server.py" ]; then
    start_service "Proxy Server" "cd core-server && python3 proxy_server.py" "8080" "logs/proxy_server.log"
    PROXY_STARTED=$?
else
    print_status "ERROR" "proxy_server.py not found"
    PROXY_STARTED=1
fi

# Step 5: Start Multi-Project Manager
echo ""
print_status "INFO" "Step 5: Starting Multi-Project Manager..."

if [ -f "core-server/multi_project_manager.py" ]; then
    start_service "Multi-Project Manager" "cd core-server && python3 multi_project_manager.py" "8001" "logs/multi_project.log"
    MULTI_STARTED=$?
else
    print_status "ERROR" "multi_project_manager.py not found"
    MULTI_STARTED=1
fi

# Step 6: Start Truth Checker
echo ""
print_status "INFO" "Step 6: Starting Truth Checker..."

if [ -f "local_ai_integration/truth_checker.py" ]; then
    start_service "Truth Checker" "cd local_ai_integration && python3 truth_checker.py" "8002" "logs/truth_checker.log"
    TRUTH_STARTED=$?
else
    print_status "ERROR" "truth_checker.py not found"
    TRUTH_STARTED=1
fi

# Step 7: Start Editor Integration
echo ""
print_status "INFO" "Step 7: Starting Editor Integration..."

if [ -f "local_ai_integration/editor_integration.py" ]; then
    start_service "Editor Integration" "cd local_ai_integration && python3 editor_integration.py" "8003" "logs/editor_integration.log"
    EDITOR_STARTED=$?
else
    print_status "ERROR" "editor_integration.py not found"
    EDITOR_STARTED=1
fi

# Step 8: Start Main Server (if not already running)
echo ""
print_status "INFO" "Step 8: Starting Main Server..."

if check_port 12345; then
    print_status "OK" "Main Server already running on port 12345"
    MAIN_STARTED=0
else
    if [ -f "core-server/main_server.py" ]; then
        start_service "Main Server" "cd core-server && python3 main_server.py" "12345" "logs/main_server.log"
        MAIN_STARTED=$?
    else
        print_status "ERROR" "main_server.py not found"
        MAIN_STARTED=1
    fi
fi

# Step 9: Start Advanced Agent System
echo ""
print_status "INFO" "Step 9: Starting Advanced Agent System..."

if [ -f "core-server/advanced_agent_system.py" ]; then
    start_service "Advanced Agent System" "cd core-server && python3 advanced_agent_system.py" "8004" "logs/advanced_agent.log"
    ADVANCED_STARTED=$?
else
    print_status "ERROR" "advanced_agent_system.py not found"
    ADVANCED_STARTED=1
fi

# Step 10: Create logs directory if not exists
mkdir -p logs

# Step 11: Final status check
echo ""
print_status "INFO" "Step 11: Final Status Check..."

sleep 3

# Check all services
SERVICES=(
    "Proxy Server:8080"
    "Multi-Project Manager:8001"
    "Truth Checker:8002"
    "Editor Integration:8003"
    "Main Server:12345"
    "Advanced Agent System:8004"
)

echo ""
echo "========================================================"
echo "🧟 System Status Summary:"
echo "========================================================"

for service in "${SERVICES[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if check_port $port; then
        print_status "OK" "$name is running on port $port"
    else
        print_status "ERROR" "$name is not running on port $port"
    fi
done

# Check Ollama
if pgrep -x "ollama" > /dev/null; then
    print_status "OK" "Ollama is running"
else
    print_status "ERROR" "Ollama is not running"
fi

echo ""
echo "========================================================"
echo "🚀 Available Services:"
echo "========================================================"
echo "• Main Server: http://localhost:12345"
echo "• Proxy Server: http://localhost:8080"
echo "• Multi-Project Manager: http://localhost:8001"
echo "• Truth Checker: http://localhost:8002"
echo "• Editor Integration: http://localhost:8003"
echo "• Advanced Agent System: http://localhost:8004"
echo "• Ollama API: http://localhost:11434"
echo ""

# Show running processes
echo "========================================================"
echo "🔄 Running Processes:"
echo "========================================================"
ps aux | grep -E "(python3|ollama)" | grep -v grep | while read line; do
    echo "• $line"
done

echo ""
print_status "INFO" "All systems started! Check logs in the 'logs' directory."
print_status "INFO" "To stop all services: pkill -f 'python3.*zombiecoder'"
