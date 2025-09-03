# 📱 Editor Integration Guide

> **Complete Local AI Integration for Cursor, VS Code, and Terminal**

## 🎯 Overview

This guide covers how to integrate ZombieCoder Local AI with popular code editors and development environments.

## 🚀 Automatic Setup

### GLOBAL_LAUNCHER.bat
The `GLOBAL_LAUNCHER.bat` automatically configures all editors:

```bash
# Run once to set up everything
GLOBAL_LAUNCHER.bat
```

**What it creates automatically:**
- ✅ Environment variables
- ✅ `.env` files in all directories
- ✅ VS Code settings
- ✅ Cursor AI rules
- ✅ API endpoint testing

## 🎨 Cursor AI Integration

### Automatic Configuration
1. **Run GLOBAL_LAUNCHER.bat** ✅
2. **Restart Cursor** 🔄
3. **Test with Ctrl+Shift+I** 🧪

### Manual Configuration
If you need manual setup:

```bash
# Create .env file in your project
echo OPENAI_API_BASE=http://127.0.0.1:8001/v1 > .env
echo OPENAI_API_KEY=local-ai-key >> .env
echo FORCE_LOCAL_AI=true >> .env
echo LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1 >> .env
```

### .cursorrules File
```bash
# Cursor AI Local Configuration
FORCE_LOCAL_AI=true
LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1
LOCAL_AI_KEY=local-ai-key
AI_MODEL=local-llama
AI_PROVIDER=zombiecoder
```

### Testing Cursor AI
1. **Open Cursor**
2. **Press Ctrl+Shift+I**
3. **Type a question**
4. **Verify local AI response**

## 🔧 VS Code Integration

### Automatic Configuration
1. **Run GLOBAL_LAUNCHER.bat** ✅
2. **Install ZombieCoder Extension** 📦
3. **Test with Ctrl+Shift+P** 🧪

### Manual Configuration
Create `.vscode/settings.json`:

```json
{
  "openai.apiBase": "http://127.0.0.1:8001/v1",
  "openai.apiKey": "local-ai-key",
  "openai.forceLocal": true,
  "zombiecoder.endpoint": "http://127.0.0.1:8001/v1",
  "zombiecoder.apiKey": "local-ai-key"
}
```

### Extension Installation
```bash
# Install from VSIX file
code --install-extension shaon-zombiecoder-extension-1.0.0.vsix

# Or from marketplace
# Search: "ZombieCoder"
```

### Testing VS Code
1. **Open VS Code**
2. **Press Ctrl+Shift+P**
3. **Type "ZombieCoder"**
4. **Select command and test**

## 💻 Terminal Integration

### Environment Variables
```bash
# Set for current session
set OPENAI_API_BASE=http://127.0.0.1:8001/v1
set OPENAI_API_KEY=local-ai-key
set FORCE_LOCAL_AI=true
```

### API Testing
```bash
# Health check
curl http://127.0.0.1:8001/health

# Chat completion
curl -X POST http://127.0.0.1:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local-llama",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 100
  }'
```

### ZombieCoder API
```bash
# System status
curl http://127.0.0.1:12345/

# Chat with agent
curl -X POST http://127.0.0.1:12345/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a Python function",
    "agent": "সাহন ভাই"
  }'
```

## 🔍 Verification Commands

### Check All Services
```bash
# Port status
netstat -an | findstr ":8001\|:12345\|:11434"

# Service health
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:12345/
curl http://127.0.0.1:11434/api/tags
```

### Check Configuration
```bash
# Environment files
dir /s .env

# VS Code settings
type .vscode\settings.json

# Cursor rules
type .cursorrules

# Environment variables
echo %OPENAI_API_BASE%
echo %FORCE_LOCAL_AI%
```

## 🚨 Troubleshooting

### Editor Not Working
1. **Verify .env file exists**
2. **Check environment variables**
3. **Restart editor**
4. **Verify API endpoints**

### API Connection Failed
1. **Check if services are running**
2. **Verify port numbers**
3. **Check firewall settings**
4. **Test with curl commands**

### Configuration Issues
1. **Run GLOBAL_LAUNCHER.bat again**
2. **Delete and recreate .env files**
3. **Check file permissions**
4. **Verify Python installation**

## 📋 Configuration Files

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

## 🎯 Success Indicators

### ✅ Cursor AI
- `.env` file exists
- `Ctrl+Shift+I` works
- Local AI responses
- No cloud dependency

### ✅ VS Code
- `.vscode/settings.json` exists
- ZombieCoder extension works
- `Ctrl+Shift+P` → ZombieCoder
- Local AI integration

### ✅ Terminal
- Environment variables set
- `curl` commands work
- API endpoints respond
- Local AI accessible

## 🔄 Daily Workflow

### Start Development
```bash
# 1. Start Local AI System
GLOBAL_LAUNCHER.bat

# 2. Open your editor
# 3. Start coding with local AI
```

### Stop Development
```bash
# Kill all services
taskkill /F /IM python.exe
taskkill /F /IM ollama.exe
```

### Check Status
```bash
# Quick health check
curl http://127.0.0.1:8001/health
```

---

**🎉 Your editors are now fully integrated with Local AI!**

- **No more cloud dependency** ☁️➡️🏠
- **Faster AI responses** ⚡
- **Complete privacy** 🔒
- **Advanced AI capabilities** 🤖
