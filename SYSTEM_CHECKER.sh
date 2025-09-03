#!/bin/bash

echo "🔍 ZombieCoder System Checker - Comprehensive Verification"
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
    elif [ "$status" = "CHECKING" ]; then
        echo -e "${CYAN}🔍 $message${NC}"
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

# Function to check service health
check_service_health() {
    local service_name=$1
    local port=$2
    local endpoint=$3
    
    print_status "CHECKING" "Checking $service_name..."
    
    if check_port $port; then
        if [ -n "$endpoint" ]; then
            if curl -s "http://localhost:$port$endpoint" > /dev/null 2>&1; then
                print_status "OK" "$service_name is healthy on port $port"
                return 0
            else
                print_status "WARN" "$service_name is running but API not responding on port $port"
                return 1
            fi
        else
            print_status "OK" "$service_name is running on port $port"
            return 0
        fi
    else
        print_status "ERROR" "$service_name is not running on port $port"
        return 1
    fi
}

# Initialize counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Step 1: Check Python Environment
echo ""
print_status "INFO" "Step 1: Python Environment Check"
echo "----------------------------------------"

TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_status "OK" "Python found: $PYTHON_VERSION"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    print_status "ERROR" "Python3 not found"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
fi

TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
if [ -d "zombie_env" ]; then
    print_status "OK" "Virtual environment exists"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    print_status "ERROR" "Virtual environment not found"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
fi

# Step 2: Check Required Packages
echo ""
print_status "INFO" "Step 2: Package Dependencies Check"
echo "----------------------------------------"

REQUIRED_PACKAGES=("flask" "flask_cors" "dotenv" "requests" "yaml" "psutil" "transformers" "torch" "numpy")

# Activate virtual environment for package checks
source zombie_env/bin/activate

for package in "${REQUIRED_PACKAGES[@]}"; do
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if python3 -c "import $package" 2>/dev/null; then
        print_status "OK" "$package is installed"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        print_status "ERROR" "$package is missing"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
done

# Step 3: Check Ollama
echo ""
print_status "INFO" "Step 3: Ollama Check"
echo "----------------------------------------"

TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
if pgrep -x "ollama" > /dev/null; then
    print_status "OK" "Ollama process is running"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    print_status "ERROR" "Ollama process is not running"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
fi

TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
if curl -s http://localhost:11434/api/tags > /dev/null; then
    print_status "OK" "Ollama API is responding"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    print_status "ERROR" "Ollama API is not responding"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
fi

# Step 4: Check Core Files
echo ""
print_status "INFO" "Step 4: Core Files Check"
echo "----------------------------------------"

CORE_FILES=(
    "core-server/unified_agent_system.py"
    "core-server/proxy_server.py"
    "core-server/multi_project_manager.py"
    "core-server/main_server.py"
    "core-server/advanced_agent_system.py"
    "core-server/config.json"
    "local_ai_integration/truth_checker.py"
    "local_ai_integration/editor_integration.py"
)

for file in "${CORE_FILES[@]}"; do
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ -f "$file" ]; then
        print_status "OK" "$file exists"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        print_status "ERROR" "$file not found"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
done

# Step 5: Check Services
echo ""
print_status "INFO" "Step 5: Services Check"
echo "----------------------------------------"

SERVICES=(
    "Main Server:12345:/"
    "Proxy Server:8080:/"
    "Multi-Project Manager:8001:/"
    "Truth Checker:8002:/"
    "Editor Integration:8003:/"
    "Advanced Agent System:8004:/"
)

for service in "${SERVICES[@]}"; do
    IFS=':' read -r name port endpoint <<< "$service"
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if check_service_health "$name" "$port" "$endpoint"; then
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
done

# Step 6: Check Network Security
echo ""
print_status "INFO" "Step 6: Network Security Check"
echo "----------------------------------------"

BLOCKED_DOMAINS=("api.openai.com" "api.anthropic.com" "huggingface.co" "models.openai.com")

for domain in "${BLOCKED_DOMAINS[@]}"; do
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if curl -s --connect-timeout 5 "https://$domain" > /dev/null; then
        print_status "WARN" "$domain is accessible (should be blocked)"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    else
        print_status "OK" "$domain is blocked"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    fi
done

# Step 7: Check System Resources
echo ""
print_status "INFO" "Step 7: System Resources Check"
echo "----------------------------------------"

TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
MEMORY_AVAILABLE=$(free -m | awk 'NR==2{printf "%.1f", $7/1024}')
if (( $(echo "$MEMORY_AVAILABLE > 2.0" | bc -l) )); then
    print_status "OK" "Available memory: ${MEMORY_AVAILABLE}GB"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    print_status "WARN" "Low memory available: ${MEMORY_AVAILABLE}GB"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
fi

TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
DISK_AVAILABLE=$(df -h . | awk 'NR==2{print $4}' | sed 's/G//')
if (( $(echo "$DISK_AVAILABLE > 10.0" | bc -l) )); then
    print_status "OK" "Available disk space: ${DISK_AVAILABLE}GB"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    print_status "WARN" "Low disk space: ${DISK_AVAILABLE}GB"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
fi

# Step 8: Check Logs Directory
echo ""
print_status "INFO" "Step 8: Logs Directory Check"
echo "----------------------------------------"

TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
if [ -d "logs" ]; then
    print_status "OK" "Logs directory exists"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    print_status "WARN" "Logs directory not found"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
fi

# Final Summary
echo ""
echo "========================================================"
echo "📊 System Check Summary"
echo "========================================================"
echo "Total Checks: $TOTAL_CHECKS"
echo "Passed: $PASSED_CHECKS"
echo "Failed: $FAILED_CHECKS"
echo "Success Rate: $(( (PASSED_CHECKS * 100) / TOTAL_CHECKS ))%"

if [ $FAILED_CHECKS -eq 0 ]; then
    echo ""
    print_status "OK" "🎉 All systems are healthy!"
else
    echo ""
    print_status "WARN" "⚠️  Some issues detected. Please check the errors above."
fi

echo ""
echo "========================================================"
echo "🚀 Quick Actions:"
echo "========================================================"
echo "• Start all systems: ./GLOBAL_LAUNCHER.sh"
echo "• Check specific service: curl http://localhost:PORT/status"
echo "• View logs: tail -f logs/SERVICE_NAME.log"
echo "• Stop all services: pkill -f 'python3.*zombiecoder'"
echo ""

# Show current running processes
echo "========================================================"
echo "🔄 Currently Running ZombieCoder Processes:"
echo "========================================================"
ps aux | grep -E "(python3.*zombiecoder|ollama)" | grep -v grep | while read line; do
    echo "• $line"
done
