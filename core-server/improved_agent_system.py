#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ZombieCoder Improved Unified Agent System
"যেখানে কোড ও কথা বলে"

Enhanced version with better local AI integration and error handling
"""

import os
import json
import time
import logging
import requests
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any, Optional, List
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImprovedUnifiedAgent:
    def __init__(self):
        self.name = "ZombieCoder Agent (সাহন ভাই)"
        self.family_members = ['সাহন ভাই', 'মুসকান', 'ভাবি', 'বাঘ', 'হান্টার', 'পরিবার']

        # Ollama configuration
        self.ollama_url = "http://localhost:11434"
        self.default_model = "llama3.2:1b"

        # Capabilities
        self.capabilities = {
            "coding": {"description": "Programming and development tasks"},
            "debugging": {"description": "Error fixing and troubleshooting"},
            "frontend": {"description": "UI/UX development"},
            "database": {"description": "Database operations"},
            "api": {"description": "API development and integration"},
            "security": {"description": "Security and authentication"},
            "performance": {"description": "Performance optimization"},
            "devops": {"description": "Deployment and infrastructure"},
            "general": {"description": "General conversation and assistance"},
            "real_time": {"description": "Real-time information and updates"}
        }

        # System status
        self.system_status = {
            "ollama_connected": False,
            "available_models": [],
            "last_health_check": None
        }

        # Initialize system
        self.initialize_system()

    def initialize_system(self):
        """Initialize the system and check connections"""
        logger.info("🚀 Initializing Improved Unified Agent System...")

        # Check Ollama connection
        self.check_ollama_connection()

        # Log initialization
        logger.info(f"🎭 Agent: {self.name}")
        logger.info(f"👨‍👩‍👧 Family Members: {self.family_members}")
        logger.info(f"🌐 Ollama URL: {self.ollama_url}")
        logger.info(f"🤖 Available Models: {self.system_status['available_models']}")

    def check_ollama_connection(self):
        """Check Ollama server connection and available models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                self.system_status['available_models'] = [
                    model.get('name', '') for model in models_data.get('models', [])
                ]
                self.system_status['ollama_connected'] = True
                self.system_status['last_health_check'] = datetime.now()
                logger.info(f"✅ Ollama connected. Available models: {self.system_status['available_models']}")
                return True
            else:
                logger.error(f"❌ Ollama API error: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Ollama connection failed: {e}")
            self.system_status['ollama_connected'] = False
            return False

    def detect_capability(self, message: str) -> str:
        """Detect the capability needed for the message"""
        message_lower = message.lower()

        # Coding related
        if any(word in message_lower for word in ['code', 'program', 'function', 'class', 'bug', 'error']):
            return "coding"

        # Debugging
        if any(word in message_lower for word in ['debug', 'fix', 'error', 'problem', 'issue']):
            return "debugging"

        # Frontend
        if any(word in message_lower for word in ['html', 'css', 'javascript', 'react', 'vue', 'ui', 'design']):
            return "frontend"

        # Database
        if any(word in message_lower for word in ['database', 'sql', 'query', 'table', 'data']):
            return "database"

        # API
        if any(word in message_lower for word in ['api', 'endpoint', 'rest', 'http']):
            return "api"

        # Security
        if any(word in message_lower for word in ['security', 'auth', 'password', 'encrypt']):
            return "security"

        # Performance
        if any(word in message_lower for word in ['performance', 'speed', 'optimize', 'fast']):
            return "performance"

        # DevOps
        if any(word in message_lower for word in ['deploy', 'server', 'docker', 'cloud']):
            return "devops"

        # Real-time
        if any(word in message_lower for word in ['real-time', 'live', 'current', 'now']):
            return "real_time"

        return "general"

    def create_family_prompt(self, message: str, capability: str, context: Dict[str, Any] = None) -> str:
        """Create a family-oriented prompt"""
        if context is None:
            context = {}

        agent = context.get('agent', 'সাহন ভাই')

        base_prompt = f"""You are {agent}, a helpful AI assistant from the ZombieCoder family.
You are speaking in Bengali (বাংলা) and should respond in a friendly, family-oriented way.

User message: {message}

Capability needed: {capability}

Please provide a helpful response in Bengali, being warm and supportive like a family member would be."""

        return base_prompt

    def call_local_ai(self, prompt: str, model: str = None) -> Optional[str]:
        """Call local Ollama AI with improved error handling"""
        if not self.system_status['ollama_connected']:
            logger.error("❌ Ollama not connected")
            return None

        # Use default model if none specified
        if model is None:
            model = self.default_model

        # Check if model is available
        if model not in self.system_status['available_models']:
            logger.warning(f"⚠️ Model {model} not available, using first available model")
            if self.system_status['available_models']:
                model = self.system_status['available_models'][0]
            else:
                logger.error("❌ No models available")
                return None

        try:
            logger.info(f"🤖 Calling Ollama with model: {model}")

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 500,
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "")
                logger.info(f"✅ Local AI response received from {model}")
                return response_text
            else:
                logger.error(f"❌ Ollama API error: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.Timeout:
            logger.error("❌ Ollama API timeout")
            return None
        except requests.exceptions.ConnectionError:
            logger.error("❌ Cannot connect to Ollama server")
            self.system_status['ollama_connected'] = False
            return None
        except Exception as e:
            logger.error(f"❌ Local AI error: {e}")
            return None

    def process_message(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process message with improved local AI integration"""
        if context is None:
            context = {}

        logger.info(f"📝 Processing message: {message[:50]}...")

        # Detect capability
        capability = self.detect_capability(message)
        logger.info(f"🎯 Detected capability: {capability}")

        # Create prompt
        prompt = self.create_family_prompt(message, capability, context)

        # Try local AI first
        response = self.call_local_ai(prompt)

        if response:
            logger.info("✅ Local AI response successful")
            return {
                "response": response,
                "agent": self.name,
                "capability": capability,
                "capability_info": self.capabilities.get(capability, {}),
                "source": "local_ai",
                "model_used": self.default_model,
                "timestamp": datetime.now().isoformat()
            }
        else:
            logger.warning("⚠️ Local AI failed, returning fallback response")
            return {
                "response": "ভাই, আমি এখনই আপনার প্রশ্নের উত্তর দিতে পারছি না। দয়া করে একটু পরে আবার চেষ্টা করুন।",
                "agent": self.name,
                "capability": capability,
                "capability_info": self.capabilities.get(capability, {}),
                "source": "fallback",
                "error": "local_ai_unavailable",
                "timestamp": datetime.now().isoformat()
            }

    def get_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            "agent": self.name,
            "family_members": self.family_members,
            "capabilities": list(self.capabilities.keys()),
            "system_status": self.system_status,
            "ollama_url": self.ollama_url,
            "default_model": self.default_model,
            "timestamp": datetime.now().isoformat()
        }

    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "name": self.name,
            "description": "ZombieCoder Improved Unified Agent System",
            "version": "2.0.0",
            "capabilities": self.capabilities,
            "family_members": self.family_members,
            "endpoints": {
                "chat": "/chat",
                "status": "/status",
                "info": "/info"
            }
        }

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize agent
unified_agent = ImprovedUnifiedAgent()

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "agent": unified_agent.name,
        "endpoints": {
            "chat": "/chat",
            "info": "/info",
            "status": "/status"
        },
        "family": {
            "সাহন ভাই": "Main AI Assistant",
            "মুসকান": "Voice Assistant",
            "ভাবি": "Document Assistant",
            "পরিবার": "Family Coordinator"
        },
        "capabilities": list(unified_agent.capabilities.keys()),
        "ollama_status": unified_agent.system_status['ollama_connected'],
        "available_models": unified_agent.system_status['available_models']
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        agent = data.get('agent', 'সাহন ভাই')

        if not message:
            return jsonify({"error": "Message is required"}), 400

        logger.info(f"💬 Chat request from {agent}: {message[:50]}...")

        result = unified_agent.process_message(message, {"agent": agent})

        logger.info(f"✅ Chat response sent to {agent}")
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ Chat endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/status')
def status():
    """Status endpoint"""
    return jsonify(unified_agent.get_status())

@app.route('/info')
def info():
    """Info endpoint"""
    return jsonify(unified_agent.get_info())

if __name__ == '__main__':
    logger.info("🤖 Starting ZombieCoder Improved Unified Agent System...")
    logger.info(f"🎭 Agent: {unified_agent.name}")
    logger.info(f"👨‍👩‍👧 Family Members: {unified_agent.family_members}")
    logger.info("🌐 Server starting on http://localhost:12345")
    logger.info("📡 Available endpoints:")
    logger.info("   - GET  / (home)")
    logger.info("   - POST /chat (chat with agents)")
    logger.info("   - GET  /status (agent status)")
    logger.info("   - GET  /info (agent info)")
    logger.info("=" * 50)

    app.run(host='0.0.0.0', port=12345, debug=True)
