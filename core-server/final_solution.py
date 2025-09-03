#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Final Solution for ZombieCoder
Direct connection between Ollama and Main Server
"""

import os
import sys
import json
import time
import requests
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

class FinalSolution:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Configuration
        self.ollama_url = "http://localhost:11434"
        self.main_server_url = "http://localhost:12345"
        
        # Setup routes
        self.setup_routes()
        
        # Start health check
        self.start_health_check()
    
    def setup_routes(self):
        """Setup direct connection routes"""
        
        @self.app.route('/api/chat', methods=['POST'])
        def direct_chat():
            """Direct chat with Ollama"""
            try:
                data = request.get_json()
                message = data.get('message', '')
                agent = data.get('agent', 'bhai')
                
                # Format message for agent
                formatted_message = f"[{agent}] {message}"
                
                # Send directly to Ollama
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": "llama3.2:1b",
                        "prompt": formatted_message,
                        "stream": False
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result.get('response', 'No response')
                    
                    return jsonify({
                        "response": ai_response,
                        "agent": agent,
                        "model": "llama3.2:1b",
                        "status": "success"
                    })
                else:
                    return jsonify({
                        "error": f"Ollama error: {response.text}",
                        "status": "error"
                    }), 500
                    
            except Exception as e:
                return jsonify({
                    "error": f"Chat error: {str(e)}",
                    "status": "error"
                }), 500
        
        @self.app.route('/api/agents', methods=['GET'])
        def get_agents():
            """Get available agents"""
            return jsonify({
                "agents": ["bhai", "hamba", "bondhu", "custom"],
                "status": "available"
            })
        
        @self.app.route('/api/status', methods=['GET'])
        def get_status():
            """Get system status"""
            status = {
                "timestamp": time.time(),
                "ollama": {"status": "unknown"},
                "agents": ["bhai", "hamba", "bondhu", "custom"],
                "model": "llama3.2:1b"
            }
            
            # Check Ollama
            try:
                ollama_response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
                if ollama_response.status_code == 200:
                    status["ollama"]["status"] = "running"
                    status["ollama"]["models"] = [m['name'] for m in ollama_response.json().get('models', [])]
                else:
                    status["ollama"]["status"] = "error"
            except:
                status["ollama"]["status"] = "not_connected"
            
            return jsonify(status)
        
        @self.app.route('/api/test', methods=['GET'])
        def test_connection():
            """Test Ollama connection"""
            try:
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": "llama3.2:1b",
                        "prompt": "Hello",
                        "stream": False
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    return jsonify({
                        "status": "success",
                        "message": "Ollama is working correctly",
                        "response": response.json().get('response', '')
                    })
                else:
                    return jsonify({
                        "status": "error",
                        "message": f"Ollama error: {response.text}"
                    })
                    
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": f"Connection failed: {str(e)}"
                })
    
    def start_health_check(self):
        """Start health check thread"""
        def health_check():
            while True:
                try:
                    # Check Ollama every 30 seconds
                    response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
                    if response.status_code != 200:
                        print(f"⚠️ Ollama health check failed: {response.status_code}")
                    else:
                        print("✅ Ollama health check passed")
                    
                    time.sleep(30)
                    
                except Exception as e:
                    print(f"❌ Health check error: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=health_check, daemon=True)
        thread.start()
        print("🏥 Health check started")

if __name__ == "__main__":
    solution = FinalSolution()
    print("🎯 Final Solution started")
    print("🌐 Direct Ollama connection")
    print("📡 Endpoints:")
    print("  - POST /api/chat")
    print("  - GET  /api/agents")
    print("  - GET  /api/status")
    print("  - GET  /api/test")
    print(f"🌐 Server running on http://localhost:8082")
    solution.app.run(host='0.0.0.0', port=8082, debug=False)
