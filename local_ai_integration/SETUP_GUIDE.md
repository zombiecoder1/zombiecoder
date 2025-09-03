# 🚀 ZombieCoder Local AI Integration - Complete Setup Guide

## 📋 **Overview**

This guide will help you set up a complete local AI system that integrates with Cursor IDE, providing unlimited AI assistance without any cloud calls or usage limits.

## 🎯 **What You'll Get**

- ✅ **100% Local AI** - No cloud calls, unlimited usage
- ✅ **Cursor IDE Integration** - Seamless local AI experience
- ✅ **Multiple AI Models** - ZombieCoder agents + Ollama models
- ✅ **Auto-Fallback System** - Always responsive, even when models are offline
- ✅ **Memory Integration** - Persistent agent memory and learning
- ✅ **Truth Verification** - Ensures agents are truly local

## 🏗️ **System Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Cursor IDE    │    │  OpenAI Shim     │    │  Local AI       │
│                 │────│  (Port 8001)     │────│  Backends       │
│  Ctrl+Shift+Z   │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    │  • ZombieCoder  │
                                               │  • Ollama       │
                                               │  • Fallback     │
                                               └─────────────────┘
```

## 🚀 **Quick Start (5 Minutes)**

### Step 1: Install Dependencies
```bash
cd local_ai_integration
pip install -r requirements.txt
```

### Step 2: Start Local AI System
```bash
# Start OpenAI Shim Server
python openai_shim.py

# In another terminal, start ZombieCoder
cd ..
python core-server/advanced_agent_system.py

# In another terminal, start Ollama (if you have it)
ollama serve
```

### Step 3: Test Integration
```bash
cd local_ai_integration
python test_local_setup.py
```

### Step 4: Verify Everything Works
```bash
python final_verification.py
```

## 🔧 **Detailed Setup Instructions**

### 1. **Environment Setup**

#### Install Python Dependencies
```bash
pip install flask flask-cors requests psutil
```

#### Verify Installation
```bash
python -c "import flask, requests, psutil; print('✅ Dependencies installed')"
```

### 2. **OpenAI Shim Server Setup**

#### Start the Server
```bash
cd local_ai_integration
python openai_shim.py
```

#### Verify Server is Running
```bash
# Test health endpoint
curl http://127.0.0.1:8001/health

# Test models endpoint
curl http://127.0.0.1:8001/v1/models

# Test chat endpoint
curl -X POST http://127.0.0.1:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-coder:latest", "messages": [{"role": "user", "content": "Hello"}]}'
```

### 3. **ZombieCoder Agent System Setup**

#### Start Agent System
```bash
cd core-server
python advanced_agent_system.py
```

#### Verify Agents are Running
```bash
# Test status endpoint
curl http://127.0.0.1:12345/status

# Test chat with agent
curl -X POST http://127.0.0.1:12345/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "agent": "সাহন ভাই"}'
```

### 4. **Ollama Models Setup (Optional)**

#### Install Ollama
- Windows: Download from [ollama.ai](https://ollama.ai)
- Or use: `winget install Ollama.Ollama`

#### Start Ollama Service
```bash
ollama serve
```

#### Pull Models
```bash
ollama pull deepseek-coder:latest
ollama pull llama3.2:1b
```

#### Verify Ollama
```bash
curl http://127.0.0.1:11434/api/tags
```

### 5. **Cursor IDE Integration**

#### Set Environment Variables
```powershell
# PowerShell (run as Administrator)
setx OPENAI_API_KEY "local-only"
setx OPENAI_API_BASE "http://127.0.0.1:8001/v1"
setx OPENAI_BASE_URL "http://127.0.0.1:8001/v1"
```

#### Configure Hosts File (Admin Required)
1. Open Notepad as Administrator
2. Open: `C:\Windows\System32\drivers\etc\hosts`
3. Add these lines:
```
127.0.0.1   api.openai.com
127.0.0.1   oai.hf.space
127.0.0.1   openaiapi-site.azureedge.net
127.0.0.1   api.anthropic.com
```
4. Save and close

#### Restart Cursor IDE
- Close Cursor completely
- Reopen Cursor
- Test with Ctrl+Shift+Z

### 6. **Port Configuration (Optional)**

#### Set up Port Redirect (Admin Required)
```bash
# Redirect HTTPS (443) to OpenAI Shim (8001)
netsh interface portproxy add v4tov4 listenport=443 listenaddress=127.0.0.1 connectport=8001 connectaddress=127.0.0.1

# Verify redirect
netsh interface portproxy show all
```

## 🧪 **Testing & Verification**

### 1. **Quick Health Check**
```bash
python test_local_setup.py
```

### 2. **Complete System Verification**
```bash
python final_verification.py --save
```

### 3. **Agent Truth Verification**
```bash
python truth_checker.py --save
```

### 4. **Manual Testing**
```bash
# Test OpenAI Shim
curl http://127.0.0.1:8001/v1/models

# Test ZombieCoder
curl http://127.0.0.1:12345/status

# Test Ollama
curl http://127.0.0.1:11434/api/tags
```

## 🔄 **Auto-Startup Configuration**

### Windows Auto-Startup
```bash
# Run as Administrator
setup_auto_startup.bat
```

### Manual Start
```bash
start_local_ai.bat
```

### Desktop Shortcut
- Double-click "ZombieCoder Local AI" shortcut on desktop
- System will start all services automatically

## 🚨 **Troubleshooting**

### Common Issues & Solutions

#### 1. **Port Already in Use**
```bash
# Check what's using the port
netstat -ano | findstr :8001

# Kill the process
taskkill /PID <PID> /F
```

#### 2. **Permission Denied**
- Run PowerShell as Administrator
- Check Windows Defender/Firewall settings
- Ensure you have write access to project folder

#### 3. **Environment Variables Not Working**
```bash
# Check current values
echo $env:OPENAI_API_BASE

# Set again
$env:OPENAI_API_BASE="http://127.0.0.1:8001/v1"
```

#### 4. **Hosts File Not Working**
- Ensure you're running as Administrator
- Check file permissions
- Try flushing DNS: `ipconfig /flushdns`

#### 5. **Models Not Loading**
```bash
# Check Ollama status
ollama list

# Restart Ollama
ollama serve
```

### Debug Commands
```bash
# Check all ports
netstat -an | findstr "8001\|12345\|11434"

# Test endpoints
python -c "import requests; print(requests.get('http://127.0.0.1:8001/health').text)"

# Check processes
tasklist | findstr "python\|ollama"
```

## 📊 **Performance Optimization**

### 1. **Response Time Optimization**
- Keep models in memory
- Use SSD storage
- Optimize network settings

### 2. **Memory Management**
- Monitor agent memory usage
- Clean up old sessions periodically
- Use lazy loading for capabilities

### 3. **Model Selection**
- Use smaller models for faster responses
- Keep frequently used models loaded
- Implement model switching based on task

## 🔒 **Security Features**

### 1. **Local-Only Operation**
- No data leaves your machine
- All AI processing is local
- Network isolation for AI services

### 2. **Agent Verification**
- Truth-checking system
- Memory isolation per agent
- Secure communication protocols

### 3. **Access Control**
- Local network only
- No external API calls
- Secure memory management

## 📈 **Monitoring & Maintenance**

### 1. **System Health Monitoring**
```bash
# Daily health check
python test_local_setup.py --save

# Weekly comprehensive verification
python final_verification.py --save
```

### 2. **Performance Monitoring**
- Response time tracking
- Memory usage monitoring
- Error rate analysis

### 3. **Log Analysis**
- Check server logs for errors
- Monitor agent performance
- Track system usage patterns

## 🎯 **Advanced Configuration**

### 1. **Custom Model Integration**
- Add new Ollama models
- Configure custom agent capabilities
- Set up model routing rules

### 2. **Memory System Customization**
- Custom memory schemas
- Persistent learning patterns
- Cross-agent memory sharing

### 3. **Network Configuration**
- Custom port assignments
- Load balancing setup
- Failover configuration

## 📞 **Support & Community**

### 1. **Documentation**
- README.md - Quick start guide
- SETUP_GUIDE.md - This comprehensive guide
- Code comments - Inline documentation

### 2. **Testing Tools**
- `test_local_setup.py` - Basic system testing
- `final_verification.py` - Complete system verification
- `truth_checker.py` - Agent verification

### 3. **Reporting Issues**
- Run verification scripts first
- Check logs for error details
- Provide system information

## 🎉 **Success Indicators**

### ✅ **System is Working When:**
- All verification scripts pass
- Cursor IDE responds to Ctrl+Shift+Z
- No cloud API calls are made
- Response times are under 2 seconds
- All agents are accessible

### 🚀 **Ready for Production When:**
- 100% local operation verified
- All tests pass consistently
- Performance meets requirements
- Security measures are active
- Monitoring is in place

---

## 🔥 **Quick Commands Reference**

```bash
# Start everything
start_local_ai.bat

# Test system
python test_local_setup.py

# Verify everything
python final_verification.py

# Check agent truth
python truth_checker.py

# Health check
curl http://127.0.0.1:8001/health
```

---

**Built with ❤️ for the ZombieCoder Family**
*"আমি নিজে বানাইছি" - We build our own future*

For additional support, check the README.md file or run the verification scripts for detailed diagnostics.
