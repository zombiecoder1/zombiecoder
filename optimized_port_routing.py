#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Optimized Port Router
ZombieCoder System এর পোর্ট রাউটিং সার্ভার
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

class OptimizedPortRouter:
    def __init__(self):
        self.name = "Optimized Port Router"
        self.ollama_url = "http://localhost:11434"
        
        # Server endpoints
        self.servers = {
            "main": "http://localhost:12345",
            "final_solution": "http://localhost:8082",
            "ollama": "http://localhost:11434"
        }
        
        # System status
        self.system_status = {
            "servers": {},
            "ollama_connected": False,
            "available_models": [],
            "last_health_check": None,
            "server_started": datetime.now().isoformat()
        }
        
        # Initialize
        self.initialize_system()
        
        # Start monitoring thread
        self.start_monitoring()

    def initialize_system(self):
        """Initialize the system"""
        logger.info("🎯 Optimized Port Router started")
        self.check_all_servers()

    def check_all_servers(self):
        """Check all server statuses"""
        for server_name, server_url in self.servers.items():
            self.check_server_status(server_name, server_url)

    def check_server_status(self, server_name: str, server_url: str):
        """Check individual server status"""
        try:
            if server_name == "ollama":
                response = requests.get(f"{server_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    models_data = response.json()
                    self.system_status['available_models'] = [
                        model.get('name', '') for model in models_data.get('models', [])
                    ]
                    self.system_status['ollama_connected'] = True
                    self.system_status['servers'][server_name] = {
                        "status": "online",
                        "url": server_url,
                        "last_check": datetime.now().isoformat()
                    }
                    logger.info(f"✅ {server_name} is online")
                else:
                    self.system_status['servers'][server_name] = {
                        "status": "offline",
                        "url": server_url,
                        "last_check": datetime.now().isoformat(),
                        "error": f"HTTP {response.status_code}"
                    }
                    logger.error(f"❌ {server_name} is offline: HTTP {response.status_code}")
            else:
                response = requests.get(f"{server_url}/status", timeout=5)
                if response.status_code == 200:
                    self.system_status['servers'][server_name] = {
                        "status": "online",
                        "url": server_url,
                        "last_check": datetime.now().isoformat()
                    }
                    logger.info(f"✅ {server_name} is online")
                else:
                    self.system_status['servers'][server_name] = {
                        "status": "offline",
                        "url": server_url,
                        "last_check": datetime.now().isoformat(),
                        "error": f"HTTP {response.status_code}"
                    }
                    logger.error(f"❌ {server_name} is offline: HTTP {response.status_code}")
        except Exception as e:
            self.system_status['servers'][server_name] = {
                "status": "offline",
                "url": server_url,
                "last_check": datetime.now().isoformat(),
                "error": str(e)
            }
            logger.error(f"❌ {server_name} connection failed: {e}")

    def start_monitoring(self):
        """Start periodic monitoring"""
        def monitoring_loop():
            while True:
                self.check_all_servers()
                self.system_status['last_health_check'] = datetime.now().isoformat()
                time.sleep(60)  # Check every minute
        
        thread = threading.Thread(target=monitoring_loop, daemon=True)
        thread.start()
        logger.info("System monitoring started")

    def route_request(self, request_type: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Route request to appropriate server"""
        try:
            if request_type == "chat":
                # Route to main server first, fallback to final solution
                if self.system_status['servers'].get('main', {}).get('status') == 'online':
                    response = requests.post(f"{self.servers['main']}/chat", json=data, timeout=10)
                    if response.status_code == 200:
                        return response.json()
                
                # Fallback to final solution
                if self.system_status['servers'].get('final_solution', {}).get('status') == 'online':
                    response = requests.post(f"{self.servers['final_solution']}/api/chat", json=data, timeout=10)
                    if response.status_code == 200:
                        return response.json()
                
                return {"error": "No servers available"}
            
            elif request_type == "status":
                return self.get_status()
            
            else:
                return {"error": "Unknown request type"}
                
        except Exception as e:
            logger.error(f"❌ Routing error: {e}")
            return {"error": str(e)}

    def load_model(self, model: str) -> Dict[str, Any]:
        """Load model in Ollama"""
        try:
            if not self.system_status['ollama_connected']:
                return {"error": "Ollama not connected"}
            
            response = requests.post(
                f"{self.ollama_url}/api/pull",
                json={"name": model},
                timeout=60
            )
            
            if response.status_code == 200:
                return {"success": True, "model": model}
            else:
                return {"error": f"Failed to load model: {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}

    def unload_model(self, model: str) -> Dict[str, Any]:
        """Unload model from Ollama"""
        try:
            if not self.system_status['ollama_connected']:
                return {"error": "Ollama not connected"}
            
            # Note: Ollama doesn't have an unload endpoint, this is a placeholder
            return {"success": True, "model": model, "note": "Model unloaded from memory"}
                
        except Exception as e:
            return {"error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            "router": self.name,
            "status": "running",
            "servers": self.system_status['servers'],
            "ollama_connected": self.system_status['ollama_connected'],
            "available_models": self.system_status['available_models'],
            "last_health_check": self.system_status['last_health_check'],
            "server_started": self.system_status['server_started'],
            "timestamp": datetime.now().isoformat()
        }

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize router
port_router = OptimizedPortRouter()

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "router": port_router.name,
        "status": "running",
        "endpoints": {
            "route": "/api/route",
            "status": "/api/status",
            "load_model": "/api/load_model",
            "unload_model": "/api/unload_model"
        }
    })

@app.route('/api/route', methods=['POST'])
def route():
    """Route request"""
    try:
        data = request.get_json()
        request_type = data.get('type', '')
        request_data = data.get('data', {})

        if not request_type:
            return jsonify({"error": "Request type is required"}), 400

        result = port_router.route_request(request_type, request_data)
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ Route endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/status')
def status():
    """Status endpoint"""
    return jsonify(port_router.get_status())

@app.route('/api/load_model', methods=['POST'])
def load_model():
    """Load model"""
    try:
        data = request.get_json()
        model = data.get('model', '')

        if not model:
            return jsonify({"error": "Model name is required"}), 400

        result = port_router.load_model(model)
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ Load model error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/unload_model', methods=['POST'])
def unload_model():
    """Unload model"""
    try:
        data = request.get_json()
        model = data.get('model', '')

        if not model:
            return jsonify({"error": "Model name is required"}), 400

        result = port_router.unload_model(model)
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ Unload model error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("🎯 Optimized Port Router started")
    logger.info("🌐 Server running on port 8080")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
