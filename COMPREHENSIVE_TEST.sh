#!/bin/bash

echo "🧟 ZombieCoder Comprehensive Test for Linux"
echo "==========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    fi
}

# Test 1: Check Python installation
echo "1. Testing Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_status "OK" "Python found: $PYTHON_VERSION"
else
    print_status "ERROR" "Python3 not found"
    exit 1
fi

# Test 2: Check virtual environment
echo "2. Testing virtual environment..."
if [ -d "zombie_env" ]; then
    print_status "OK" "Virtual environment exists"
else
    print_status "WARN" "Virtual environment not found"
    echo "Creating virtual environment..."
    python3 -m venv zombie_env
    print_status "OK" "Virtual environment created"
fi

# Test 3: Check required packages
echo "3. Testing required packages..."
source zombie_env/bin/activate
REQUIRED_PACKAGES=("Flask" "Flask-CORS" "python-dotenv" "requests" "PyYAML" "psutil" "transformers" "torch" "numpy")

for package in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        print_status "OK" "$package is installed"
    else
        print_status "ERROR" "$package is missing"
        echo "Installing $package..."
        pip install "$package"
    fi
done

# Test 4: Check Ollama
echo "4. Testing Ollama..."
if pgrep -x "ollama" > /dev/null; then
    print_status "OK" "Ollama is running"
    
    # Test Ollama API
    if curl -s http://localhost:11434/api/tags > /dev/null; then
        print_status "OK" "Ollama API is responding"
    else
        print_status "WARN" "Ollama API not responding"
    fi
else
    print_status "WARN" "Ollama is not running"
    echo "To start Ollama: ollama serve"
fi

# Test 5: Check core-server files
echo "5. Testing core-server files..."
if [ -f "core-server/unified_agent_system.py" ]; then
    print_status "OK" "unified_agent_system.py found"
else
    print_status "ERROR" "unified_agent_system.py not found"
fi

if [ -f "core-server/config.json" ]; then
    print_status "OK" "config.json found"
else
    print_status "WARN" "config.json not found"
fi

# Test 6: Check network connectivity (blocked domains)
echo "6. Testing network security..."
BLOCKED_DOMAINS=("api.openai.com" "api.anthropic.com" "huggingface.co")

for domain in "${BLOCKED_DOMAINS[@]}"; do
    if curl -s --connect-timeout 5 "https://$domain" > /dev/null; then
        print_status "WARN" "$domain is accessible (should be blocked)"
    else
        print_status "OK" "$domain is blocked"
    fi
done

# Test 7: Check system resources
echo "7. Testing system resources..."
MEMORY_AVAILABLE=$(free -m | awk 'NR==2{printf "%.1f", $7/1024}')
print_status "INFO" "Available memory: ${MEMORY_AVAILABLE}GB"

DISK_AVAILABLE=$(df -h . | awk 'NR==2{print $4}')
print_status "INFO" "Available disk space: $DISK_AVAILABLE"

# Test 8: Test Unified Agent System startup
echo "8. Testing Unified Agent System startup..."
cd core-server
timeout 10s python3 unified_agent_system.py > /tmp/zombie_test.log 2>&1 &
PID=$!
sleep 3

if kill -0 $PID 2>/dev/null; then
    print_status "OK" "Unified Agent System started successfully"
    kill $PID 2>/dev/null
else
    print_status "ERROR" "Unified Agent System failed to start"
    echo "Error log:"
    cat /tmp/zombie_test.log
fi

cd ..

# Summary
echo ""
echo "==========================================="
echo "🧟 Test Summary:"
echo "==========================================="
echo "All tests completed. Check the output above for any issues."
echo ""
echo "To start ZombieCoder:"
echo "  ./SIMPLE_LAUNCHER.sh"
echo ""
echo "To block cloud AI services:"
echo "  sudo nano /etc/hosts"
echo "  Add: 127.0.0.1 api.openai.com"
echo "  Add: 127.0.0.1 api.anthropic.com"
echo "  Add: 127.0.0.1 huggingface.co"
