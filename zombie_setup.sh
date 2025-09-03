#!/bin/bash
# ==============================
# 🚀 ZombieCoder Full Setup Script (Ubuntu)
# ==============================

echo -e "\n⚡ Starting ZombieCoder Setup..."

# Step 1: Root directory এ যাও
cd /home/sahon/Desktop/zombiecoder || exit
echo "📂 Changed directory to /home/sahon/Desktop/zombiecoder"

# Step 2: Install dependencies
echo -e "\n🔧 Installing dependencies..."
sudo apt update -y
sudo apt install -y python3 python3-pip net-tools curl

# Step 3: Launch SIMPLE_LAUNCHER.sh (Linux version)
echo -e "\n🚀 Launching services..."
chmod +x SIMPLE_LAUNCHER.sh
./SIMPLE_LAUNCHER.sh
echo "✅ SIMPLE_LAUNCHER completed!"

# Step 4: Services স্টার্ট হওয়ার জন্য একটু অপেক্ষা করো
echo -e "\n⏳ Waiting 30 seconds for services to fully start..."
sleep 30

# Step 5: Real-time status check
echo -e "\n🌐 Checking ports..."
netstat -tulnp | grep -E "8001|11434|12345"

echo -e "\n⚙️ Checking running processes..."
ps aux | grep -E "ollama|python" | grep -v grep

# Step 6: Comprehensive test চালাও
echo -e "\n🧪 Running Comprehensive Test..."
chmod +x COMPREHENSIVE_TEST.sh
./COMPREHENSIVE_TEST.sh
echo "✅ Comprehensive test completed!"

# Step 7: Core server চালাও
echo -e "\n🤖 Starting Unified Agent System..."
cd core-server || exit
python3 unified_agent_system.py

echo -e "\n🎉 ALL DONE! ZombieCoder is fully ready!"
