#!/bin/bash
# 🔌 ZombieCoder Offline Test Script
# Tests if the system works without internet

echo "🔌 ZOMBIECODER OFFLINE TEST"
echo "=========================="

# Function to test connectivity
test_connectivity() {
    local url=$1
    local name=$2
    
    if curl -s --max-time 3 "$url" > /dev/null 2>&1; then
        echo "✅ $name: Connected"
        return 0
    else
        echo "❌ $name: Disconnected"
        return 1
    fi
}

# Function to test local services
test_local_service() {
    local url=$1
    local name=$2
    
    if curl -s --max-time 2 "$url" > /dev/null 2>&1; then
        echo "✅ $name: Running"
        return 0
    else
        echo "❌ $name: Not running"
        return 1
    fi
}

echo ""
echo "🌐 Internet Connectivity Tests:"
echo "-------------------------------"
test_connectivity "https://api.openai.com" "OpenAI API"
test_connectivity "https://api.anthropic.com" "Anthropic API"
test_connectivity "https://google.com" "Google"
test_connectivity "https://github.com" "GitHub"

echo ""
echo "🏠 Local Services Tests:"
echo "-----------------------"
test_local_service "http://localhost:8001" "OpenAI Shim (8001)"
test_local_service "http://localhost:8002" "Truth Checker (8002)"
test_local_service "http://localhost:12345" "ZombieCoder Agent (12345)"
test_local_service "http://localhost:11434" "Ollama (11434)"

echo ""
echo "🔒 Blocking Tests:"
echo "-----------------"
# Test if cloud APIs are blocked
if curl -s --max-time 5 "https://api.openai.com" > /dev/null 2>&1; then
    echo "❌ OpenAI API: NOT BLOCKED (should be blocked)"
else
    echo "✅ OpenAI API: BLOCKED (correct)"
fi

if curl -s --max-time 5 "https://api.anthropic.com" > /dev/null 2>&1; then
    echo "❌ Anthropic API: NOT BLOCKED (should be blocked)"
else
    echo "✅ Anthropic API: BLOCKED (correct)"
fi

echo ""
echo "🤖 Agent Status:"
echo "---------------"
if curl -s "http://localhost:8002/agents" | grep -q "ZombieCoder Unified Agent"; then
    echo "✅ ZombieCoder Agent: Active"
else
    echo "❌ ZombieCoder Agent: Inactive"
fi

if curl -s "http://localhost:8002/agents" | grep -q "Ollama AI Models"; then
    echo "✅ Ollama Models: Active"
else
    echo "❌ Ollama Models: Inactive"
fi

echo ""
echo "📊 Summary:"
echo "----------"
local_services=$(curl -s "http://localhost:8002/status" | grep -o '"active_ports":[0-9]*' | cut -d: -f2)
echo "Active local services: $local_services/5"

# Test if we can get a response from local AI
if curl -s "http://localhost:8001/health" > /dev/null 2>&1; then
    echo "✅ Local AI: Responding"
else
    echo "❌ Local AI: Not responding"
fi

echo ""
echo "🎯 OFFLINE MODE TEST COMPLETE"
echo "============================="
