# 🚀 ZombieCoder Local AI Quick Start Guide

> **Complete Local AI Setup for Cursor, VS Code, and Terminal**

## 🎯 What You'll Get

- **🧠 Local AI Models** (Ollama + Llama)
- **🔌 OpenAI API Compatible** (Port 8001)
- **🧟‍♂️ Advanced AI Agents** (Port 12345)
- **📱 Editor Integration** (Cursor, VS Code, Terminal)
- **⚡ Zero Cloud Dependency** (100% Local)

## 🚀 One-Click Setup

### Step 1: Run GLOBAL_LAUNCHER.bat
```bash
# Double-click or run in terminal
GLOBAL_LAUNCHER.bat
```

**What it does automatically:**
- 🧹 Cleans up blocked ports
- 🔧 Sets environment variables
- 📝 Creates configuration files
- 🚀 Starts all services
- 🧪 Tests all APIs
- ✅ Configures editors

### Step 2: Wait for Completion
```
====================================================
   🧟‍♂️ ZombieCoder Local AI System Starting...
====================================================

[1/5] 🧹 Cleaning up blocked ports and processes...
[2/5] 🤖 Starting Ollama Models...
[3/5] 🔌 Starting OpenAI Shim Server...
[4/5] 🧟‍♂️ Starting ZombieCoder Agent System...
[5/5] 🔄 Starting Additional Services...

🎯 All services started! Checking status...
📊 Checking Service Status...
✅ Ollama: http://127.0.0.1:11434 - RUNNING
✅ OpenAI Shim: http://127.0.0.1:8001 - RUNNING
✅ ZombieCoder: http://127.0.0.1:12345 - RUNNING
```

## 📱 Editor Integration

### 🎨 Cursor AI
1. **Automatic Setup** ✅ (via GLOBAL_LAUNCHER.bat)
2. **Test**: Press `Ctrl+Shift+I`
3. **Configuration**: `.env` file auto-created

### 🔧 VS Code
1. **Automatic Setup** ✅ (via GLOBAL_LAUNCHER.bat)
2. **Test**: `Ctrl+Shift+P` → ZombieCoder
3. **Configuration**: `.vscode/settings.json` auto-created

### 💻 Terminal
1. **Test Local AI**:
```bash
curl http://127.0.0.1:8001/health
```

2. **Test AI Chat**:
```bash
curl -X POST http://127.0.0.1:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"local-llama","messages":[{"role":"user","content":"Hello"}]}'
```

## 🔍 Verification

### Check All Services
```bash
# Port Status
netstat -an | findstr ":8001\|:12345\|:11434"

# Service Health
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:12345/
curl http://127.0.0.1:11434/api/tags
```

### Check Configuration Files
```bash
# Environment Files
dir /s .env

# VS Code Settings
type .vscode\settings.json

# Cursor Rules
type .cursorrules
```

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Kill processes on ports
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8001"') do taskkill /PID %%a /F
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":12345"') do taskkill /PID %%a /F
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":11434"') do taskkill /PID %%a /F
```

### Service Not Starting
```bash
# Check Python installation
python --version

# Check Ollama installation
ollama --version

# Check logs
dir core-server\logs
```

### Editor Not Working
```bash
# Restart editor after setup
# Verify .env file exists
# Check environment variables
echo %OPENAI_API_BASE%
```

## 📋 Configuration Files Created

### .env (Root Directory)
```bash
OPENAI_API_BASE=http://127.0.0.1:8001/v1
OPENAI_API_KEY=local-ai-key
FORCE_LOCAL_AI=true
LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1
ZOMBIECODER_HOST=http://127.0.0.1:12345
OLLAMA_HOST=http://127.0.0.1:11434
```

### .vscode/settings.json
```json
{
  "openai.apiBase": "http://127.0.0.1:8001/v1",
  "openai.apiKey": "local-ai-key",
  "openai.forceLocal": true,
  "zombiecoder.endpoint": "http://127.0.0.1:8001/v1",
  "zombiecoder.apiKey": "local-ai-key"
}
```

### .cursorrules
```bash
# Cursor AI Local Configuration
FORCE_LOCAL_AI=true
LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1
LOCAL_AI_KEY=local-ai-key
AI_MODEL=local-llama
AI_PROVIDER=zombiecoder
```

## 🎉 Success Indicators

### ✅ All Services Running
- Ollama: Port 11434 ✅
- OpenAI Shim: Port 8001 ✅
- ZombieCoder: Port 12345 ✅
- Proxy: Port 8080 ✅
- Multi-Project API: Port 8081 ✅

### ✅ Editor Integration
- Cursor AI: Local AI working ✅
- VS Code: ZombieCoder extension ready ✅
- Terminal: curl commands working ✅

### ✅ Configuration
- Environment variables set ✅
- .env files created ✅
- VS Code settings configured ✅
- Cursor rules applied ✅

## 🔄 Daily Usage

### Start System
```bash
GLOBAL_LAUNCHER.bat
```

### Stop System
```bash
# Kill all processes
taskkill /F /IM python.exe
taskkill /F /IM ollama.exe
```

### Check Status
```bash
# Quick status check
curl http://127.0.0.1:8001/health
```

## 🆘 Need Help?

1. **Check this guide** 📖
2. **Run GLOBAL_LAUNCHER.bat** 🚀
3. **Check troubleshooting section** 🔍
4. **Verify configuration files** 📝

---

**🎯 Your Local AI System is Ready!**

- **No more cloud dependency** ☁️➡️🏠
- **Faster response times** ⚡
- **Complete privacy** 🔒
- **Advanced AI agents** 🤖
- **Editor integration** 📱
