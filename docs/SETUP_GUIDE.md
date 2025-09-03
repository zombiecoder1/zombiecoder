# 🚀 Setup Guide - ZombieCoder Agent Personal

## 📋 Prerequisites

### System Requirements
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **RAM**: Minimum 8GB, Recommended 16GB
- **Storage**: At least 20GB free space
- **Internet**: Required for initial setup and model downloads

### Required Software
1. **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
2. **Node.js 16+**: [Download Node.js](https://nodejs.org/)
3. **Git**: [Download Git](https://git-scm.com/)
4. **Ollama**: [Download Ollama](https://ollama.ai/)

## 🛠️ Installation Steps

### Step 1: Clone the Repository
```bash
git clone https://github.com/devsahon/ZombieCoder-Agent-Personal.git
cd ZombieCoder-Agent-Personal
```

### Step 2: Python Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Node.js Dependencies
```bash
# Navigate to extension directory
cd extension

# Install Node.js dependencies
npm install

# Return to root directory
cd ..
```

### Step 4: Ollama Setup
```bash
# Install Ollama (if not already installed)
# Windows: Download from https://ollama.ai/
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Download required models (in a new terminal)
ollama pull llama3.2:1b
ollama pull qwen2.5-coder:1.5b-base
ollama pull codellama:latest
```

### Step 5: Environment Configuration
```bash
# Create .env file
cp .env.example .env

# Edit .env file with your settings
# Add your API keys for cloud fallback (optional)
OPENROUTER_API_KEY=your_openrouter_key
TOGETHER_API_KEY=your_together_key
```

## 🚀 Quick Start

### One-Click Launch (Recommended)
```bash
# Windows
.\GLOBAL_LAUNCHER.bat

# macOS/Linux
./GLOBAL_LAUNCHER.sh
```

### Manual Launch
```bash
# Terminal 1: Main Server
python our-server/main_server.py

# Terminal 2: Proxy Server
python our-server/proxy_server.py

# Terminal 3: Multi-Project API
python our-server/multi_project_api.py
```

## 🎯 VS Code Extension Installation

### Method 1: Development Installation
```bash
# Copy extension to VS Code extensions directory
# Windows
xcopy extension "%USERPROFILE%\.vscode\extensions\zombiecoder-force-local" /s /e /h

# macOS/Linux
cp -r extension ~/.vscode/extensions/zombiecoder-force-local
```

### Method 2: Manual Installation
1. Open VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
3. Type "Extensions: Install from VSIX"
4. Select the extension folder: `extension/`

### Method 3: Development Mode
```bash
# Navigate to extension directory
cd extension

# Install dependencies
npm install

# Package extension
npm run package

# Install the generated .vsix file in VS Code
```

## 🔧 Configuration

### Main Configuration (`our-server/config.json`)
```json
{
  "memory": {
    "botgachh_path": "data/botgachh/",
    "session_log": "logs/sessions/",
    "task_history": "data/task_history.json"
  },
  "server": {
    "port": 12345,
    "host": "0.0.0.0"
  },
  "agents": {
    "default_agent": "ZombieCoder Agent (সাহন ভাই)",
    "capabilities": ["coding", "debugging", "architecture", "database", "api", "security", "performance", "devops", "voice", "real_time"],
    "personalities": ["elder_brother", "friend", "teacher", "doctor", "engineer", "guard", "coach", "professional"]
  },
  "proxy": {
    "port": 8080,
    "host": "0.0.0.0",
    "intercept_endpoints": ["api.openai.com", "api.anthropic.com", "api.together.xyz"]
  },
  "multi_project": {
    "port": 8081,
    "host": "0.0.0.0",
    "config_file": "data/multi_project_config.json"
  },
  "ollama": {
    "url": "http://localhost:11434",
    "timeout": 30,
    "models": ["llama3.2:1b", "qwen2.5-coder:1.5b-base", "codellama:latest"]
  },
  "cloud_fallback": {
    "enabled": true,
    "providers": ["openrouter", "together", "huggingface"],
    "api_keys": {
      "openrouter": "your_openrouter_key",
      "together": "your_together_key"
    }
  }
}
```

### Cursor Configuration (`cursor-config.json`)
```json
{
  "cursor": {
    "forceLocal": true,
    "proxyUrl": "http://localhost:8080",
    "localAgent": "ZombieCoder Agent (সাহন ভাই)",
    "cloudBypass": {
      "authentication": false,
      "apiLimits": false,
      "telemetry": false,
      "cloudAI": false
    }
  }
}
```

## 🧪 Testing

### System Health Check
```bash
# Test all services
python TEST_PROXY.py

# Test extension functionality
cd extension
node test-extension.js
```

### Manual Testing
```bash
# Test Main Server
curl http://localhost:12345/api/status

# Test Proxy Server
curl http://localhost:8080/proxy/status

# Test Multi-Project API
curl http://localhost:8081/api/projects/status
```

### VS Code Extension Testing
1. Open VS Code
2. Press `Ctrl+Shift+P`
3. Type "ZombieCoder: Show Status"
4. Check status bar for indicators

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Windows
netstat -ano | findstr :12345
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :12345
kill -9 <PID>
```

#### 2. Ollama Connection Error
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

#### 3. Python Dependencies Error
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

#### 4. Extension Not Working
```bash
# Check VS Code logs
# Help > Toggle Developer Tools > Console

# Reinstall extension
# Extensions > ZombieCoder Force Local > Uninstall > Install
```

#### 5. Memory Issues
```bash
# Check available memory
# Windows: Task Manager
# macOS: Activity Monitor
# Linux: htop

# Reduce model size or close other applications
```

### Performance Optimization

#### 1. Model Selection
```bash
# Use smaller models for faster response
ollama pull llama3.2:1b  # Fast, ~2GB
ollama pull qwen2.5-coder:1.5b-base  # Balanced, ~3GB
ollama pull codellama:latest  # Comprehensive, ~7GB
```

#### 2. System Tuning
```bash
# Increase swap space (Linux/macOS)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 3. Network Optimization
```bash
# Use local models when possible
# Configure cloud fallback only when needed
# Monitor network usage
```

## 📊 Monitoring

### Log Files
- **Main Server**: `logs/main_server.log`
- **Proxy Server**: `logs/proxy_server.log`
- **Multi-Project API**: `logs/multi_project_api.log`
- **Extension**: VS Code Developer Tools

### Status Monitoring
```bash
# Real-time status
watch -n 5 'curl -s http://localhost:12345/api/status | jq'

# Performance metrics
curl http://localhost:12345/api/performance
```

### Health Checks
```bash
# Automated health check script
python scripts/health_check.py
```

## 🔒 Security

### Best Practices
1. **Keep API keys secure**: Store in `.env` file, never commit to git
2. **Regular updates**: Update dependencies regularly
3. **Network security**: Use HTTPS in production
4. **Access control**: Limit access to localhost in development
5. **Log monitoring**: Monitor logs for suspicious activity

### Production Deployment
```bash
# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:12345 our-server.main_server:app

# Use reverse proxy (nginx)
# Configure SSL certificates
# Set up monitoring and alerting
```

## 📚 Additional Resources

### Documentation
- [System Overview](SYSTEM_OVERVIEW.md)
- [Agent Descriptions](AGENT_DESCRIPTIONS.md)
- [Contribution Guide](CONTRIBUTION_GUIDE.md)

### Support
- **GitHub Issues**: [Report bugs](https://github.com/devsahon/ZombieCoder-Agent-Personal/issues)
- **Discussions**: [Community support](https://github.com/devsahon/ZombieCoder-Agent-Personal/discussions)
- **Documentation**: [Full documentation](https://github.com/devsahon/ZombieCoder-Agent-Personal/tree/main/docs)

### Community
- **Discord**: Join our community server
- **Telegram**: Follow for updates
- **YouTube**: Tutorial videos and demos

---

**🎉 Congratulations!** You've successfully set up ZombieCoder Agent Personal. Start coding with your new AI assistant!

**📝 Note**: If you encounter any issues, please check the troubleshooting section or create an issue on GitHub.
