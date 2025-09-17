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
        
        # Model management - Updated with available models
        self.models = {
            "llama2:7b": {"loaded": False, "memory": 3800, "priority": 1},
            "deepseek-coder:1.3b": {"loaded": False, "memory": 776, "priority": 2},
            "llama3.2:1b": {"loaded": False, "memory": 1300, "priority": 3},
            "qwen2.5-coder:1.5b-base": {"loaded": False, "memory": 986, "priority": 4},
            "codellama:latest": {"loaded": False, "memory": 3800, "priority": 5}
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
        @self.app.before_request
        def _log_local_route():
            try:
                ua = request.headers.get('User-Agent', '-')
                logger.info(
                    f"route=local method={request.method} path={request.path} client={request.remote_addr} ua=\"{ua}\""
                )
            except Exception:
                # logging must never break request handling
                pass

        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint for monitoring"""
            try:
                # Check if Ollama is responding
                ollama_health = requests.get(
                    f"http://localhost:{self.ports['ollama']}/api/tags",
                    timeout=5
                ).status_code == 200
                
                return jsonify({
                    "status": "healthy" if ollama_health else "degraded",
                    "ollama_connected": ollama_health,
                    "active_models": self.system_status['active_models'],
                    "cpu_usage": self.system_status['cpu_usage'],
                    "memory_usage": self.system_status['memory_usage'],
                    "timestamp": time.time()
                }), 200 if ollama_health else 503
                
            except Exception as e:
                logger.error(f"Health check error: {e}")
                return jsonify({
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": time.time()
                }), 503
        
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
        
        @self.app.route('/v1/models', methods=['GET'])
        def list_models_openai():
            """OpenAI-compatible models list, backed by Ollama /api/tags"""
            try:
                resp = requests.get(f"http://localhost:{self.ports['ollama']}/api/tags", timeout=5)
                if resp.status_code != 200:
                    return jsonify({"data": [], "error": "ollama_unavailable"}), 503
                tags = resp.json().get('models', [])
                data = [{
                    "id": m.get('name'),
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "local-ollama"
                } for m in tags]
                return jsonify({"object": "list", "data": data})
            except Exception as e:
                logger.error(f"/v1/models error: {e}")
                return jsonify({"data": [], "error": str(e)}), 503
        
        # Shim: some clients call alternate paths; map them to OpenAI-compatible handlers
        @self.app.route('/openai/v1/models', methods=['GET'])
        @self.app.route('/openai/models', methods=['GET'])
        def list_models_openai_shim():
            return list_models_openai()
        
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
            """Optimized chat with automatic model selection and graceful fallback"""
            try:
                data = request.get_json()
                message = data.get('message', '')
                agent = data.get('agent', 'bhai')
                requested_model = data.get('model')
                
                # Check system health first (more reasonable thresholds)
                if self.system_status['cpu_usage'] > 85 or self.system_status['memory_usage'] > 85:
                    return jsonify({
                        "error": "System overloaded. Please try again later.",
                        "error_type": "system_overload",
                        "system_status": self.system_status,
                        "suggestion": "Wait for system resources to free up"
                    }), 503
                
                # Select model: prefer requested model if available in Ollama; otherwise best available
                best_model = None
                if requested_model:
                    try:
                        tags_resp = requests.get(f"http://localhost:{self.ports['ollama']}/api/tags", timeout=5)
                        if tags_resp.status_code == 200:
                            models_data = tags_resp.json()
                            ollama_models = [m.get('name') for m in models_data.get('models', [])]
                            if requested_model in ollama_models:
                                best_model = requested_model
                    except Exception:
                        pass
                if not best_model:
                best_model = self.select_best_model()
                if not best_model:
                    return jsonify({
                        "error": "No models available. Please load a model first.",
                        "error_type": "no_models",
                        "available_models": [name for name, info in self.models.items() if info["loaded"]],
                        "suggestion": "Use /api/load_model endpoint to load a model"
                    }), 503
                
                # Process with selected model
                response = self.process_with_model(message, best_model, agent)
                
                # Check if response indicates model failure
                if response.startswith("Error:"):
                    return jsonify({
                        "error": "Model processing failed",
                        "error_type": "model_error",
                        "details": response,
                        "model_used": best_model,
                        "suggestion": "Try a different model or check Ollama status"
                    }), 503
                
                return jsonify({
                    "response": response,
                    "model_used": best_model,
                    "system_status": self.system_status,
                    "timestamp": time.time()
                })
                
            except requests.exceptions.Timeout:
                logger.error("Request timeout - model may be overloaded")
                return jsonify({
                    "error": "Request timeout. Model may be overloaded.",
                    "error_type": "timeout",
                    "suggestion": "Try again with a shorter message or wait a moment"
                }), 504
                
            except requests.exceptions.ConnectionError:
                logger.error("Connection error - Ollama may be down")
                return jsonify({
                    "error": "Cannot connect to local AI model.",
                    "error_type": "connection_error",
                    "suggestion": "Check if Ollama is running on port 11434"
                }), 503
                
            except Exception as e:
                logger.error(f"Chat error: {e}")
                return jsonify({
                    "error": "Internal server error",
                    "error_type": "internal_error",
                    "details": str(e),
                    "suggestion": "Check server logs for more details"
                }), 500

        @self.app.route('/v1/chat/completions', methods=['POST'])
        def openai_chat_completions():
            """Minimal OpenAI-compatible endpoint for Cursor. Non-streaming."""
            try:
                body = request.get_json(force=True)
                model = body.get('model')
                messages = body.get('messages', [])
                temperature = body.get('temperature', 0.7)
                # Build prompt from messages (simple join of user/assistant turns)
                prompt_parts = []
                for m in messages:
                    role = m.get('role', 'user')
                    content = m.get('content', '')
                    prompt_parts.append(f"[{role}] {content}")
                prompt = "\n".join(prompt_parts)

                # Prefer requested model if present; else fall back
                selected_model = None
                if model:
                    try:
                        r = requests.get(f"http://localhost:{self.ports['ollama']}/api/tags", timeout=5)
                        if r.status_code == 200:
                            names = [m.get('name') for m in r.json().get('models', [])]
                            if model in names:
                                selected_model = model
                    except Exception:
                        pass
                if not selected_model:
                    selected_model = self.select_best_model()
                if not selected_model:
                    return jsonify({
                        "error": {"message": "No local models available", "type": "model_unavailable"}
                    }), 503

                # Call Ollama generate (non-streaming)
                gen = requests.post(
                    f"http://localhost:{self.ports['ollama']}/api/generate",
                    json={
                        "model": selected_model,
                        "prompt": prompt,
                        "options": {"temperature": temperature},
                        "stream": False
                    },
                    timeout=60
                )
                if gen.status_code != 200:
                    return jsonify({
                        "error": {"message": gen.text, "type": "ollama_error"}
                    }), 502
                resp_json = gen.json()
                text = resp_json.get('response', '')
                now = int(time.time())
                openai_shape = {
                    "id": f"chatcmpl-local-{now}",
                    "object": "chat.completion",
                    "created": now,
                    "model": selected_model,
                    "choices": [{
                        "index": 0,
                        "message": {"role": "assistant", "content": text},
                        "finish_reason": "stop"
                    }],
                    "usage": {"prompt_tokens": None, "completion_tokens": None, "total_tokens": None}
                }
                return jsonify(openai_shape)
            except requests.exceptions.Timeout:
                return jsonify({
                    "error": {"message": "Local model timeout", "type": "timeout"}
                }), 504
            except Exception as e:
                logger.error(f"/v1/chat/completions error: {e}")
                return jsonify({
                    "error": {"message": str(e), "type": "internal_error"}
                }), 500

        # Shim routes for chat completions that some clients may use
        @self.app.route('/openai/v1/chat/completions', methods=['POST'])
        @self.app.route('/openai/chat/completions', methods=['POST'])
        @self.app.route('/chat/completions', methods=['POST'])
        def openai_chat_completions_shim():
            return openai_chat_completions()

        @self.app.route('/v1/embeddings', methods=['POST'])
        def openai_embeddings():
            """OpenAI-compatible embeddings endpoint backed by Ollama /api/embeddings.
            Accepts { model, input } where input can be a string or an array of strings.
            Returns { data: [{embedding: [...]}, ...], model, object } similar to OpenAI.
            """
            try:
                body = request.get_json(force=True)
                model = body.get('model')
                input_data = body.get('input', "")

                # Normalize inputs to a list of strings
                if isinstance(input_data, list):
                    inputs = [str(x) for x in input_data]
                else:
                    inputs = [str(input_data)]

                # Choose model if not explicitly available
                selected_model = None
                if model:
                    try:
                        r = requests.get(f"http://localhost:{self.ports['ollama']}/api/tags", timeout=5)
                        if r.status_code == 200:
                            names = [m.get('name') for m in r.json().get('models', [])]
                            if model in names:
                                selected_model = model
                    except Exception:
                        pass
                if not selected_model:
                    selected_model = self.select_best_model()
                if not selected_model:
                    return jsonify({
                        "error": {"message": "No local models available", "type": "model_unavailable"}
                    }), 503

                data_items = []
                for idx, text in enumerate(inputs):
                    resp = requests.post(
                        f"http://localhost:{self.ports['ollama']}/api/embeddings",
                        json={"model": selected_model, "prompt": text},
                        timeout=60
                    )
                    if resp.status_code != 200:
                        return jsonify({
                            "error": {"message": resp.text, "type": "ollama_error"}
                        }), 502
                    emb_json = resp.json()
                    vector = emb_json.get('embedding') or emb_json.get('vector') or []
                    data_items.append({
                        "object": "embedding",
                        "index": idx,
                        "embedding": vector
                    })

                return jsonify({
                    "object": "list",
                    "data": data_items,
                    "model": selected_model
                })
            except requests.exceptions.Timeout:
                return jsonify({
                    "error": {"message": "Local embeddings timeout", "type": "timeout"}
                }), 504
            except Exception as e:
                logger.error(f"/v1/embeddings error: {e}")
                return jsonify({
                    "error": {"message": str(e), "type": "internal_error"}
                }), 500

        # Shim routes for embeddings
        @self.app.route('/openai/v1/embeddings', methods=['POST'])
        @self.app.route('/openai/embeddings', methods=['POST'])
        def openai_embeddings_shim():
            return openai_embeddings()
    
    def load_model_safely(self, model_name: str) -> bool:
        """Safely load model without overwhelming system"""
        try:
            if model_name not in self.models:
                logger.error(f"Unknown model: {model_name}")
                return False
            
            if self.models[model_name]["loaded"]:
                logger.info(f"Model {model_name} already loaded")
                return True
            
            # Check memory availability with proper unit conversion (MB -> % of total)
            required_memory_mb = self.models[model_name]["memory"]
            current_memory_percent = self.system_status['memory_usage']
            try:
                import psutil
                total_mb = psutil.virtual_memory().total / (1024 * 1024)
                required_percent = (required_memory_mb / total_mb) * 100.0 if total_mb else 0.0
            except Exception:
                # If psutil fails, fall back to lenient check
                required_percent = 0.0
            # Allow up to 90% projected usage
            if current_memory_percent + required_percent > 90:
                logger.warning(
                    f"Insufficient memory for {model_name} (current: {current_memory_percent}%, requires ~{required_percent:.2f}% of RAM)"
                )
                return False
            
            # Check if model exists in Ollama
            response = requests.get(
                f"http://localhost:{self.ports['ollama']}/api/tags",
                timeout=10
            )
            
            if response.status_code == 200:
                models_data = response.json()
                available_models = [model['name'] for model in models_data.get('models', [])]
                
                if model_name in available_models:
                    # Model exists, mark as loaded
                self.models[model_name]["loaded"] = True
                self.system_status['active_models'] += 1
                logger.info(f"Model {model_name} loaded successfully")
                return True
            else:
                    logger.error(f"Model {model_name} not found in Ollama. Available: {available_models}")
                    return False
            else:
                logger.error(f"Failed to check Ollama models: {response.text}")
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
            # Use available models directly (they're already in Ollama)
            # Check which models are actually available in Ollama
            try:
                response = requests.get(f"http://localhost:{self.ports['ollama']}/api/tags", timeout=5)
                if response.status_code == 200:
                    models_data = response.json()
                    ollama_models = [model['name'] for model in models_data.get('models', [])]
                    
                    # Return first available model
                    for model_name in ["deepseek-coder:1.3b", "llama2:7b"]:
                        if model_name in ollama_models:
                            return model_name
            except:
                pass
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
                logger.error(f"Ollama error: {response.text}")
                return f"Error: {response.text}"
                
        except requests.exceptions.Timeout:
            logger.error("Ollama request timeout")
            return "Error: Request timeout - model may be overloaded"
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama")
            return "Error: Cannot connect to local AI model"
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
                    # Get CPU usage with interval to avoid 100% false readings
                    self.system_status['cpu_usage'] = psutil.cpu_percent(interval=0.1)
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
