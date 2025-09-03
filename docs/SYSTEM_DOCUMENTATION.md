# 🤖 Shaon AI Advanced System v3.0 - Complete Documentation

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Components](#components)
4. [Agent System](#agent-system)
5. [Smart Routing](#smart-routing)
6. [Memory Management](#memory-management)
7. [VSCode Extension](#vscode-extension)
8. [Installation & Setup](#installation--setup)
9. [Usage Guide](#usage-guide)
10. [API Reference](#api-reference)
11. [Troubleshooting](#troubleshooting)

---

## 🎯 System Overview

**Shaon AI Advanced System v3.0** is a comprehensive local AI-powered development assistant that combines multiple AI agents with advanced features like Lazy Loading, Memory Management, Smart Routing, and VSCode integration.

### 🌟 Key Features

- **5 AI Agents** with unique personalities and 10 capabilities each
- **Lazy Loading** for optimal performance
- **Memory Management** with automatic cleanup
- **Smart Routing** with cloud fallback
- **VSCode Extension** with Copilot integration
- **Multi-Project API** support
- **Real-time Status Monitoring**

---

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

---

## 🔧 Components

### 1. **Advanced Agent System** (`core-server/advanced_agent_system.py`)

- **Port**: 12345
- **Purpose**: Main AI processing engine
- **Features**:
  - 5 AI agents with unique personalities
  - Lazy loading for performance
  - Memory management
  - Smart routing with cloud fallback

### 2. **Proxy Server** (`optimized_port_routing.py`)

- **Port**: 8080
- **Purpose**: Smart routing and load balancing
- **Features**:
  - Request routing to appropriate services
  - Status monitoring
  - CORS handling

### 3. **Multi-Project API** (`our-server/multi_project_api.py`)

- **Port**: 8081
- **Purpose**: Multi-project management
- **Features**:
  - Project tracking
  - File management
  - Development statistics

### 4. **VSCode Extension** (`shaon-extension/`)

- **Purpose**: Editor integration
- **Features**:
  - Copilot-style chat (`Ctrl+Shift+P`)
  - Status bar indicator
  - Real-time agent communication

---

## 🤖 Agent System

### Agent Personalities

#### 1. **সাহন ভাই** 👨‍💻

- **Role**: Elder brother and technical advisor
- **Expertise**: Coding, debugging, system architecture
- **Capabilities**:
  1. কোড রিভিউ এবং অপটিমাইজেশন
  2. সিস্টেম আর্কিটেকচার ডিজাইন
  3. ডিবাগিং এবং ট্রাবলশুটিং
  4. পারফরম্যান্স অপটিমাইজেশন
  5. সিকিউরিটি অডিট
  6. কোডিং বেস্ট প্র্যাকটিস
  7. প্রজেক্ট ম্যানেজমেন্ট
  8. টেকনিক্যাল কনসালটেশন
  9. মেন্টরশিপ এবং গাইডেন্স
  10. প্রবলেম সলভিং

#### 2. **মুসকান** 👧

- **Role**: Creative frontend specialist
- **Expertise**: Frontend development, UI/UX, creative coding
- **Capabilities**:
  1. ফ্রন্টএন্ড ডেভেলপমেন্ট
  2. UI/UX ডিজাইন
  3. ক্রিয়েটিভ কোডিং
  4. অ্যানিমেশন এবং ইন্টারেকশন
  5. রেসপনসিভ ডিজাইন
  6. ফ্রন্টএন্ড অপটিমাইজেশন
  7. মডার্ন ফ্রেমওয়ার্ক
  8. ক্রস-ব্রাউজার কম্প্যাটিবিলিটি
  9. অ্যাক্সেসিবিলিটি
  10. ইউজার এক্সপেরিয়েন্স

#### 3. **ভাবি** 👩‍💼

- **Role**: Backend and database specialist
- **Expertise**: Database, API development, security
- **Capabilities**:
  1. ডাটাবেস ডিজাইন এবং অপটিমাইজেশন
  2. API ডেভেলপমেন্ট
  3. ডাটা মডেলিং
  4. ব্যাকএন্ড সিকিউরিটি
  5. ডাটা ইন্টিগ্রিটি
  6. স্কেলেবল আর্কিটেকচার
  7. মাইক্রোসার্ভিস
  8. ডাটা ব্যাকআপ এবং রিকভারি
  9. ডাটা অ্যানালিটিক্স
  10. সিস্টেম ইন্টিগ্রেশন

#### 4. **বাঘ** 🐯

- **Role**: Security and performance specialist
- **Expertise**: Security, performance, system optimization
- **Capabilities**:
  1. সিকিউরিটি অডিট এবং পেনিট্রেশন টেস্টিং
  2. সিস্টেম পারফরম্যান্স অপটিমাইজেশন
  3. নেটওয়ার্ক সিকিউরিটি
  4. ম্যালওয়্যার অ্যানালাইসিস
  5. ইনসিডেন্ট রেসপন্স
  6. সিকিউরিটি আর্কিটেকচার
  7. ক্রিপ্টোগ্রাফি
  8. সিস্টেম হার্ডেনিং
  9. থ্রেট হান্টিং
  10. সিকিউরিটি কমপ্লায়েন্স

#### 5. **হান্টার** 🔍

- **Role**: Quality assurance and debugging specialist
- **Expertise**: Bug hunting, code review, quality assurance
- **Capabilities**:
  1. বাগ হান্টিং এবং ডিবাগিং
  2. কোড কোয়ালিটি অ্যাসুরেন্স
  3. অটোমেটেড টেস্টিং
  4. কোড রিভিউ এবং অ্যানালাইসিস
  5. পারফরম্যান্স প্রোফাইলিং
  6. মেমরি লিক ডিটেকশন
  7. কোড কমপ্লেক্সিটি অ্যানালাইসিস
  8. টেস্ট কভারেজ অ্যানালাইসিস
  9. কোড স্ট্যাটিক অ্যানালাইসিস
  10. কোয়ালিটি মেট্রিক্স

---

## 🧠 Smart Routing

### Complex Prompt Detection

The system automatically detects complex prompts and routes them to cloud providers:

```python
def _is_complex_prompt(self, prompt: str) -> bool:
    complex_keywords = [
        'analyze', 'review', 'optimize', 'debug', 'security', 'performance',
        'architecture', 'design', 'complex', 'advanced', 'sophisticated',
        'critical', 'important', 'urgent', 'production', 'enterprise'
    ]

    prompt_lower = prompt.lower()
    complexity_score = sum(1 for keyword in complex_keywords if keyword in prompt_lower)

    return complexity_score >= 2 or len(prompt) > 500
```

### Routing Flow

1. **Simple Prompts** → Local AI (Ollama)
2. **Complex Prompts** → Cloud Fallback → Local AI
3. **Local AI Failure** → Cloud Fallback
4. **All Failures** → Fallback Response

---

## 💾 Memory Management

### Features

- **Automatic Cleanup**: Every 5 minutes
- **History Management**: Last 100 conversations
- **Cache Management**: Maximum 50 entries
- **Garbage Collection**: Forced cleanup
- **Performance Monitoring**: Real-time stats

### Memory Stats

```json
{
  "memory_mb": 45.2,
  "cache_size": 12,
  "history_size": 25,
  "cpu_percent": 2.1
}
```

---

## 🔌 VSCode Extension

### Installation

```bash
# Install the extension
code --install-extension shaon-zombiecoder-extension-1.0.0.vsix
```

### Features

- **Copilot Chat**: `Ctrl+Shift+P` → "Shaon: Copilot Chat"
- **Status Bar**: Real-time system status indicator
- **Agent Selection**: Choose from 5 agents
- **Code Analysis**: Right-click → "Shaon: Analyze Code"

### Status Indicators

- 🔴 **Inactive**: System not running
- 🟡 **Loading**: System starting up
- 🟢 **Active**: System ready
- ⚠️ **Error**: System error

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Ollama (with models: llama3.2:1b, qwen2.5-coder:1.5b-base)

### Quick Start

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

---

## 📖 Usage Guide

### 1. **Terminal Usage**

```bash
# Test chat with specific agent
curl -X POST http://localhost:12345/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a Python function", "agent": "সাহন ভাই"}'

# Check system status
curl http://localhost:12345/status
```

### 2. **Browser Usage**

- **Advanced Agent System**: http://localhost:12345
- **Proxy Server**: http://localhost:8080
- **Multi-Project API**: http://localhost:8081

### 3. **VSCode Usage**

1. Install extension
2. Press `Ctrl+Shift+P`
3. Type "Shaon: Copilot Chat"
4. Select agent and start chatting

### 4. **Power Switch**

```bash
# Use the power switch for easy management
./power-switch.bat
```

---

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

### Proxy Server (Port 8080)

#### GET `/proxy/status`

Get proxy status

```json
{
  "local_agent": "ZombieCoder Agent (সাহন ভাই)",
  "proxy": "cursor",
  "status": "active"
}
```

### Multi-Project API (Port 8081)

#### GET `/api/projects/status`

Get project status

```json
{
  "active_project": null,
  "stats": {...},
  "status": "active"
}
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. **Ollama Connection Error**

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

#### 2. **Port Already in Use**

```bash
# Find process using port
netstat -ano | findstr :12345

# Kill process
taskkill /PID <PID> /F
```

#### 3. **VSCode Extension Not Working**

```bash
# Rebuild extension
cd shaon-extension
npm run build:extension

# Reinstall extension
code --install-extension shaon-zombiecoder-extension-1.0.0.vsix
```

#### 4. **Cloud Fallback Not Working**

- Check API keys in `our-server/config.json`
- Verify cloud provider credits
- Check network connectivity

### Performance Optimization

#### 1. **Memory Issues**

- System automatically manages memory
- Manual cleanup: Restart services
- Monitor with `/status` endpoint

#### 2. **Slow Responses**

- Check Ollama model loading
- Verify local AI connection
- Monitor cloud fallback usage

#### 3. **High CPU Usage**

- Check background processes
- Monitor memory usage
- Restart services if needed

---

## 📊 System Monitoring

### Real-time Monitoring

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

---

## 🔄 Updates and Maintenance

### Regular Maintenance

1. **Daily**: Check system status
2. **Weekly**: Update dependencies
3. **Monthly**: Review and optimize performance

### Backup

```bash
# Backup configuration
cp our-server/config.json backup/config_$(date +%Y%m%d).json

# Backup logs
tar -czf backup/logs_$(date +%Y%m%d).tar.gz */logs/
```

---

## 📞 Support

### Getting Help

1. Check this documentation
2. Review troubleshooting section
3. Check system logs
4. Test individual components

### Contact

- **Repository**: https://github.com/devsahon/ZombieCoder-Agent-Personal
- **Branch**: `alhamdullha-advanced-system`

---

## 🎉 Conclusion

**Shaon AI Advanced System v3.0** provides a comprehensive, local AI-powered development environment with:

- ✅ **5 Specialized AI Agents** with unique capabilities
- ✅ **Advanced Performance Optimization** with lazy loading
- ✅ **Smart Routing** with cloud fallback
- ✅ **VSCode Integration** with Copilot-style chat
- ✅ **Real-time Monitoring** and status tracking
- ✅ **Multi-Project Support** for complex workflows

The system is designed to be **reliable**, **scalable**, and **user-friendly**, providing developers with powerful AI assistance while maintaining privacy and performance.

---

_Last Updated: August 24, 2025_
_Version: 3.0.0_
_Branch: alhamdullha-advanced-system_
