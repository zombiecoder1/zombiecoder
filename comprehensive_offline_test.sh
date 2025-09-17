#!/bin/bash
# 🧪 Comprehensive Offline Test for ZombieCoder
# Tests everything: MCP, Local AI, Internet blocking, and offline functionality

echo "🧪 ZOMBIECODER COMPREHENSIVE OFFLINE TEST"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Function to print section headers
print_section() {
    echo ""
    echo -e "${CYAN}🔍 $1${NC}"
    echo "$(printf '=%.0s' {1..50})"
}

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

# Function to test AI response
test_ai_response() {
    echo -e "${YELLOW}🤖 Testing AI Response...${NC}"
    
    # Test with a simple question
    local response=$(curl -s --max-time 10 -X POST "http://localhost:8001/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "local-llama",
            "messages": [{"role": "user", "content": "Say hello in Bengali"}],
            "max_tokens": 100
        }' 2>/dev/null)
    
    if echo "$response" | grep -q "choices"; then
        echo -e "   ${GREEN}✅ AI Response: Working${NC}"
        # Extract and show part of response
        local content=$(echo "$response" | grep -o '"content":"[^"]*"' | head -1 | cut -d'"' -f4)
        if [ ! -z "$content" ]; then
            echo -e "   ${BLUE}📝 Response: ${content:0:50}...${NC}"
        fi
        return 0
    else
        echo -e "   ${RED}❌ AI Response: Failed${NC}"
        return 1
    fi
}

# Function to test MCP configuration
test_mcp_config() {
    echo -e "${YELLOW}🔧 Testing MCP Configuration...${NC}"
    
    if [ -f "/home/sahon/.cursor/mcp.json" ]; then
        local cloud_blocked=$(grep -o '"cloud_ai_blocked":[^,]*' /home/sahon/.cursor/mcp.json | cut -d: -f2 | tr -d ' ,')
        local local_ai=$(grep -o '"local_ai_available":[^,]*' /home/sahon/.cursor/mcp.json | cut -d: -f2 | tr -d ' ,')
        
        if [ "$cloud_blocked" = "true" ]; then
            echo -e "   ${GREEN}✅ Cloud AI Blocked: Yes${NC}"
        else
            echo -e "   ${RED}❌ Cloud AI Blocked: No${NC}"
        fi
        
        if [ "$local_ai" = "true" ]; then
            echo -e "   ${GREEN}✅ Local AI Available: Yes${NC}"
        else
            echo -e "   ${RED}❌ Local AI Available: No${NC}"
        fi
    else
        echo -e "   ${RED}❌ MCP configuration file not found${NC}"
    fi
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

# Main test sequence
print_section "INITIAL STATUS CHECK"
test_internet
test_local_services
test_mcp_config

print_section "PRE-OFFLINE AI TEST"
test_ai_response

# Get network interface
INTERFACE=$(get_network_interface)
echo -e "${BLUE}📡 Network Interface: $INTERFACE${NC}"

print_section "DISCONNECTING INTERNET"
echo -e "${RED}🔌 Disconnecting $INTERFACE...${NC}"
sudo ip link set "$INTERFACE" down

# Wait for disconnection
sleep 3

# Verify disconnection
if test_internet; then
    echo -e "${YELLOW}⚠️  Internet still connected, trying DNS blocking...${NC}"
    sudo iptables -A OUTPUT -p udp --dport 53 -j DROP
    sudo iptables -A OUTPUT -p tcp --dport 53 -j DROP
fi

print_section "OFFLINE PERIOD (30 seconds)"
echo -e "${PURPLE}⏱️  Testing offline functionality...${NC}"

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
            test_ai_response > /dev/null 2>&1
        fi
    fi
    
    sleep 1
done

print_section "RECONNECTING INTERNET"
echo -e "${GREEN}🔌 Reconnecting $INTERFACE...${NC}"
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

print_section "POST-RECONNECT TEST"
test_internet
test_local_services
test_ai_response

print_section "FINAL SUMMARY"
echo -e "${GREEN}🎯 COMPREHENSIVE TEST COMPLETE!${NC}"
echo ""
echo -e "${BLUE}📊 Test Results:${NC}"
echo -e "   Internet Status: $(test_internet && echo -e "${GREEN}Connected${NC}" || echo -e "${RED}Disconnected${NC}")"
echo -e "   Local Services: $(test_local_services > /dev/null 2>&1; echo "$?/4 active")"
echo -e "   AI Functionality: $(test_ai_response > /dev/null 2>&1 && echo -e "${GREEN}Working${NC}" || echo -e "${RED}Not Working${NC}")"
echo ""
echo -e "${PURPLE}💡 If AI worked during the 30-second offline period,${NC}"
echo -e "${PURPLE}   your ZombieCoder local setup is successful! 🚀${NC}"
echo ""
echo -e "${CYAN}🔧 To run this test again: ./comprehensive_offline_test.sh${NC}"
