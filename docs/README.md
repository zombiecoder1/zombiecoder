# 🤖 Shaon AI Advanced System v3.0

> **"যেখানে কোড ও কথা বলে, পরিবারের মত সহায়তা করে"**

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/devsahon/ZombieCoder-Agent-Personal)
[![Branch](https://img.shields.io/badge/branch-alhamdullha--advanced--system-green.svg)](https://github.com/devsahon/ZombieCoder-Agent-Personal/tree/alhamdullha-advanced-system)
[![Python](https://img.shields.io/badge/python-3.11+-yellow.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org)

## 🎯 Overview

**Shaon AI Advanced System v3.0** is a comprehensive local AI-powered development assistant that combines multiple AI agents with advanced features like Lazy Loading, Memory Management, Smart Routing, and VSCode integration.

### 🌟 Key Features

- **🤖 5 AI Agents** with unique personalities and 10 capabilities each
- **⚡ Lazy Loading** for optimal performance
- **💾 Memory Management** with automatic cleanup
- **🧠 Smart Routing** with cloud fallback
- **🔌 VSCode Extension** with Copilot integration
- **📊 Multi-Project API** support
- **📈 Real-time Status Monitoring**

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Shaon AI Advanced System                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   VSCode    │  │   Browser   │  │   Terminal  │         │
│  │ Extension   │  │   Interface │  │   Commands  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                    Proxy Server (Port 8080)                │
│                    Smart Routing & Load Balancing           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Advanced   │  │   Multi-    │  │   Cloud     │         │
│  │   Agent     │  │  Project    │  │  Fallback   │         │
│  │  System     │  │    API      │  │  Providers  │         │
│  │ (Port 12345)│  │(Port 8081)  │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                    Local AI (Ollama)                       │
│                    Models: llama3.2:1b, qwen2.5-coder, etc.│
└─────────────────────────────────────────────────────────────┘
```

## 🤖 AI Agents

### 👨‍💻 সাহন ভাই (Elder Brother)
- **Role**: Technical advisor and mentor
- **Expertise**: Coding, debugging, system architecture
- **Capabilities**: Code review, performance optimization, security audit

### 👧 মুসকান (Creative Specialist)
- **Role**: Frontend and creative development
- **Expertise**: UI/UX, frontend development, creative coding
- **Capabilities**: Responsive design, animations, modern frameworks

### 👩‍💼 ভাবি (Backend Specialist)
- **Role**: Backend and database management
- **Expertise**: Database design, API development, security
- **Capabilities**: Data modeling, microservices, system integration

### 🐯 বাঘ (Security Specialist)
- **Role**: Security and performance optimization
- **Expertise**: Security audit, penetration testing, system hardening
- **Capabilities**: Threat hunting, cryptography, incident response

### 🔍 হান্টার (Quality Specialist)
- **Role**: Quality assurance and debugging
- **Expertise**: Bug hunting, code review, quality assurance
- **Capabilities**: Automated testing, performance profiling, code analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama (with models: `llama3.2:1b`, `qwen2.5-coder:1.5b-base`)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/devsahon/ZombieCoder-Agent-Personal.git
cd ZombieCoder-Agent-Personal

# 2. Switch to advanced branch
git checkout alhamdullha-advanced-system

# 3. Install dependencies
pip install -r config/requirements.txt
cd shaon-extension && npm install

# 4. Start system
./GLOBAL_LAUNCHER.bat
```

### Manual Setup

```bash
# Start Advanced Agent System
python core-server/advanced_agent_system.py

# Start Proxy Server
python optimized_port_routing.py

# Start Multi-Project API
python our-server/multi_project_api.py
```

## 📖 Usage

### Terminal Usage
```bash
# Chat with specific agent
curl -X POST http://localhost:12345/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a Python function", "agent": "সাহন ভাই"}'

# Check system status
curl http://localhost:12345/status
```

### Browser Usage
- **Advanced Agent System**: http://localhost:12345
- **Proxy Server**: http://localhost:8080
- **Multi-Project API**: http://localhost:8081

### VSCode Usage
1. Install extension: `code --install-extension shaon-zombiecoder-extension-1.0.0.vsix`
2. Press `Ctrl+Shift+P`
3. Type "Shaon: Copilot Chat"
4. Select agent and start chatting

## 🔌 API Reference

### Advanced Agent System (Port 12345)

#### POST `/chat`
Chat with AI agents
```json
{
  "message": "Your message here",
  "agent": "সাহন ভাই"
}
```

#### GET `/status`
Get system status
```json
{
  "system": "ZombieCoder Advanced Agent System",
  "agents": {...},
  "system_status": {...},
  "memory_stats": {...}
}
```

#### GET `/info`
Get system information
```json
{
  "name": "ZombieCoder Advanced Agent System",
  "version": "3.0.0",
  "features": [...],
  "agents": [...]
}
```

## 🧠 Smart Features

### Lazy Loading
- Agent personalities load only when needed
- Reduces memory usage and startup time
- Automatic performance optimization

### Memory Management
- Automatic cleanup every 5 minutes
- History management (last 100 conversations)
- Cache management (maximum 50 entries)
- Real-time performance monitoring

### Smart Routing
- Complex prompt detection
- Automatic cloud fallback
- Intelligent provider selection
- Performance-based routing

## 🔧 Configuration

### Environment Setup
```bash
# Install Ollama models
ollama pull llama3.2:1b
ollama pull qwen2.5-coder:1.5b-base
ollama pull codellama:latest
ollama pull llama3.1:8b
```

### API Keys (Optional)
Edit `our-server/config.json`:
```json
{
  "cloud_fallback": {
    "api_keys": {
      "openrouter": "your_openrouter_key",
      "together": "your_together_key",
      "huggingface": "your_huggingface_key",
      "anthropic": "your_anthropic_key"
    }
  }
}
```

## 📊 Monitoring

### Real-time Status
```bash
# Monitor system status
watch -n 5 'curl -s http://localhost:12345/status | jq'

# Monitor memory usage
watch -n 10 'curl -s http://localhost:12345/status | jq .memory_stats'
```

### Log Files
- **Advanced Agent System**: `core-server/logs/`
- **Proxy Server**: `proxy-server/logs/`
- **Multi-Project API**: `our-server/logs/`

## 🔧 Troubleshooting

### Common Issues

#### Ollama Connection Error
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

#### Port Already in Use
```bash
# Find process using port
netstat -ano | findstr :12345

# Kill process
taskkill /PID <PID> /F
```

#### VSCode Extension Not Working
```bash
# Rebuild extension
cd shaon-extension
npm run build:extension

# Reinstall extension
code --install-extension shaon-zombiecoder-extension-1.0.0.vsix
```

## 📁 Project Structure

```
D:\Alhamdullha\
├── core-server/
│   ├── advanced_agent_system.py    # Main AI system
│   ├── memory_manager.py           # Memory management
│   └── agents/                     # Agent personalities
├── our-server/
│   ├── ai_providers.py             # Cloud fallback providers
│   ├── multi_project_api.py        # Multi-project API
│   └── config.json                 # Configuration
├── shaon-extension/
│   ├── src/                        # VSCode extension source
│   ├── dist/                       # Compiled extension
│   └── package.json                # Extension configuration
├── optimized_port_routing.py       # Proxy server
├── GLOBAL_LAUNCHER.bat             # System launcher
├── power-switch.bat                # Power management
└── SYSTEM_DOCUMENTATION.md         # Complete documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama** for local AI models
- **VSCode** for extension platform
- **Flask** for web framework
- **Next.js** for extension UI

## 📞 Support

- **Repository**: https://github.com/devsahon/ZombieCoder-Agent-Personal
- **Branch**: `alhamdullha-advanced-system`
- **Documentation**: [SYSTEM_DOCUMENTATION.md](SYSTEM_DOCUMENTATION.md)

---

## 🎉 Features Summary

| Feature | Status | Description |
|---------|--------|-------------|
| 🤖 5 AI Agents | ✅ | Unique personalities with 10 capabilities each |
| ⚡ Lazy Loading | ✅ | Performance optimization |
| 💾 Memory Management | ✅ | Automatic cleanup and monitoring |
| 🧠 Smart Routing | ✅ | Complex prompt detection and cloud fallback |
| 🔌 VSCode Extension | ✅ | Copilot-style integration |
| 📊 Multi-Project API | ✅ | Project management and tracking |
| 🌐 Cloud Fallback | ✅ | Multiple provider support |
| 📈 Real-time Monitoring | ✅ | Status and performance tracking |

---

*Last Updated: August 24, 2025*  
*Version: 3.0.0*  
*Branch: alhamdullha-advanced-system*
