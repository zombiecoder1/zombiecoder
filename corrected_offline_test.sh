#!/bin/bash
# 🧪 Corrected Offline Test for ZombieCoder
# Uses correct Ollama endpoints

echo "🧪 ZOMBIECODER CORRECTED OFFLINE TEST"
echo "===================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Function to test internet
test_internet() {
    if ping -c 1 -W 3 8.8.8.8 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Internet: Connected${NC}"
        return 0
    else
        echo -e "${RED}❌ Internet: Disconnected${NC}"
        return 1
    fi
}

# Function to test Ollama directly
test_ollama_ai() {
    echo -e "${YELLOW}🤖 Testing Ollama AI Response...${NC}"
    
    local response=$(curl -s -X POST "http://localhost:11434/api/generate" \
        -H "Content-Type: application/json" \
        -d '{"model": "llama2:7b", "prompt": "Say hello in Bengali", "stream": false}' 2>/dev/null)
    
    if echo "$response" | grep -q "response"; then
        local ai_response=$(echo "$response" | grep -o '"response":"[^"]*"' | cut -d'"' -f4)
        echo -e "   ${GREEN}✅ Ollama AI: Working${NC}"
        echo -e "   ${BLUE}📝 Response: ${ai_response:0:60}...${NC}"
        return 0
    else
        echo -e "   ${RED}❌ Ollama AI: Failed${NC}"
        return 1
    fi
}

# Function to test local services
test_local_services() {
    local services=(
        "ZombieCoder Agent:http://localhost:12345"
        "OpenAI Shim:http://localhost:8001"
        "Truth Checker:http://localhost:8002"
        "Ollama:http://localhost:11434"
    )
    
    local active=0
    local total=${#services[@]}
    
    for service in "${services[@]}"; do
        IFS=':' read -r name url <<< "$service"
        if curl -s --max-time 2 "$url" > /dev/null 2>&1; then
            echo -e "   ${GREEN}✅ $name: Active${NC}"
            ((active++))
        else
            echo -e "   ${RED}❌ $name: Inactive${NC}"
        fi
    done
    
    echo -e "${BLUE}📊 Local Services: $active/$total active${NC}"
    return $active
}

# Function to get network interface
get_network_interface() {
    if ip link show | grep -q "enp3s0"; then
        echo "enp3s0"
    elif ip link show | grep -q "eth0"; then
        echo "eth0"
    elif ip link show | grep -q "wlan0"; then
        echo "wlan0"
    else
        ip link show | grep -E "^[0-9]+:" | grep -v "lo:" | head -1 | cut -d: -f2 | tr -d ' '
    fi
}

echo -e "${CYAN}🔍 INITIAL STATUS CHECK${NC}"
echo "========================"
test_internet
test_local_services

echo ""
echo -e "${CYAN}🤖 PRE-OFFLINE AI TEST${NC}"
echo "========================"
test_ollama_ai

# Get network interface
INTERFACE=$(get_network_interface)
echo -e "${BLUE}📡 Network Interface: $INTERFACE${NC}"

echo ""
echo -e "${RED}🔌 DISCONNECTING INTERNET...${NC}"
echo "================================"
sudo ip link set "$INTERFACE" down

# Wait for disconnection
sleep 3

# Verify disconnection
if test_internet; then
    echo -e "${YELLOW}⚠️  Internet still connected, trying DNS blocking...${NC}"
    sudo iptables -A OUTPUT -p udp --dport 53 -j DROP
    sudo iptables -A OUTPUT -p tcp --dport 53 -j DROP
fi

echo ""
echo -e "${PURPLE}⏱️  OFFLINE PERIOD (30 seconds)${NC}"
echo "=============================="
echo -e "${YELLOW}Testing offline AI functionality...${NC}"

# Test during offline period
for i in {30..1}; do
    echo -n -e "\r${CYAN}⏰ Time remaining: ${i}s${NC}"
    
    # Test every 5 seconds
    if [ $((i % 5)) -eq 0 ]; then
        echo ""
        echo -e "${BLUE}🏠 Local Services Status:${NC}"
        test_local_services > /dev/null 2>&1
        
        # Test AI every 10 seconds
        if [ $((i % 10)) -eq 0 ]; then
            test_ollama_ai > /dev/null 2>&1
        fi
    fi
    
    sleep 1
done

echo ""
echo ""
echo -e "${GREEN}🔌 RECONNECTING INTERNET...${NC}"
echo "=============================="
sudo ip link set "$INTERFACE" up

# Remove DNS blocks
sudo iptables -D OUTPUT -p udp --dport 53 -j DROP 2>/dev/null
sudo iptables -D OUTPUT -p tcp --dport 53 -j DROP 2>/dev/null

# Wait for reconnection
echo -e "${YELLOW}⏳ Waiting for reconnection...${NC}"
for i in {1..10}; do
    if test_internet; then
        echo -e "${GREEN}✅ Internet reconnected!${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

echo ""
echo -e "${CYAN}🤖 POST-RECONNECT AI TEST${NC}"
echo "=========================="
test_ollama_ai

echo ""
echo -e "${GREEN}🎯 CORRECTED TEST COMPLETE!${NC}"
echo "============================="
echo -e "${BLUE}📊 Final Results:${NC}"
echo -e "   Internet: $(test_internet && echo -e "${GREEN}Connected${NC}" || echo -e "${RED}Disconnected${NC}")"
echo -e "   Local Services: $(test_local_services > /dev/null 2>&1; echo "$?/4 active")"
echo -e "   AI Functionality: $(test_ollama_ai > /dev/null 2>&1 && echo -e "${GREEN}Working${NC}" || echo -e "${RED}Not Working${NC}")"
echo ""
echo -e "${PURPLE}💡 If AI worked during the 30-second offline period,${NC}"
echo -e "${PURPLE}   your ZombieCoder local setup is successful! 🚀${NC}"
