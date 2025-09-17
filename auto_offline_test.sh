#!/bin/bash
# 🔌 Automatic Internet Disconnect/Reconnect Test Script
# Tests ZombieCoder AI functionality during offline periods

echo "🚀 ZOMBIECODER AUTOMATIC OFFLINE TEST"
echo "====================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to get network interface
get_network_interface() {
    # Try to find the active network interface
    if ip link show | grep -q "enp3s0"; then
        echo "enp3s0"
    elif ip link show | grep -q "eth0"; then
        echo "eth0"
    elif ip link show | grep -q "wlan0"; then
        echo "wlan0"
    else
        # Get the first non-loopback interface
        ip link show | grep -E "^[0-9]+:" | grep -v "lo:" | head -1 | cut -d: -f2 | tr -d ' '
    fi
}

# Function to test internet connectivity
test_internet() {
    if ping -c 1 -W 3 8.8.8.8 > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to test local AI services
test_local_ai() {
    local services_ok=0
    local total_services=4
    
    if curl -s --max-time 2 "http://localhost:8001" > /dev/null 2>&1; then
        ((services_ok++))
    fi
    
    if curl -s --max-time 2 "http://localhost:8002" > /dev/null 2>&1; then
        ((services_ok++))
    fi
    
    if curl -s --max-time 2 "http://localhost:12345" > /dev/null 2>&1; then
        ((services_ok++))
    fi
    
    if curl -s --max-time 2 "http://localhost:11434" > /dev/null 2>&1; then
        ((services_ok++))
    fi
    
    echo "$services_ok/$total_services"
}

# Function to test AI response
test_ai_response() {
    echo "🤖 Testing AI response..."
    
    # Try to get a simple response from local AI
    local response=$(curl -s --max-time 5 -X POST "http://localhost:8001/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "local-llama",
            "messages": [{"role": "user", "content": "Hello, are you working?"}],
            "max_tokens": 50
        }' 2>/dev/null)
    
    if echo "$response" | grep -q "choices"; then
        echo "✅ AI Response: Working"
        return 0
    else
        echo "❌ AI Response: Not working"
        return 1
    fi
}

# Get network interface
INTERFACE=$(get_network_interface)
echo -e "${BLUE}📡 Network Interface: $INTERFACE${NC}"

# Initial status check
echo ""
echo -e "${YELLOW}🔍 INITIAL STATUS CHECK${NC}"
echo "========================"

if test_internet; then
    echo -e "${GREEN}✅ Internet: Connected${NC}"
else
    echo -e "${RED}❌ Internet: Disconnected${NC}"
fi

echo -e "${BLUE}🏠 Local Services: $(test_local_ai) active${NC}"

# Test AI before disconnect
echo ""
echo -e "${YELLOW}🤖 PRE-DISCONNECT AI TEST${NC}"
echo "=========================="
test_ai_response

echo ""
echo -e "${RED}🔌 DISCONNECTING INTERNET...${NC}"
echo "================================"

# Disconnect internet
if [ "$INTERFACE" != "" ]; then
    sudo ip link set "$INTERFACE" down
    echo -e "${RED}❌ Internet disconnected via $INTERFACE${NC}"
else
    echo -e "${RED}❌ Could not find network interface${NC}"
    exit 1
fi

# Wait 2 seconds for disconnection to take effect
sleep 2

# Verify disconnection
if test_internet; then
    echo -e "${YELLOW}⚠️  Internet still connected, trying alternative method...${NC}"
    # Try blocking DNS
    sudo iptables -A OUTPUT -p udp --dport 53 -j DROP
    sudo iptables -A OUTPUT -p tcp --dport 53 -j DROP
fi

echo ""
echo -e "${YELLOW}⏱️  OFFLINE PERIOD (30 seconds)${NC}"
echo "=============================="

# Countdown and test during offline period
for i in {30..1}; do
    echo -n -e "\r${BLUE}⏰ Time remaining: ${i}s${NC}"
    
    # Test local services every 5 seconds
    if [ $((i % 5)) -eq 0 ]; then
        echo ""
        echo -e "${BLUE}🏠 Local Services: $(test_local_ai) active${NC}"
        
        # Test AI response every 10 seconds
        if [ $((i % 10)) -eq 0 ]; then
            test_ai_response
        fi
    fi
    
    sleep 1
done

echo ""
echo ""
echo -e "${GREEN}🔌 RECONNECTING INTERNET...${NC}"
echo "=============================="

# Reconnect internet
sudo ip link set "$INTERFACE" up

# Remove DNS blocks if they were added
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
echo -e "${YELLOW}🤖 POST-RECONNECT AI TEST${NC}"
echo "=========================="
test_ai_response

echo ""
echo -e "${GREEN}🎯 TEST COMPLETE!${NC}"
echo "==============="
echo -e "${BLUE}📊 Final Status:${NC}"
echo -e "   Internet: $(test_internet && echo -e "${GREEN}Connected${NC}" || echo -e "${RED}Disconnected${NC}")"
echo -e "   Local Services: $(test_local_ai) active"
echo ""
echo -e "${YELLOW}💡 If AI worked during offline period, your local setup is successful!${NC}"
