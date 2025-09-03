#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏥 Final Solution Server
ZombieCoder System এর চূড়ান্ত সমাধান সার্ভার
"""

import os
import json
import time
import logging
import requests
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinalSolutionServer:
    def __init__(self):
        self.name = "Final Solution Server"
        self.ollama_url = "http://localhost:11434"
        self.default_model = "llama3.2:1b"
        
        # System status
        self.system_status = {
            "ollama_connected": False,
            "available_models": [],
            "last_health_check": None,
            "server_started": datetime.now().isoformat()
        }
        
        # Initialize
        self.initialize_system()
        
        # Start health check thread
        self.start_health_check()

    def initialize_system(self):
        """Initialize the system"""
        logger.info("🏥 Health check started")
        self.check_ollama_connection()

    def check_ollama_connection(self):
        """Check Ollama connection"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                self.system_status['available_models'] = [
                    model.get('name', '') for model in models_data.get('models', [])
                ]
                self.system_status['ollama_connected'] = True
                self.system_status['last_health_check'] = datetime.now().isoformat()
                logger.info("✅ Ollama health check passed")
                return True
            else:
                logger.error(f"❌ Ollama API error: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Ollama connection failed: {e}")
            self.system_status['ollama_connected'] = False
            return False

    def start_health_check(self):
        """Start periodic health check"""
        def health_check_loop():
            while True:
                self.check_ollama_connection()
                time.sleep(30)  # Check every 30 seconds
        
        thread = threading.Thread(target=health_check_loop, daemon=True)
        thread.start()

    def call_ollama(self, prompt: str, model: str = None) -> Optional[str]:
        """Call Ollama API"""
        if not self.system_status['ollama_connected']:
            return None

        if model is None:
            model = self.default_model

        try:
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
                return result.get("response", "")
            else:
                logger.error(f"❌ Ollama API error: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"❌ Ollama call error: {e}")
            return None

    def process_message(self, message: str, agent: str = "bhai") -> Dict[str, Any]:
        """Process message"""
        logger.info(f"📝 Processing message from {agent}: {message[:50]}...")

        # Create prompt
        prompt = f"""You are {agent}, a helpful AI assistant from the ZombieCoder family.
You are speaking in Bengali (বাংলা) and should respond in a friendly, family-oriented way.

User message: {message}

Please provide a helpful response in Bengali, being warm and supportive like a family member would be."""

        # Call Ollama
        response = self.call_ollama(prompt)

        if response:
            return {
                "response": response,
                "agent": agent,
                "source": "ollama",
                "model_used": self.default_model,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "response": "ভাই, আমি এখনই আপনার প্রশ্নের উত্তর দিতে পারছি না। দয়া করে একটু পরে আবার চেষ্টা করুন।",
                "agent": agent,
                "source": "fallback",
                "error": "ollama_unavailable",
                "timestamp": datetime.now().isoformat()
            }

    def get_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            "server": self.name,
            "status": "running",
            "ollama_connected": self.system_status['ollama_connected'],
            "available_models": self.system_status['available_models'],
            "last_health_check": self.system_status['last_health_check'],
            "server_started": self.system_status['server_started'],
            "timestamp": datetime.now().isoformat()
        }

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize server
final_solution = FinalSolutionServer()

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "server": final_solution.name,
        "status": "running",
        "endpoints": {
            "chat": "/api/chat",
            "status": "/api/status",
            "agents": "/api/agents",
            "test": "/api/test"
        }
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        agent = data.get('agent', 'bhai')

        if not message:
            return jsonify({"error": "Message is required"}), 400

        result = final_solution.process_message(message, agent)
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ Chat endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/status')
def status():
    """Status endpoint"""
    return jsonify(final_solution.get_status())

@app.route('/api/agents')
def agents():
    """Available agents"""
    return jsonify({
        "agents": [
            {
                "name": "bhai",
                "description": "Main AI Assistant",
                "capabilities": ["general", "coding", "debugging"]
            },
            {
                "name": "muskan",
                "description": "Voice Assistant",
                "capabilities": ["voice", "speech"]
            },
            {
                "name": "bhabi",
                "description": "Document Assistant",
                "capabilities": ["document", "writing"]
            }
        ]
    })

@app.route('/api/test')
def test():
    """Test endpoint"""
    return jsonify({
        "message": "Final Solution Server is working!",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    logger.info("🎯 Final Solution started")
    logger.info("🌐 Direct Ollama connection")
    logger.info("📡 Endpoints:")
    logger.info("  - POST /api/chat")
    logger.info("  - GET  /api/agents")
    logger.info("  - GET  /api/status")
    logger.info("  - GET  /api/test")
    logger.info("🌐 Server running on http://localhost:8082")

    app.run(host='0.0.0.0', port=8082, debug=False)
