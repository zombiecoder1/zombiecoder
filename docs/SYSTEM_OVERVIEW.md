# 🤖 ZombieCoder Agent Personal - System Overview

## 🎯 Project Vision

**"যেখানে কোড ও কথা বলে"** - Where code and conversation meet.

A comprehensive, privacy-focused AI development environment that provides seamless local AI assistance without cloud dependencies.

## 🏗️ Architecture Overview

### Core Components

```
ZombieCoder Agent Personal
├── 🖥️ Main Server (Port 12345)
├── 📡 Proxy Server (Port 8080)
├── 🔄 Multi-Project API (Port 8081)
├── 🎯 VS Code Extension
└── 🤖 Unified AI Agent System
```

### 1️⃣ Main Server (`our-server/main_server.py`)
- **Port**: 12345
- **Purpose**: Core AI processing and agent management
- **Features**:
  - Unified agent system with 10 capabilities
  - Local Ollama model integration
  - Cloud fallback support
  - Memory management
  - Real-time status monitoring

### 2️⃣ Proxy Server (`our-server/proxy_server.py`)
- **Port**: 8080
- **Purpose**: Intercept Cursor API calls and redirect to local agent
- **Features**:
  - Cursor integration
  - API request interception
  - Response formatting
  - Cloud bypass

### 3️⃣ Multi-Project API (`our-server/multi_project_api.py`)
- **Port**: 8081
- **Purpose**: Dynamic project management and agent switching
- **Features**:
  - Project detection
  - Agent assignment
  - Shortcut key support
  - Context switching

### 4️⃣ VS Code Extension (`extension/`)
- **Purpose**: Editor integration and user interface
- **Features**:
  - Status bar indicators
  - Agent switching (Ctrl+Shift+1-8)
  - Cloud bypass
  - Real-time feedback

## 🤖 Agent System

### Unified Agent Architecture
Instead of multiple separate agents, we use a single **ZombieCoder Agent (সাহন ভাই)** with multiple personalities and capabilities:

#### 🎭 Agent Personalities
1. **ZombieCoder Agent (সাহন ভাই)** - Main AI Assistant
2. **DocMaster** - Documentation Expert
3. **BugHunter** - Debugging Specialist
4. **CloudFallback** - Cloud Support
5. **CodeArchitect** - System Designer
6. **SecurityGuard** - Security Expert
7. **PerformanceGuru** - Performance Optimizer
8. **DevOpsPilot** - DevOps Engineer

#### 🔧 Capabilities
1. **Coding** - Code generation, refactoring, optimization
2. **Debugging** - Error detection, fixing, logging
3. **Architecture** - System design, patterns, best practices
4. **Database** - Query optimization, schema design
5. **API** - REST/GraphQL development, testing
6. **Security** - Vulnerability scanning, authentication
7. **Performance** - Code optimization, benchmarking
8. **DevOps** - Deployment, CI/CD, automation
9. **Voice** - Voice command processing
10. **Real-time** - Live information, system status

## 🔄 Data Flow

### Request Flow
```
User Input → VS Code Extension → Proxy Server → Main Server → Local Agent → Response
```

### Fallback Flow
```
Local Agent (Timeout) → Cloud Providers → Response
```

## 🛡️ Security & Privacy

### Local-First Approach
- All processing happens locally by default
- No user data collection
- Cloud fallback only when necessary
- Complete offline capability

### Cloud Providers (Fallback)
- **OpenRouter**: Claude, Llama models
- **Together AI**: Open source models
- **HuggingFace**: Community models

## 📊 Performance Metrics

### Latency
- **Local Processing**: ~2-5 seconds
- **Cloud Fallback**: ~3-8 seconds
- **Status Updates**: Real-time

### Resource Usage
- **Memory**: ~2-4GB (depending on models)
- **CPU**: Moderate usage during processing
- **Storage**: ~15-20GB (including models)

## 🔧 Configuration

### Key Files
- `our-server/config.json` - Main configuration
- `cursor-config.json` - Cursor integration
- `extension/package.json` - Extension settings

### Environment Variables
- `OLLAMA_HOST` - Ollama server URL
- `OPENROUTER_API_KEY` - Cloud fallback key
- `TOGETHER_API_KEY` - Alternative cloud provider

## 🚀 Deployment

### One-Click Launch
```bash
# Windows
.\GLOBAL_LAUNCHER.bat

# Linux/Mac
./GLOBAL_LAUNCHER.sh
```

### Manual Launch
```bash
# 1. Main Server
python our-server/main_server.py

# 2. Proxy Server
python our-server/proxy_server.py

# 3. Multi-Project API
python our-server/multi_project_api.py
```

## 📈 Monitoring

### Health Checks
```bash
# Main Server
curl http://localhost:12345/api/status

# Proxy Server
curl http://localhost:8080/proxy/status

# Multi-Project API
curl http://localhost:8081/api/projects/status
```

### Status Indicators
- 🟢 **Active** - Server responding
- 🔴 **Inactive** - Server offline
- 💡 **Blink** - Processing request
- 📡 **Latency** - Response time

## 🔮 Future Enhancements

### Planned Features
1. **Multi-language Support** - Bengali, English, Hindi
2. **Voice Integration** - Speech-to-text and text-to-speech
3. **Advanced Caching** - Intelligent response caching
4. **Plugin System** - Extensible agent capabilities
5. **Mobile Support** - Android/iOS companion apps

### Scalability
- **Horizontal Scaling** - Multiple server instances
- **Load Balancing** - Request distribution
- **Microservices** - Component separation
- **Containerization** - Docker support

---

**📝 Note**: This system is designed for privacy and local processing. All modifications should follow the documentation guidelines in the `docs/` folder.
