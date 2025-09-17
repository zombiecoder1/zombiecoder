#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Cursor Proxy Interceptor - Shadow Proxy Technique
Intercepts Cursor's requests and redirects to local Ollama
Maintains UI workflow while using local models
"""

import os
import json
import time
import logging
import requests
import threading
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from typing import Dict, Any, Optional
import subprocess
import signal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CursorProxyInterceptor:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Port configuration
        self.ports = {
            "interceptor": 8080,  # Main proxy port
            "ollama": 11434,      # Local Ollama
            "cursor_backup": 8081 # Backup for Cursor's original requests
        }
        
        # Model configuration
        self.models = {
            "deepseek-coder:1.3b": {"priority": 1, "size": "776MB"},
            "llama2:7b": {"priority": 2, "size": "3.8GB"},
            "llama3.2:1b": {"priority": 3, "size": "1.3GB"}
        }
        
        # Request tracking
        self.request_count = 0
        self.local_responses = 0
        self.cursor_responses = 0
        
        # Setup routes
        self.setup_routes()
        
        # Start monitoring
        self.start_monitoring()
        
        logger.info("🎯 Cursor Proxy Interceptor initialized")
    
    def setup_routes(self):
        """Setup interceptor routes"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            try:
                # Check Ollama connection
                ollama_health = requests.get(
                    f"http://localhost:{self.ports['ollama']}/api/tags",
                    timeout=5
                ).status_code == 200
                
                return jsonify({
                    "status": "healthy" if ollama_health else "degraded",
                    "ollama_connected": ollama_health,
                    "request_count": self.request_count,
                    "local_responses": self.local_responses,
                    "cursor_responses": self.cursor_responses,
                    "timestamp": time.time()
                }), 200 if ollama_health else 503
                
            except Exception as e:
                logger.error(f"Health check error: {e}")
                return jsonify({
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": time.time()
                }), 503
        
        @self.app.route('/v1/chat/completions', methods=['POST'])
        def chat_completions():
            """Intercept Cursor's chat completions requests"""
            try:
                self.request_count += 1
                data = request.get_json()
                
                logger.info(f"📨 Intercepted Cursor request #{self.request_count}")
                logger.debug(f"Request data: {json.dumps(data, indent=2)}")
                
                # Extract message from Cursor's format
                messages = data.get('messages', [])
                if not messages:
                    return jsonify({"error": "No messages provided"}), 400
                
                # Get the last user message
                user_message = ""
                for msg in reversed(messages):
                    if msg.get('role') == 'user':
                        user_message = msg.get('content', '')
                        break
                
                if not user_message:
                    return jsonify({"error": "No user message found"}), 400
                
                # Process with local Ollama
                local_response = self.process_with_local_ollama(user_message)
                
                if local_response:
                    self.local_responses += 1
                    logger.info(f"✅ Local response #{self.local_responses}")
                    
                    # Format response in Cursor's expected format
                    cursor_response = {
                        "id": f"chatcmpl-{int(time.time())}",
                        "object": "chat.completion",
                        "created": int(time.time()),
                        "model": "local-ollama",
                        "choices": [{
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": local_response
                            },
                            "finish_reason": "stop"
                        }],
                        "usage": {
                            "prompt_tokens": len(user_message.split()),
                            "completion_tokens": len(local_response.split()),
                            "total_tokens": len(user_message.split()) + len(local_response.split())
                        }
                    }
                    
                    return jsonify(cursor_response)
                else:
                    # Fallback to Cursor's original service
                    return self.fallback_to_cursor(data)
                    
            except Exception as e:
                logger.error(f"Chat completions error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/v1/models', methods=['GET'])
        def list_models():
            """List available models"""
            return jsonify({
                "object": "list",
                "data": [
                    {
                        "id": "local-ollama",
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "zombiecoder"
                    }
                ]
            })
        
        @self.app.route('/v1/completions', methods=['POST'])
        def completions():
            """Intercept Cursor's completions requests"""
            try:
                self.request_count += 1
                data = request.get_json()
                
                logger.info(f"📨 Intercepted completions request #{self.request_count}")
                
                prompt = data.get('prompt', '')
                if not prompt:
                    return jsonify({"error": "No prompt provided"}), 400
                
                # Process with local Ollama
                local_response = self.process_with_local_ollama(prompt)
                
                if local_response:
                    self.local_responses += 1
                    
                    # Format response in Cursor's expected format
                    cursor_response = {
                        "id": f"cmpl-{int(time.time())}",
                        "object": "text_completion",
                        "created": int(time.time()),
                        "model": "local-ollama",
                        "choices": [{
                            "index": 0,
                            "text": local_response,
                            "finish_reason": "stop"
                        }],
                        "usage": {
                            "prompt_tokens": len(prompt.split()),
                            "completion_tokens": len(local_response.split()),
                            "total_tokens": len(prompt.split()) + len(local_response.split())
                        }
                    }
                    
                    return jsonify(cursor_response)
                else:
                    # Fallback to Cursor's original service
                    return self.fallback_to_cursor(data)
                    
            except Exception as e:
                logger.error(f"Completions error: {e}")
                return jsonify({"error": str(e)}), 500
        
        # Catch-all route for other Cursor requests
        @self.app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
        @self.app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def catch_all(path):
            """Catch all other requests and forward to Cursor's original service"""
            try:
                # Forward to Cursor's original service
                return self.fallback_to_cursor(request)
            except Exception as e:
                logger.error(f"Catch-all error: {e}")
                return jsonify({"error": str(e)}), 500
    
    def process_with_local_ollama(self, message: str) -> Optional[str]:
        """Process message with local Ollama"""
        try:
            # Select best available model
            model = self.select_best_model()
            if not model:
                logger.warning("No models available in Ollama")
                return None
            
            # Send to Ollama
            response = requests.post(
                f"http://localhost:{self.ports['ollama']}/api/generate",
                json={
                    "model": model,
                    "prompt": message,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                logger.error(f"Ollama error: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("Ollama request timeout")
            return None
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama")
            return None
        except Exception as e:
            logger.error(f"Local Ollama error: {e}")
            return None
    
    def select_best_model(self) -> Optional[str]:
        """Select best available model from Ollama"""
        try:
            response = requests.get(
                f"http://localhost:{self.ports['ollama']}/api/tags",
                timeout=5
            )
            
            if response.status_code == 200:
                models_data = response.json()
                available_models = [model['name'] for model in models_data.get('models', [])]
                
                # Return first available model
                for model_name in ["deepseek-coder:1.3b", "llama2:7b", "llama3.2:1b"]:
                    if model_name in available_models:
                        return model_name
                        
        except Exception as e:
            logger.error(f"Model selection error: {e}")
            
        return None
    
    def fallback_to_cursor(self, data) -> Response:
        """Fallback to Cursor's original service"""
        try:
            self.cursor_responses += 1
            logger.info(f"🔄 Fallback to Cursor #{self.cursor_responses}")
            
            # For now, return a simple response
            # In production, you'd forward to Cursor's actual service
            return jsonify({
                "error": "Local model unavailable, please check Ollama",
                "fallback": True
            }), 503
            
        except Exception as e:
            logger.error(f"Fallback error: {e}")
            return jsonify({"error": str(e)}), 500
    
    def start_monitoring(self):
        """Start system monitoring thread"""
        def monitor():
            while True:
                try:
                    # Log statistics every 60 seconds
                    logger.info(f"📊 Stats: Requests={self.request_count}, Local={self.local_responses}, Fallback={self.cursor_responses}")
                    time.sleep(60)
                    
                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        logger.info("📊 Monitoring started")

def setup_hosts_redirect():
    """Setup hosts file redirect (optional - use with caution)"""
    try:
        # This is a placeholder - in production, you'd modify /etc/hosts
        # to redirect Cursor's API calls to localhost:8080
        logger.info("⚠️  Hosts redirect setup - implement with caution")
        logger.info("💡 Consider using Cursor's proxy settings instead")
        
    except Exception as e:
        logger.error(f"Hosts setup error: {e}")

if __name__ == "__main__":
    interceptor = CursorProxyInterceptor()
    
    logger.info("🚀 Starting Cursor Proxy Interceptor...")
    logger.info(f"🌐 Server running on port {interceptor.ports['interceptor']}")
    logger.info("📝 Cursor requests will be intercepted and redirected to local Ollama")
    logger.info("⚠️  Make sure to configure Cursor to use localhost:8080 as proxy")
    
    # Optional: Setup hosts redirect (use with caution)
    # setup_hosts_redirect()
    
    interceptor.app.run(host='0.0.0.0', port=interceptor.ports['interceptor'], debug=False)
