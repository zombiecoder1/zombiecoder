# 🤝 Contribution Guide - ZombieCoder Agent Personal

## 🚫 Project Organization Guardrails

### ⚠️ IMPORTANT: Read Before Contributing

**🚫 Direct modification not allowed. Please read docs/ first.**

This project follows strict organization rules to maintain code quality and system stability. Before making any changes, you MUST:

1. **Read all documentation** in the `docs/` folder
2. **Understand the architecture** and component relationships
3. **Follow the contribution guidelines** below
4. **Test your changes** thoroughly
5. **Get approval** for major modifications

### 📁 Project Structure Rules

```
ZombieCoder-Agent-Personal/
├── 📜 README.md              # Main project documentation
├── our-server/               # Core AI Servers (DO NOT MODIFY STRUCTURE)
│   ├── main_server.py        # Main AI server
│   ├── proxy_server.py       # Cursor proxy
│   ├── multi_project_api.py  # Project manager
│   ├── unified_agent_system.py # Unified agent logic
│   ├── ai_providers.py       # Cloud fallback
│   └── config.json           # Configuration
├── extension/                # VS Code Extension (DO NOT MODIFY STRUCTURE)
│   ├── force-local-extension.js
│   ├── package.json
│   └── test-extension.js
├── docs/                     # 📜 Documentation (MUST READ)
│   ├── SYSTEM_OVERVIEW.md
│   ├── AGENT_DESCRIPTIONS.md
│   ├── SETUP_GUIDE.md
│   └── CONTRIBUTION_GUIDE.md
├── data/                     # Data storage
├── logs/                     # System logs
├── tests/                    # Test files
├── requirements.txt          # Python dependencies
└── GLOBAL_LAUNCHER.bat       # One-click launcher
```

### 🚫 Forbidden Actions

1. **Creating new folders** without documentation
2. **Modifying server structure** without approval
3. **Adding new agents** without updating documentation
4. **Changing configuration** without testing
5. **Removing documentation** files
6. **Breaking existing functionality** without fallback

## 🎯 Contribution Guidelines

### 1️⃣ Code Quality Standards

#### Python Code
```python
# ✅ Good Example
def process_message(message: str, agent: str = "default") -> Dict[str, Any]:
    """
    Process user message with specified agent.
    
    Args:
        message: User input message
        agent: Agent to use for processing
        
    Returns:
        Dictionary containing response and metadata
    """
    try:
        # Implementation
        return {"response": "Success", "agent": agent}
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return {"error": str(e)}
```

#### JavaScript Code
```javascript
// ✅ Good Example
/**
 * Process text with local AI agent
 * @param {string} text - Input text to process
 * @param {string} agent - Agent to use
 * @returns {Promise<Object>} Response object
 */
async function processWithLocalAI(text, agent = 'default') {
    try {
        const response = await sendToLocalProxy(text, agent);
        return { success: true, data: response };
    } catch (error) {
        console.error('Local AI error:', error);
        return { success: false, error: error.message };
    }
}
```

### 2️⃣ Documentation Requirements

#### For New Features
1. **Update System Overview** (`docs/SYSTEM_OVERVIEW.md`)
2. **Add Agent Descriptions** (`docs/AGENT_DESCRIPTIONS.md`)
3. **Update Setup Guide** (`docs/SETUP_GUIDE.md`)
4. **Create Test Cases** (`tests/`)

#### For Bug Fixes
1. **Document the Issue** in GitHub Issues
2. **Add Test Cases** to prevent regression
3. **Update Documentation** if needed
4. **Test Thoroughly** before submitting

### 3️⃣ Testing Requirements

#### Before Submitting
```bash
# Run all tests
python -m pytest tests/

# Test extension functionality
cd extension && npm test

# Test system integration
python TEST_PROXY.py

# Check code quality
flake8 our-server/
eslint extension/
```

#### Test Coverage
- **Unit Tests**: 80% minimum coverage
- **Integration Tests**: All major components
- **End-to-End Tests**: Complete user workflows
- **Performance Tests**: Latency and resource usage

### 4️⃣ Pull Request Process

#### PR Checklist
- [ ] **Documentation Updated**: All relevant docs updated
- [ ] **Tests Added**: New test cases for new features
- [ ] **Tests Passing**: All existing tests pass
- [ ] **Code Quality**: Follows style guidelines
- [ ] **Performance**: No significant performance regression
- [ ] **Security**: No security vulnerabilities introduced
- [ ] **Compatibility**: Works with existing configurations

#### PR Template
```markdown
## 🎯 Description
Brief description of changes

## 🔧 Changes Made
- [ ] Feature A added
- [ ] Bug B fixed
- [ ] Documentation C updated

## 🧪 Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Performance tested

## 📚 Documentation
- [ ] System Overview updated
- [ ] Agent Descriptions updated
- [ ] Setup Guide updated
- [ ] Code comments added

## 🔍 Review Checklist
- [ ] Code follows style guidelines
- [ ] No breaking changes
- [ ] Backward compatibility maintained
- [ ] Security considerations addressed
```

## 🛠️ Development Setup

### Local Development Environment
```bash
# Clone repository
git clone https://github.com/devsahon/ZombieCoder-Agent-Personal.git
cd ZombieCoder-Agent-Personal

# Create development branch
git checkout -b feature/your-feature-name

# Setup development environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Setup extension development
cd extension
npm install
cd ..

# Start development servers
python our-server/main_server.py &
python our-server/proxy_server.py &
python our-server/multi_project_api.py &
```

### Development Tools
```bash
# Install development dependencies
pip install pytest pytest-cov flake8 black
npm install -g eslint prettier

# Code formatting
black our-server/
prettier --write extension/

# Linting
flake8 our-server/
eslint extension/
```

## 🎭 Agent Development

### Adding New Agents
1. **Update Agent System** (`our-server/unified_agent_system.py`)
2. **Add Agent Description** (`docs/AGENT_DESCRIPTIONS.md`)
3. **Update Extension** (`extension/force-local-extension.js`)
4. **Add Tests** (`tests/test_agents.py`)
5. **Update Configuration** (`our-server/config.json`)

### Agent Template
```python
class NewAgent:
    """New Agent for specific functionality."""
    
    def __init__(self):
        self.name = "NewAgent"
        self.identity = "আমি নতুন এজেন্ট, বিশেষ কাজ করি।"
        self.capabilities = ["capability1", "capability2"]
        
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process message with new agent logic."""
        try:
            # Agent-specific processing
            response = self.special_processing(message)
            return {
                "response": response,
                "agent": self.name,
                "capability": "capability1",
                "source": "local"
            }
        except Exception as e:
            logger.error(f"NewAgent error: {e}")
            return {"error": str(e)}
```

## 🔒 Security Guidelines

### Code Security
1. **Input Validation**: Validate all user inputs
2. **Error Handling**: Don't expose sensitive information
3. **API Security**: Use proper authentication
4. **Data Protection**: Encrypt sensitive data
5. **Dependency Security**: Keep dependencies updated

### Security Checklist
- [ ] No hardcoded secrets
- [ ] Input sanitization implemented
- [ ] Error messages don't leak information
- [ ] API endpoints properly secured
- [ ] Dependencies scanned for vulnerabilities

## 📊 Performance Guidelines

### Performance Standards
- **Response Time**: < 5 seconds for local processing
- **Memory Usage**: < 4GB for main server
- **CPU Usage**: < 80% during processing
- **Network**: Minimal external requests

### Performance Testing
```bash
# Load testing
python tests/performance_test.py

# Memory profiling
python -m memory_profiler our-server/main_server.py

# CPU profiling
python -m cProfile our-server/main_server.py
```

## 🚀 Release Process

### Version Management
- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Changelog**: Update CHANGELOG.md
- **Release Notes**: Detailed release documentation
- **Backward Compatibility**: Maintain compatibility

### Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Performance benchmarks met
- [ ] Security scan completed
- [ ] Release notes prepared
- [ ] Version tags created

## 🤝 Community Guidelines

### Communication
- **Respectful**: Be respectful to all contributors
- **Constructive**: Provide constructive feedback
- **Helpful**: Help others learn and grow
- **Inclusive**: Welcome diverse perspectives

### Code of Conduct
1. **Be Respectful**: Treat everyone with respect
2. **Be Inclusive**: Welcome diverse contributors
3. **Be Constructive**: Provide helpful feedback
4. **Be Patient**: Allow time for responses
5. **Be Professional**: Maintain professional behavior

## 📞 Getting Help

### Support Channels
- **GitHub Issues**: [Report bugs](https://github.com/devsahon/ZombieCoder-Agent-Personal/issues)
- **Discussions**: [Community support](https://github.com/devsahon/ZombieCoder-Agent-Personal/discussions)
- **Documentation**: [Full documentation](https://github.com/devsahon/ZombieCoder-Agent-Personal/tree/main/docs)

### Before Asking for Help
1. **Read Documentation**: Check docs/ folder first
2. **Search Issues**: Look for similar problems
3. **Test Locally**: Reproduce the issue
4. **Provide Details**: Include error messages and context

---

**🎯 Remember**: The goal is to maintain a high-quality, stable, and user-friendly AI development environment. Every contribution should improve the system for all users.

**📝 Note**: This guide is a living document. Please suggest improvements and updates as needed.
