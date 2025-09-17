# Prompt Orchestration System

**Editor ভাই-এর জন্য Smart Prompt Routing System**

একটি সম্পূর্ণ AI-powered prompt orchestration system যা user input কে intelligently process করে, appropriate AI models এ route করে, এবং multiple formats এ response দেয়।

## 🚀 Features

- **Smart Input Processing**: Multi-language input detection এবং normalization
- **Intelligent Prompt Refining**: Context-aware prompt enhancement
- **Model Routing**: Automatic routing to appropriate AI models
- **Multi-format Output**: JSON, HTML, Text, Audio, Code, Conversation formats
- **Real-time TTS**: Bengali এবং English text-to-speech support
- **Conversation History**: Session-based conversation tracking
- **Health Monitoring**: Comprehensive system health checks

## 📁 Project Structure

```
prompt_orchestration_system/
├── config.py              # System configuration
├── input_handler.py       # User input processing
├── prompt_refiner.py      # Prompt refinement and routing
├── model_interface.py     # AI model integration
├── output_formatter.py    # Multi-format response formatting
├── main_orchestrator.py   # Main orchestration system
├── api_server.py          # FastAPI web server
├── demo.py               # Interactive demo script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🛠️ Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure models** (optional):
   - Edit `config.py` to add your API keys
   - Configure local model endpoints

## 🎯 Usage

### 1. Interactive Demo
```bash
python demo.py
```

### 2. Web API Server
```bash
python api_server.py
```
Then visit: `http://localhost:8000`

### 3. Direct Usage
```python
from main_orchestrator import PromptOrchestrator

orchestrator = PromptOrchestrator()
response = orchestrator.process_request(
    user_input="আজকের আবহাওয়া কেমন?",
    output_format="json"
)
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | System information and documentation |
| `/process` | POST | Process user input and get AI response |
| `/status` | GET | Get comprehensive system status |
| `/health` | GET | Health check endpoint |
| `/history` | GET | Get conversation history |
| `/stats` | GET | Get system statistics |
| `/reset` | POST | Reset current session |
| `/formats` | GET | Get supported output formats |

## 🔧 Configuration

### Model Configuration
Edit `config.py` to configure your AI models:

```python
models = {
    "llm_local": ModelConfig(
        name="Local LLM",
        endpoint="http://localhost:11434/api/generate",
        model_type="llm"
    ),
    "tts_coqui": ModelConfig(
        name="Coqui TTS",
        endpoint="local",
        model_type="tts"
    )
}
```

### Supported Languages
- Bengali (বাংলা)
- English
- Hindi
- Urdu
- Arabic

### Output Formats
- **JSON**: Structured data response
- **HTML**: Web-formatted response
- **Text**: Plain text response
- **Audio**: TTS audio response
- **Code**: Code-formatted response
- **Conversation**: Conversational response

## 🎨 Example Usage

### Bengali Weather Query
```python
response = orchestrator.process_request(
    user_input="আজকের আবহাওয়া কেমন?",
    output_format="json"
)
```

### English Coding Help
```python
response = orchestrator.process_request(
    user_input="How to fix a Python bug?",
    output_format="code"
)
```

### Translation Request
```python
response = orchestrator.process_request(
    user_input="Translate this to English: 'আমি একজন প্রোগ্রামার'",
    output_format="html"
)
```

## 🔍 System Components

### 1. Input Handler
- Language detection
- Text normalization
- Intent extraction
- Confidence scoring

### 2. Prompt Refiner
- Template selection
- Context enhancement
- Model routing
- Parameter optimization

### 3. Model Interface
- LLM integration (Ollama, OpenAI)
- TTS integration (Coqui TTS)
- Error handling
- Fallback mechanisms

### 4. Output Formatter
- Multi-format support
- Code highlighting
- Audio generation
- Response structuring

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### System Status
```bash
curl http://localhost:8000/status
```

### Statistics
```bash
curl http://localhost:8000/stats
```

## 🚨 Error Handling

The system includes comprehensive error handling:
- Input validation
- Model fallbacks
- Graceful degradation
- Detailed error logging

## 🔧 Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Formatting
```bash
black .
flake8 .
```

### Adding New Models
1. Add model configuration to `config.py`
2. Implement query method in `model_interface.py`
3. Update routing logic in `prompt_refiner.py`

## 📝 Logging

The system logs all activities:
- Request processing
- Model queries
- Error conditions
- Performance metrics

Logs are written to:
- Console output
- `orchestration.log` file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is part of the ZombieCoder Agent System.

## 👨‍💻 Author

**সাহন ভাই** - ZombieCoder Agent System

---

## 🎯 Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the demo**:
   ```bash
   python demo.py
   ```

3. **Start the API server**:
   ```bash
   python api_server.py
   ```

4. **Visit the web interface**:
   Open `http://localhost:8000` in your browser

## 💡 Tips

- Start with the interactive demo to understand the system
- Use Bengali and English inputs for best results
- Check system status regularly for optimal performance
- Monitor logs for debugging and optimization

**Happy coding with Editor ভাই! 🚀**
