# 🏗️ ZombieCoder Architecture & Setup Guide

## 🎯 Server Architecture Overview

```
Cursor UI → Proxy (8080) → Agent System (8004) → Memory + Logic
             ↳ Truth Checker (8002) → Validation
             ↳ Multi-Project Manager (8001) → Context Split
             ↳ Editor Integration (8003) → File/IDE Sync
             ↳ Ollama (11434) → Model Core
Main Server (12345) → Orchestration
```

## 📊 Setup Comparison Table

| Setup Type | Servers Required | Use Case | Response Quality | Features |
|------------|------------------|----------|------------------|----------|
| **🔴 Basic Chat** | Ollama (11434) + Proxy (8080) | Simple Q&A | Raw Model Response | ❌ No memory, ❌ No context, ❌ No validation |
| **🟡 Smart Chat** | + Agent System (8004) | Intelligent responses | Context-aware | ✅ Memory, ✅ Role handling, ✅ Logic |
| **🟢 Production** | + Truth Checker (8002) | Factual responses | Validated responses | ✅ Fact-checking, ✅ Hallucination reduction |
| **🔵 Full IDE** | + Editor Integration (8003) | Code assistance | IDE-aware | ✅ File sync, ✅ Context enrichment |
| **🟣 Multi-Project** | + Multi-Project Manager (8001) | Project management | Project-specific | ✅ Memory split, ✅ Context isolation |
| **⚡ Complete** | + Main Server (12345) | Full automation | Production-ready | ✅ Orchestration, ✅ All features |

## 🚀 Quick Setup Commands

### 🔴 Basic Chat Setup (Minimum)
```bash
# Start Ollama
ollama serve

# Start Proxy
cd /home/sahon/Desktop/zombiecoder
source zombie_env/bin/activate
python3 cursor_proxy_interceptor.py
```
**Result:** Raw model responses, no intelligence

### 🟡 Smart Chat Setup
```bash
# Start Ollama + Proxy + Agent System
./GLOBAL_LAUNCHER.sh
# Then manually start Agent System:
cd core-server && python3 advanced_agent_system.py
```
**Result:** Intelligent responses with memory and role handling

### 🟢 Production Setup
```bash
# Start all services
./GLOBAL_LAUNCHER.sh
```
**Result:** All services running with validation and fact-checking

## 📋 Server Responsibilities

### 🎯 Core Servers

| Server | Port | Purpose | Required For |
|--------|------|---------|--------------|
| **Ollama** | 11434 | Model execution | All setups |
| **Proxy** | 8080 | Request interception | All setups |

### 🧠 Intelligence Servers

| Server | Port | Purpose | Required For |
|--------|------|---------|--------------|
| **Agent System** | 8004 | Memory, Logic, Role handling | Smart Chat+ |
| **Truth Checker** | 8002 | Fact validation, Hallucination reduction | Production+ |
| **Multi-Project Manager** | 8001 | Context splitting, Memory isolation | Multi-Project+ |
| **Editor Integration** | 8003 | File sync, IDE context | Full IDE+ |
| **Main Server** | 12345 | Orchestration, Coordination | Complete setup |

## 🔧 Configuration Examples

### Basic Chat Configuration
```json
{
  "servers": ["ollama", "proxy"],
  "features": ["raw_responses"],
  "use_case": "simple_qa"
}
```

### Smart Chat Configuration
```json
{
  "servers": ["ollama", "proxy", "agent_system"],
  "features": ["memory", "role_handling", "context_awareness"],
  "use_case": "intelligent_chat"
}
```

### Production Configuration
```json
{
  "servers": ["ollama", "proxy", "agent_system", "truth_checker"],
  "features": ["memory", "validation", "fact_checking"],
  "use_case": "production_chat"
}
```

### Full IDE Configuration
```json
{
  "servers": ["ollama", "proxy", "agent_system", "truth_checker", "editor_integration"],
  "features": ["memory", "validation", "file_sync", "ide_context"],
  "use_case": "code_assistance"
}
```

### Complete Configuration
```json
{
  "servers": ["ollama", "proxy", "agent_system", "truth_checker", "editor_integration", "multi_project", "main_server"],
  "features": ["all"],
  "use_case": "full_automation"
}
```

## 🎯 Use Case Scenarios

### Scenario 1: Quick Testing
**Setup:** Basic Chat
**Servers:** Ollama + Proxy
**Use:** Test if Cursor integration works
**Response:** Raw model output

### Scenario 2: Daily Coding
**Setup:** Smart Chat
**Servers:** Ollama + Proxy + Agent System
**Use:** Intelligent code assistance
**Response:** Context-aware, memory-enabled

### Scenario 3: Production Work
**Setup:** Production
**Servers:** + Truth Checker
**Use:** Factual, validated responses
**Response:** Hallucination-reduced, fact-checked

### Scenario 4: Multi-Project Development
**Setup:** Full IDE
**Servers:** + Editor Integration + Multi-Project Manager
**Use:** Project-specific assistance
**Response:** IDE-aware, project-isolated

### Scenario 5: Enterprise Automation
**Setup:** Complete
**Servers:** All servers
**Use:** Full automation, orchestration
**Response:** Production-ready, fully orchestrated

## 🚨 Common Issues & Solutions

### Issue: "Model giving random responses"
**Cause:** Basic Chat setup (no Agent System)
**Solution:** Start Agent System (port 8004)

### Issue: "Model hallucinating facts"
**Cause:** No Truth Checker
**Solution:** Start Truth Checker (port 8002)

### Issue: "Model not understanding file context"
**Cause:** No Editor Integration
**Solution:** Start Editor Integration (port 8003)

### Issue: "Model confusing between projects"
**Cause:** No Multi-Project Manager
**Solution:** Start Multi-Project Manager (port 8001)

## 📊 Performance Impact

| Setup | Memory Usage | CPU Usage | Response Time | Quality |
|-------|--------------|-----------|---------------|---------|
| Basic Chat | Low | Low | Fast | Poor |
| Smart Chat | Medium | Medium | Medium | Good |
| Production | High | High | Slow | Excellent |
| Full IDE | Very High | Very High | Very Slow | Outstanding |
| Complete | Maximum | Maximum | Slowest | Perfect |

## 🎯 Recommendations

### For Development:
- **Start with:** Smart Chat (Ollama + Proxy + Agent System)
- **Add when needed:** Truth Checker for factual work
- **Add for coding:** Editor Integration

### For Production:
- **Minimum:** Production setup (all except Main Server)
- **Recommended:** Complete setup (all servers)

### For Testing:
- **Start with:** Basic Chat
- **Upgrade as needed:** Add servers incrementally

## 🔄 Dynamic Server Management

### Start Specific Servers:
```bash
# Start only what you need
cd core-server && python3 advanced_agent_system.py &
cd core-server && python3 truth_checker.py &
cd core-server && python3 editor_integration.py &
cd core-server && python3 multi_project_manager.py &
```

### Stop Specific Servers:
```bash
# Stop specific services
pkill -f "advanced_agent_system.py"
pkill -f "truth_checker.py"
pkill -f "editor_integration.py"
pkill -f "multi_project_manager.py"
```

### Check Server Status:
```bash
# Check which servers are running
ps aux | grep -E "(ollama|proxy|agent|truth|editor|multi)" | grep -v grep
```

---

**Status:** 🟢 Ready for Production
**Last Updated:** $(date)
**Next Step:** Choose your setup based on use case
