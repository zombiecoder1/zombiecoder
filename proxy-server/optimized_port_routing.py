#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Optimized Port Routing for ZombieCoder
Prevents PC slowdown by managing model loading intelligently
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptimizedPortRouter:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Port configuration
        self.ports = {
            "main_server": 12345,
            "proxy_server": 8080,
            "ollama": 11434,
            "smart_router": 9000
        }
        
        # Model management
        self.models = {
            "llama3.2:1b": {"loaded": False, "memory": 1300, "priority": 1},
            "qwen2.5-coder:1.5b-base": {"loaded": False, "memory": 986, "priority": 2},
            "codellama:latest": {"loaded": False, "memory": 3800, "priority": 3}
        }
        
        # System monitoring
        self.system_status = {
            "cpu_usage": 0,
            "memory_usage": 0,
            "active_models": 0,
            "max_models": 2  # Prevent PC slowdown
        }
        
        # Setup routes
        self.setup_routes()
        
        # Start monitoring
        self.start_monitoring()
    
    def setup_routes(self):
        """Setup optimized routes"""
        
        @self.app.route('/api/status', methods=['GET'])
        def get_status():
            """Get system status"""
            return jsonify({
                "status": "optimized",
                "ports": self.ports,
                "models": self.models,
                "system": self.system_status,
                "timestamp": time.time()
            })
        
        @self.app.route('/api/load_model', methods=['POST'])
        def load_model():
            """Intelligently load model based on system resources"""
            try:
                data = request.get_json()
                model_name = data.get('model', 'llama3.2:1b')
                
                # Check system resources
                if self.system_status['active_models'] >= self.system_status['max_models']:
                    return jsonify({
                        "error": "System overloaded. Please unload a model first.",
                        "active_models": self.system_status['active_models']
                    }), 400
                
                # Load model
                success = self.load_model_safely(model_name)
                if success:
                    return jsonify({
                        "message": f"Model {model_name} loaded successfully",
                        "active_models": self.system_status['active_models']
                    })
                else:
                    return jsonify({"error": f"Failed to load {model_name}"}), 500
                    
            except Exception as e:
                logger.error(f"Load model error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/unload_model', methods=['POST'])
        def unload_model():
            """Unload model to free resources"""
            try:
                data = request.get_json()
                model_name = data.get('model', 'llama3.2:1b')
                
                success = self.unload_model_safely(model_name)
                if success:
                    return jsonify({
                        "message": f"Model {model_name} unloaded successfully",
                        "active_models": self.system_status['active_models']
                    })
                else:
                    return jsonify({"error": f"Failed to unload {model_name}"}), 500
                    
            except Exception as e:
                logger.error(f"Unload model error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/chat', methods=['POST'])
        def optimized_chat():
            """Optimized chat with automatic model selection"""
            try:
                data = request.get_json()
                message = data.get('message', '')
                agent = data.get('agent', 'bhai')
                
                # Select best available model
                best_model = self.select_best_model()
                if not best_model:
                    return jsonify({"error": "No models available"}), 500
                
                # Process with selected model
                response = self.process_with_model(message, best_model, agent)
                
                return jsonify({
                    "response": response,
                    "model_used": best_model,
                    "system_status": self.system_status
                })
                
            except Exception as e:
                logger.error(f"Chat error: {e}")
                return jsonify({"error": str(e)}), 500
    
    def load_model_safely(self, model_name: str) -> bool:
        """Safely load model without overwhelming system"""
        try:
            if model_name not in self.models:
                logger.error(f"Unknown model: {model_name}")
                return False
            
            if self.models[model_name]["loaded"]:
                logger.info(f"Model {model_name} already loaded")
                return True
            
            # Check memory availability
            required_memory = self.models[model_name]["memory"]
            if self.system_status['memory_usage'] + required_memory > 80:
                logger.warning(f"Insufficient memory for {model_name}")
                return False
            
            # Load model via Ollama
            response = requests.post(
                f"http://localhost:{self.ports['ollama']}/api/pull",
                json={"name": model_name},
                timeout=30
            )
            
            if response.status_code == 200:
                self.models[model_name]["loaded"] = True
                self.system_status['active_models'] += 1
                logger.info(f"Model {model_name} loaded successfully")
                return True
            else:
                logger.error(f"Failed to load {model_name}: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Load model error: {e}")
            return False
    
    def unload_model_safely(self, model_name: str) -> bool:
        """Safely unload model"""
        try:
            if model_name not in self.models:
                return False
            
            if not self.models[model_name]["loaded"]:
                return True
            
            # Unload model
            self.models[model_name]["loaded"] = False
            self.system_status['active_models'] -= 1
            logger.info(f"Model {model_name} unloaded")
            return True
            
        except Exception as e:
            logger.error(f"Unload model error: {e}")
            return False
    
    def select_best_model(self) -> Optional[str]:
        """Select best available model based on priority and resources"""
        available_models = [
            name for name, info in self.models.items() 
            if info["loaded"]
        ]
        
        if not available_models:
            # Load default model
            if self.load_model_safely("llama3.2:1b"):
                return "llama3.2:1b"
            return None
        
        # Return highest priority model
        return min(available_models, key=lambda x: self.models[x]["priority"])
    
    def process_with_model(self, message: str, model: str, agent: str) -> str:
        """Process message with selected model"""
        try:
            # Format message for agent
            formatted_message = f"[{agent}] {message}"
            
            # Send to Ollama
            response = requests.post(
                f"http://localhost:{self.ports['ollama']}/api/generate",
                json={
                    "model": model,
                    "prompt": formatted_message,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response')
            else:
                return f"Error: {response.text}"
                
        except Exception as e:
            logger.error(f"Process error: {e}")
            return f"Error: {str(e)}"
    
    def start_monitoring(self):
        """Start system monitoring thread"""
        def monitor():
            while True:
                try:
                    # Monitor system resources
                    import psutil
                    self.system_status['cpu_usage'] = psutil.cpu_percent()
                    self.system_status['memory_usage'] = psutil.virtual_memory().percent
                    
                    # Auto-unload if system overloaded
                    if self.system_status['cpu_usage'] > 90 or self.system_status['memory_usage'] > 90:
                        logger.warning("System overloaded, unloading heavy models")
                        self.unload_model_safely("codellama:latest")
                    
                    time.sleep(30)  # Check every 30 seconds
                    
                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        logger.info("System monitoring started")

if __name__ == "__main__":
    router = OptimizedPortRouter()
    logger.info("🎯 Optimized Port Router started")
    logger.info(f"🌐 Server running on port {router.ports['proxy_server']}")
    router.app.run(host='0.0.0.0', port=router.ports['proxy_server'], debug=False)
