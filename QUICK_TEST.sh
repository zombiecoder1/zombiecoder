#!/bin/bash

echo "🚀 ZombieCoder Quick Test Script"
echo "================================"
echo ""

echo "🔍 Checking services..."
echo "Ollama:"
ps aux | grep ollama | grep -v grep || echo "❌ Ollama not running"

echo ""
echo "Proxy:"
ps aux | grep "cursor_proxy_interceptor" | grep -v grep || echo "❌ Proxy not running"

echo ""
echo "🌐 Testing endpoints..."
echo "Ollama API:"
curl -s http://localhost:11434/api/tags | jq '.models[].name' 2>/dev/null || echo "❌ Ollama API not responding"

echo ""
echo "Proxy Health:"
curl -s http://localhost:8080/health || echo "❌ Proxy not responding"

echo ""
echo "🎯 Testing proxy with Ollama..."
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"llama2:7b","messages":[{"role":"user","content":"Hello, test message"}]}' \
  | jq '.choices[0].message.content' 2>/dev/null || echo "❌ Proxy test failed"

echo ""
echo "📊 Memory Dashboard:"
echo "Open: http://localhost:9001/memory_dashboard.html"
echo ""
echo "🎯 Next Steps:"
echo "1. Configure Cursor proxy: http://localhost:8080"
echo "2. Test with Cursor UI"
echo "3. Check dashboard for LOCAL route"
