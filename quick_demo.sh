#!/bin/bash
# 🚀 Quick Demo Script for ZombieCoder Offline Testing

echo "🚀 ZOMBIECODER QUICK DEMO"
echo "========================"
echo ""

echo "📋 Available Test Scripts:"
echo "1. auto_offline_test.sh - Automatic 30-second offline test"
echo "2. comprehensive_offline_test.sh - Full comprehensive test"
echo "3. offline_test.sh - Basic offline test"
echo "4. mcp_config_checker.py - MCP configuration checker"
echo ""

echo "🎯 RECOMMENDED TEST SEQUENCE:"
echo "============================="
echo ""
echo "Step 1: Check MCP Configuration"
echo "Command: python3 mcp_config_checker.py"
echo ""
echo "Step 2: Run Comprehensive Test"
echo "Command: ./comprehensive_offline_test.sh"
echo ""
echo "Step 3: Run Quick Auto Test"
echo "Command: ./auto_offline_test.sh"
echo ""

echo "⚠️  IMPORTANT NOTES:"
echo "==================="
echo "• Make sure you have sudo access"
echo "• The test will disconnect internet for 30 seconds"
echo "• All local AI services should remain active"
echo "• You can still use Cursor during offline period"
echo ""

echo "🔧 PRE-TEST CHECKLIST:"
echo "======================"
echo "✅ ZombieCoder services running"
echo "✅ Ollama models loaded"
echo "✅ MCP configuration optimized"
echo "✅ Cursor settings updated"
echo ""

read -p "🤔 Do you want to run the comprehensive test now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting comprehensive test..."
    echo ""
    ./comprehensive_offline_test.sh
else
    echo "👋 Test cancelled. You can run it later with:"
    echo "   ./comprehensive_offline_test.sh"
fi
