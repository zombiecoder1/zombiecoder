# 🧟 ZombieCoder - Personal AI Linux System

A comprehensive local AI development system with multiple agents, editors integration, and cloud service blocking.

## 🌟 Features

### 🤖 AI Agents
- **Main Server**: Unified agent system with Bengali-English mixed language support
- **Advanced Agent System**: Multi-personality agents with lazy loading
- **Truth Checker**: Verifies local-only AI operation
- **Multi-Project Manager**: Dynamic project management and agent assignment

### 💻 Editor Integration
- **Cursor AI**: Automatic local AI integration
- **VS Code**: Extension-based integration
- **Proxy Server**: API interception and redirection

### 🔒 Security
- **Cloud Service Blocking**: Blocks OpenAI, Anthropic, Hugging Face
- **Local AI Only**: Complete offline operation
- **Network Isolation**: Prevents external AI calls

### 🎭 Agent Personalities
- সাহন ভাই (Elder Brother)
- মুসকান (Friend)
- ভাবি (Sister-in-law)
- পরিবার (Family)
- বাঘ (Hunter)
- হান্টার (Guard)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama (for local LLM)
- Linux system

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/devsahon/parsonal_ai_linux.git
cd parsonal_ai_linux
```

2. **Setup Python environment**
```bash
python3 -m venv zombie_env
source zombie_env/bin/activate
pip install -r core-server/requirements.txt
```

3. **Install Ollama**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2:7b
ollama pull deepseek-coder:1.3b
```

4. **Start Ollama**
```bash
ollama serve
```

5. **Launch complete system**
```bash
./COMPLETE_SYSTEM_LAUNCHER.sh
```

## 📡 Services

| Service | Port | Description |
|---------|------|-------------|
| Main Server | 12345 | Unified agent system |
| Proxy Server | 8080 | API interception |
| Multi-Project Manager | 8001 | Project management |
| Truth Checker | 8002 | Local AI verification |
| Editor Integration | 8003 | Editor setup |
| Advanced Agent System | 8004 | Multi-agent system |
| Ollama Server | 11434 | Local LLM |

## 🎯 Agent Capabilities

- **Editor**: Code editing and suggestions
- **Bug Hunter**: Error detection and fixing
- **Coding**: Code generation and completion
- **Debugging**: Problem solving and debugging
- **Frontend**: Web development
- **Architecture**: System design
- **Database**: Database management
- **API**: API development
- **Security**: Security analysis
- **Performance**: Optimization
- **DevOps**: Deployment and operations
- **Testing**: Test automation
- **Voice**: Voice processing
- **Real-time**: Real-time systems

## 🔧 Management Commands

```bash
# Start all services
./COMPLETE_SYSTEM_LAUNCHER.sh

# Check system status
./SYSTEM_CHECKER.sh

# Stop all services
pkill -f 'python3.*zombiecoder'

# View logs
tail -f logs/*.log

# Open dashboard
xdg-open all.html
```

## 📊 System Status

- **Success Rate**: 100%
- **All Services**: Running
- **Cloud Services**: Blocked
- **Trust Verification**: Active

## 🌐 Available Endpoints

### Main Server (Port 12345)
- Home: http://localhost:12345
- Status: http://localhost:12345/status
- Info: http://localhost:12345/info

### Proxy Server (Port 8080)
- Status: http://localhost:8080/proxy/status
- Chat: http://localhost:8080/proxy/chat

### Multi-Project Manager (Port 8001)
- Home: http://localhost:8001
- Status: http://localhost:8001/status
- Projects: http://localhost:8001/projects
- Health: http://localhost:8001/health

### Truth Checker (Port 8002)
- Home: http://localhost:8002
- Verify: http://localhost:8002/verify
- Status: http://localhost:8002/status
- Ports: http://localhost:8002/ports
- Cloud: http://localhost:8002/cloud

### Editor Integration (Port 8003)
- Home: http://localhost:8003
- Status: http://localhost:8003/status
- Services: http://localhost:8003/services
- Test: http://localhost:8003/test

### Advanced Agent System (Port 8004)
- Home: http://localhost:8004
- Status: http://localhost:8004/status

### Ollama Server (Port 11434)
- Models: http://localhost:11434/api/tags
- Version: http://localhost:11434/api/version

## 🔒 Security Features

### Cloud Service Blocking
The system automatically blocks access to:
- api.openai.com
- api.anthropic.com
- huggingface.co
- models.openai.com

### Local AI Only
- All AI operations performed locally
- No external API calls
- Complete privacy and security

## 📁 Project Structure

```
zombiecoder/
├── core-server/                 # Main server components
│   ├── unified_agent_system.py  # Main agent system
│   ├── proxy_server.py          # API proxy
│   ├── multi_project_manager.py # Project management
│   ├── advanced_agent_system.py # Advanced agents
│   └── requirements.txt         # Python dependencies
├── local_ai_integration/        # Editor integration
│   ├── truth_checker.py         # Trust verification
│   └── editor_integration.py    # Editor setup
├── shaon-extension/             # VS Code extension
├── logs/                        # Service logs
├── COMPLETE_SYSTEM_LAUNCHER.sh  # Main launcher
├── SYSTEM_CHECKER.sh           # Status checker
├── all.html                     # Dashboard
└── README.md                    # This file
```

## 🎨 Dashboard

Access the comprehensive dashboard at `all.html` to view:
- Real-time service status
- Latency information
- Agent capabilities
- Security status
- Quick actions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**সাহন ভাই (Sahon Bhai)**
- Email: devsahonsrabon@gmail.com
- GitHub: [@devsahon](https://github.com/devsahon)

## 🙏 Acknowledgments

- Ollama team for local LLM support
- Flask community for web framework
- Open source AI community

---

**🧟 ZombieCoder - Your Local AI Family Assistant**

*Status: FULLY OPERATIONAL (100% Success Rate) - All Systems Running*
