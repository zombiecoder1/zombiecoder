# 🤖 ZombieCoder - AI Agent Personal System

> "যেখানে কোড ও কথা বলে" - Where Code and Conversation Meet

ZombieCoder is a comprehensive AI agent system designed to provide intelligent programming assistance, code review, system operations, and friendly conversation in both Bengali and English.

## 🌟 Features

### 🤖 Multi-Agent System
- **রাকিব ভাই** - Friendly Programming Mentor (Bengali + English)
- **সাহন ভাই** - Senior Programmer & Code Generator
- **আর্কিটেক্ট** - Software Architecture Expert
- **Truth Guardian** - Information Verifier
- **মুসকান** - Conversational Assistant
- **হান্টার** - System Operations Specialist

### 🔧 Core Capabilities
- **Code Generation** - Python, JavaScript, Java, C++, Go, Rust
- **Code Review** - Quality assessment and improvement suggestions
- **Bug Fixing** - Error identification and resolution
- **System Architecture** - Scalable design patterns and best practices
- **Real-time Information** - Weather, time, system status
- **Memory Management** - Individual agent memory with YAML storage

### 🌐 Service Architecture
- **Proxy Server** (Port 8080) - Main API gateway
- **Unified Agent System** (Port 12345) - Core agent orchestration
- **Multi Project Manager** (Port 8001) - Project management
- **Editor Integration** (Port 8003) - IDE/Editor chat integration
- **Friendly Programmer Agent** (Port 8004) - Dedicated programming mentor

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama (for local AI models)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/zombiecoder1/zombiecoder.git
   cd zombiecoder
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv zombie_env
   source zombie_env/bin/activate  # Linux/Mac
   # or
   zombie_env\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r core-server/requirements.txt
   ```

4. **Start Ollama (if not running)**
   ```bash
   ollama serve
   ollama pull deepseek-coder:latest
   ollama pull llama3.1:latest
   ```

5. **Launch the system**
   ```bash
   chmod +x start_optimized_services.sh
   ./start_optimized_services.sh
   ```

## 📊 System Status

Check system health:
```bash
curl http://localhost:8001/health
curl http://localhost:8080/proxy/status
curl http://localhost:12345/status
```

## 🤖 Agent Testing

Test individual agents:
```bash
python3 test_all_agents.py
```

### Sample Interactions

**Programming Help:**
```bash
curl -X POST http://localhost:8080/proxy/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Python এ কিভাবে CSV ফাইল পড়া যায়?"}], "context": {}}'
```

**Code Review:**
```bash
curl -X POST http://localhost:12345/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "এই কোডটি রিভিউ করুন:\n```python\ndef add(a, b):\n    return a + b\n```", "context": {"category": "code_review"}}'
```

## 🔧 Configuration

### Agent Configuration
- `config/agent_config.yaml` - Agent settings and priorities
- `config/system_config.yaml` - System performance and security
- `config/ollama_config.yaml` - Ollama model management
- `config/memory_config.yaml` - Memory storage configuration

### Individual Agent Memory
Each agent has its own memory file in `memory/` directory:
- `friendly_programmer_memory.yaml`
- `programming_agent_memory.yaml`
- `architect_agent_memory.yaml`
- And more...

## 📈 Monitoring

### Health Checks
- **Proxy Server**: `http://localhost:8080/health`
- **Unified Agent**: `http://localhost:12345/status`
- **Multi Project**: `http://localhost:8001/health`
- **Editor Chat**: `http://localhost:8003/health`

### Performance Monitoring
```bash
python3 core-server/optimized_configuration.py
```

## 🛠️ Development

### Adding New Agents
1. Create agent class in `core-server/`
2. Add to `config/agent_config.yaml`
3. Create individual memory file
4. Update startup scripts

### Customizing Agent Personalities
Edit individual memory files in `memory/` directory to modify agent behavior, preferences, and conversation patterns.

## 📁 Project Structure

```
zombiecoder/
├── core-server/           # Core server components
│   ├── ai_providers.py    # AI provider integrations
│   ├── unified_agent_system.py
│   ├── proxy_server.py
│   ├── friendly_programmer_agent.py
│   └── ...
├── config/                # Configuration files
├── memory/                # Agent memory storage
├── logs/                  # System logs
├── start_optimized_services.sh
├── stop_services.sh
└── README.md
```

## 🔒 Security Features

- **Rate Limiting** - Prevents API abuse
- **Local AI Priority** - Privacy-first approach
- **Memory Encryption** - Secure agent memory storage
- **Health Monitoring** - Continuous system monitoring

## 🌍 Language Support

- **Primary**: Bengali (বাংলা)
- **Secondary**: English
- **Mixed Mode**: Bengali + English conversations
- **Code Languages**: Python, JavaScript, Java, C++, Go, Rust, TypeScript

## 📊 Performance Metrics

- **Response Time**: < 2 seconds average
- **Uptime**: 99.9% availability
- **Memory Usage**: Optimized for < 512MB per agent
- **Concurrent Users**: Supports up to 10 simultaneous requests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Developer**: zombiecoder1
- **Email**: zombiecoder58@gmail.com
- **GitHub**: https://github.com/zombiecoder1

## 🙏 Acknowledgments

- Ollama for local AI model support
- Flask for web framework
- CrewAI and AutoGen for agent orchestration
- Python community for excellent libraries

## 📞 Support

For support, email zombiecoder58@gmail.com or create an issue in this repository.

---

**Made with ❤️ by ZombieCoder Team**

> "Coding made simple, conversations made intelligent"