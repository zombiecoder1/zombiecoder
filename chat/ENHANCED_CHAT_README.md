# Enhanced Chat Interface with Prompt Orchestration System

**Editor ভাই-এর জন্য Real-time Chat System**

এটি একটি সম্পূর্ণ AI-powered chat interface যা Prompt Orchestration System এর সাথে integrated। Real-time conversation, multi-language support, এবং advanced AI capabilities সহ।

## 🚀 Features

### Core Features
- **Smart Prompt Orchestration** - Intelligent prompt routing and processing
- **Multi-language Support** - Bengali, English, Hindi, Urdu, Arabic
- **Real-time Communication** - WebSocket-based streaming responses
- **Voice Integration** - Speech-to-text and text-to-speech
- **Session Management** - Persistent conversation history
- **System Monitoring** - Real-time health checks

### Advanced Capabilities
- **Intent Detection** - Automatic understanding of user intent
- **Language Detection** - Automatic language identification
- **Model Routing** - Smart routing to appropriate AI models
- **TTS Integration** - High-quality Bengali and English speech synthesis
- **Fallback Systems** - Graceful degradation when services are unavailable

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Next.js UI    │    │  Orchestrator    │    │   AI Models     │
│                 │◄──►│     Server       │◄──►│                 │
│ - Chat Interface│    │ - Prompt Refiner │    │ - Ollama LLM    │
│ - Voice Controls│    │ - Model Router   │    │ - Coqui TTS     │
│ - Session Mgmt  │    │ - Output Format  │    │ - OpenAI API    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Memory Server  │    │   TTS Server     │    │  AI Server      │
│                 │    │                  │    │                 │
│ - User Memory   │    │ - Voice Synthesis│    │ - Chat Logic    │
│ - Preferences   │    │ - Audio Playback │    │ - Response Gen  │
│ - History       │    │ - Language Det   │    │ - Streaming     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🛠️ Installation & Setup

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Ollama (for local LLM)
- Coqui TTS (optional)

### 1. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies for orchestrator
cd orchestrator
pip install -r requirements.txt
cd ..
```

### 2. Environment Configuration

Create `.env.local` file:

```env
# Database Configuration
DATABASE_URL=your_neon_database_url_here

# AI Server Configuration
AI_SERVER_PORT=3001
AI_SERVER_URL=http://localhost:3001

# Memory Server Configuration
MEMORY_SERVER_PORT=3003
MEMORY_SERVER_URL=http://localhost:3003

# TTS Server Configuration
TTS_SERVER_PORT=3002
TTS_SERVER_URL=http://localhost:3002

# Orchestrator Server Configuration
ORCHESTRATOR_PORT=3004
ORCHESTRATOR_URL=http://localhost:3004

# Google TTS API Key (Optional)
GOOGLE_TTS_API_KEY=your_google_tts_api_key_here

# Local AI Model Configuration
LOCAL_AI_URL=http://localhost:11434
LOCAL_AI_MODEL=llama2

# Environment
NODE_ENV=development
```

### 3. Start All Services

#### Option 1: Automated Startup (Windows)
```bash
# Double-click the batch file
start-enhanced-chat.bat
```

#### Option 2: Manual Startup
```bash
# Terminal 1: AI Server
npm run server

# Terminal 2: Memory Server  
npm run memory

# Terminal 3: TTS Server
npm run tts

# Terminal 4: Orchestrator Server
npm run orchestrator

# Terminal 5: Next.js Server
npm run dev
```

#### Option 3: Node.js Script
```bash
npm run start-all
```

## 🎯 Usage

### 1. Access the Interface
Open your browser and go to: `http://localhost:3000`

### 2. Start Chatting
- **Text Input**: Type your message in Bengali or English
- **Voice Input**: Click the microphone icon to speak
- **Voice Output**: Click the speaker icon to hear responses

### 3. Features Available
- **Multi-language**: Ask questions in Bengali, English, or mixed
- **Voice Commands**: Use speech recognition for input
- **Audio Responses**: Listen to AI responses in Bengali/English
- **Session History**: View and manage conversation history
- **System Status**: Monitor all service health

## 🔧 API Endpoints

### Orchestrator Server (Port 3004)
- `POST /api/chat` - Process chat messages
- `POST /api/chat/stream` - Streaming chat responses
- `GET /api/status` - System status
- `GET /api/health` - Health check

### Next.js API Routes
- `POST /api/chat` - Enhanced chat with orchestrator integration
- `POST /api/memory` - Memory management
- `POST /api/tts` - Text-to-speech

## 📊 System Monitoring

### Health Checks
- **Orchestrator**: `http://localhost:3004/api/health`
- **AI Server**: `http://localhost:3001/health`
- **TTS Server**: `http://localhost:3002/health`
- **Memory Server**: `http://localhost:3003/health`

### Status Indicators
- 🟢 Green: Service is healthy and running
- 🔴 Red: Service is down or unreachable

## 🎨 Customization

### Adding New Languages
1. Update `LANGUAGE_PATTERNS` in `orchestrator/config.py`
2. Add language detection patterns
3. Update TTS language support

### Adding New Models
1. Configure model in `orchestrator/config.py`
2. Implement query method in `orchestrator/model_interface.py`
3. Update routing logic in `orchestrator/prompt_refiner.py`

### Custom Output Formats
1. Add format in `orchestrator/output_formatter.py`
2. Implement formatting logic
3. Update API endpoints

## 🐛 Troubleshooting

### Common Issues

#### 1. Orchestrator Not Starting
```bash
# Check Python dependencies
cd orchestrator
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

#### 2. Port Conflicts
```bash
# Check if ports are in use
netstat -an | findstr "3001\|3002\|3003\|3004"

# Kill processes if needed
taskkill /F /PID <process_id>
```

#### 3. AI Model Not Responding
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

#### 4. TTS Not Working
```bash
# Check TTS server
curl http://localhost:3002/health

# Check browser permissions for microphone
```

### Debug Mode
```bash
# Enable debug logging
NODE_ENV=development npm run dev

# Check logs
tail -f logs/combined.log
```

## 📈 Performance Optimization

### 1. Model Optimization
- Use smaller models for faster responses
- Enable model caching
- Optimize prompt templates

### 2. Caching
- Enable response caching
- Cache user preferences
- Cache conversation history

### 3. Load Balancing
- Use multiple AI server instances
- Implement request queuing
- Add rate limiting

## 🔒 Security Considerations

### 1. API Security
- Implement authentication
- Add rate limiting
- Validate input data

### 2. Data Privacy
- Encrypt sensitive data
- Implement data retention policies
- Add user consent mechanisms

### 3. Network Security
- Use HTTPS in production
- Implement CORS policies
- Add request validation

## 🚀 Deployment

### Production Setup
1. **Environment Variables**: Set production values
2. **Database**: Configure production database
3. **SSL**: Enable HTTPS
4. **Monitoring**: Add logging and monitoring
5. **Scaling**: Use load balancers and multiple instances

### Docker Deployment
```dockerfile
# Create Dockerfile for each service
# Use docker-compose for orchestration
# Implement health checks
```

## 📝 Development

### Adding New Features
1. **Backend**: Add to orchestrator system
2. **Frontend**: Update React components
3. **API**: Add new endpoints
4. **Testing**: Write unit and integration tests

### Code Structure
```
├── app/                    # Next.js app directory
├── components/             # React components
├── orchestrator/           # Python orchestrator system
├── server/                 # Node.js servers
├── scripts/                # Utility scripts
└── public/                 # Static assets
```

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

## 🎯 Quick Start Summary

1. **Install**: `npm install && cd orchestrator && pip install -r requirements.txt`
2. **Configure**: Create `.env.local` with your settings
3. **Start**: Run `start-enhanced-chat.bat` or `npm run start-all`
4. **Access**: Open `http://localhost:3000`
5. **Chat**: Start chatting in Bengali or English!

**Happy chatting with Editor ভাই! 🚀**
