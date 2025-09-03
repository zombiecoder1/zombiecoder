#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ZombieCoder OpenAI Shim Server
==================================

This server provides OpenAI-compatible API endpoints that route to local AI models:
- ZombieCoder Agent System (port 12345)
- Ollama Models (port 11434)
- Fallback dummy responses when models are offline

Features:
- 100% Local AI - No cloud calls
- Auto-fallback system
- Memory integration with ZombieCoder
- Cursor IDE compatibility
"""

import time
import uuid
import json
import requests
import logging
import threading
import psutil
from datetime import datetime
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

# ===============================
# Configuration
# ===============================
LOCAL_AI_CONFIG = {
    "zombiecoder": {
        "name": "ZombieCoder Agent System",
        "chat_endpoint": "http://127.0.0.1:12345/chat",
        "status_endpoint": "http://127.0.0.1:12345/status",
        "type": "zombie",
        "enabled": True
    },
    "ollama": {
        "name": "Ollama Models",
        "chat_endpoint": "http://127.0.0.1:11434/api/chat",
        "models_endpoint": "http://127.0.0.1:11434/api/tags",
        "type": "ollama",
        "enabled": True
    }
}

# Available models for fallback
FALLBACK_MODELS = [
    "deepseek-coder:latest",
    "llama3.2:1b", 
    "codellama:latest",
    "qwen2.5-coder:1.5b-base"
]

# ===============================
# Setup
# ===============================
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Memory cleanup configuration
MEMORY_CLEANUP_THRESHOLD = 3500  # MB (3.5GB - more reasonable)
MEMORY_CLEANUP_INTERVAL = 180    # seconds (3 minutes - more frequent)
CLEANUP_ENABLED = True

# ===============================
# Helper Functions
# ===============================

def get_ollama_memory_usage():
    """Get Ollama memory usage in MB"""
    try:
        # Find Ollama process
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            if 'ollama' in proc.info['name'].lower():
                memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
                return memory_mb
        return 0
    except Exception as e:
        logger.warning(f"Could not get Ollama memory usage: {e}")
        return 0

def cleanup_ollama_memory():
    """Cleanup Ollama memory if threshold exceeded"""
    if not CLEANUP_ENABLED:
        return
    
    try:
        memory_mb = get_ollama_memory_usage()
        if memory_mb > MEMORY_CLEANUP_THRESHOLD:
            logger.warning(f"⚠️ Ollama using {memory_mb:.1f}MB memory - starting cleanup")
            
            # Try gentle cleanup first (model unloading)
            try:
                import subprocess
                # Unload models to free memory
                subprocess.run(['ollama', 'rm', 'deepseek-coder:latest'], 
                             capture_output=True, timeout=10)
                logger.info("🧹 Unloaded deepseek-coder model to free memory")
                
                # Wait a bit for memory to free up
                time.sleep(5)
                
                # Reload the model
                subprocess.run(['ollama', 'pull', 'deepseek-coder:latest'], 
                             capture_output=True, timeout=60)
                logger.info("🔄 Reloaded deepseek-coder model")
                
            except Exception as e:
                logger.warning(f"Gentle cleanup failed, trying restart: {e}")
                
                # Fallback to restart if gentle cleanup fails
                try:
                    subprocess.run(['taskkill', '/f', '/im', 'ollama.exe'], 
                                 capture_output=True, shell=True)
                    time.sleep(3)
                    
                    subprocess.Popen(['ollama', 'serve'], 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
                    logger.info("✅ Ollama restart completed")
                    
                except Exception as restart_error:
                    logger.error(f"❌ Ollama restart failed: {restart_error}")
                
    except Exception as e:
        logger.error(f"Memory cleanup error: {e}")

def start_memory_cleanup_thread():
    """Start background memory cleanup thread"""
    def cleanup_worker():
        while True:
            try:
                cleanup_ollama_memory()
                time.sleep(MEMORY_CLEANUP_INTERVAL)
            except Exception as e:
                logger.error(f"Cleanup worker error: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
    cleanup_thread.start()
    logger.info("🧹 Memory cleanup thread started")

def get_system_status():
    """Get current system status"""
    status = {
        "timestamp": datetime.now().isoformat(),
        "server": "ZombieCoder OpenAI Shim",
        "version": "1.0.0",
        "status": "active"
    }
    
    # Check backend services
    for name, config in LOCAL_AI_CONFIG.items():
        if config["enabled"]:
            try:
                response = requests.get(config["status_endpoint"], timeout=10)
                status[name] = {
                    "status": "online" if response.status_code == 200 else "offline",
                    "response_time": response.elapsed.total_seconds()
                }
            except Exception as e:
                status[name] = {"status": "offline", "error": str(e)}
    
    return status

def call_zombiecoder_backend(payload):
    """Call ZombieCoder Agent System"""
    try:
        # Prepare payload for ZombieCoder
        zombie_payload = {
            "message": payload.get("prompt", ""),
            "agent": "সাহন ভাই",  # Default agent
            "model": payload.get("model", "deepseek-coder:latest")
        }
        
        # If messages array provided, extract content
        if "messages" in payload:
            user_messages = [msg["content"] for msg in payload["messages"] if msg["role"] == "user"]
            if user_messages:
                zombie_payload["message"] = " ".join(user_messages)
        
        response = requests.post(
            LOCAL_AI_CONFIG["zombiecoder"]["chat_endpoint"],
            json=zombie_payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            # Extract response text from various possible fields
            reply = (
                result.get("reply") or 
                result.get("response") or 
                result.get("text") or 
                result.get("message") or
                str(result)
            )
            
            # Add "ভাইয়া" prefix to response
            if reply and not reply.startswith("ভাইয়া"):
                reply = f"ভাইয়া, {reply}"
            
            return reply if reply else None
            
    except Exception as e:
        logger.error(f"ZombieCoder backend error: {e}")
        return None
    
    return None

def call_ollama_backend(payload):
    """Call Ollama Models"""
    try:
        # Prepare payload for Ollama
        model = payload.get("model", "deepseek-coder:latest")
        
        # Convert OpenAI format to Ollama format
        messages = []
        if "messages" in payload:
            messages = payload["messages"]
        elif "prompt" in payload:
            messages = [{"role": "user", "content": payload["prompt"]}]
        
        ollama_payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        response = requests.post(
            LOCAL_AI_CONFIG["ollama"]["chat_endpoint"],
            json=ollama_payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            # Extract response from Ollama format
            reply = (
                result.get("message", {}).get("content") or
                result.get("response") or
                str(result)
            )
            
            # Add "ভাইয়া" prefix to response
            if reply and not reply.startswith("ভাইয়া"):
                reply = f"ভাইয়া, {reply}"
            
            return reply if reply else None
            
    except Exception as e:
        logger.error(f"Ollama backend error: {e}")
        return None
    
    return None

def generate_fallback_response(payload):
    """Generate fallback response when backends are offline"""
    model = payload.get("model", "local-fallback")
    
    # Create helpful fallback message
    fallback_content = f"""🤖 **ZombieCoder Local AI Shim Active**

I'm running locally on your machine, but the AI models are currently offline.

**Available Models:**
{chr(10).join([f"- {model}" for model in FALLBACK_MODELS])}

**To get real AI responses:**
1. Start Ollama: `ollama serve`
2. Start ZombieCoder: `python core-server/advanced_agent_system.py`
3. Or use the GLOBAL_LAUNCHER.bat

**Current Request:**
- Model: {model}
- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

I'll automatically switch to real AI responses once the models are online! 🚀"""

    return {
        "id": f"fallback-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": fallback_content
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": len(str(payload)),
            "completion_tokens": len(fallback_content.split()),
            "total_tokens": len(str(payload)) + len(fallback_content.split())
        }
    }

def call_local_backend(payload):
    """Try all available backends and fallback if needed"""
    logger.info(f"Processing request for model: {payload.get('model', 'unknown')}")
    
    # Try Ollama first (higher priority for direct model access)
    if LOCAL_AI_CONFIG["ollama"]["enabled"]:
        response = call_ollama_backend(payload)
        if response:
            logger.info("✅ Ollama backend responded")
            return response
    
    # Try ZombieCoder as fallback
    if LOCAL_AI_CONFIG["zombiecoder"]["enabled"]:
        response = call_zombiecoder_backend(payload)
        if response:
            logger.info("✅ ZombieCoder backend responded")
            return response
    
    # Fallback response
    logger.info("⚠️ Using fallback response - no backends available")
    return None

# ===============================
# API Endpoints
# ===============================

@app.route("/", methods=["GET"])
def home():
    """Home endpoint"""
    return jsonify({
        "message": "🚀 ZombieCoder OpenAI Shim Server",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "/v1/models": "List available models",
            "/v1/chat/completions": "Chat completion endpoint",
            "/health": "System health check",
            "/status": "Detailed system status"
        },
        "backends": {name: "enabled" for name, config in LOCAL_AI_CONFIG.items()}
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": "ZombieCoder OpenAI Shim"
    })

@app.route("/status", methods=["GET"])
def status():
    """Detailed system status"""
    return jsonify(get_system_status())

@app.route("/v1/models", methods=["GET"])
def models():
    """List available models"""
    try:
        # Try to get models from Ollama
        if LOCAL_AI_CONFIG["ollama"]["enabled"]:
            response = requests.get(
                LOCAL_AI_CONFIG["ollama"]["models_endpoint"],
                timeout=3
            )
            if response.status_code == 200:
                ollama_models = response.json()
                models_data = [
                    {"id": model["name"], "object": "model", "source": "ollama"}
                    for model in ollama_models.get("models", [])
                ]
                logger.info(f"✅ Found {len(models_data)} Ollama models")
                return jsonify({
                    "object": "list",
                    "data": models_data
                })
    except Exception as e:
        logger.warning(f"Could not fetch Ollama models: {e}")
    
    # Fallback to static models
    fallback_data = [
        {"id": model, "object": "model", "source": "fallback"}
        for model in FALLBACK_MODELS
    ]
    
    logger.info(f"📋 Using fallback models: {len(fallback_data)}")
    return jsonify({
        "object": "list",
        "data": fallback_data
    })

@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    """Chat completion endpoint"""
    try:
        # Parse request
        payload = request.get_json(force=True, silent=True) or {}
        
        # Validate required fields
        if not payload.get("messages") and not payload.get("prompt"):
            return jsonify({
                "error": {
                    "message": "Either 'messages' or 'prompt' is required",
                    "type": "invalid_request_error"
                }
            }), 400
        
        # Try local backends
        response = call_local_backend(payload)
        
        if response:
            # Real AI response
            now = int(time.time())
            return jsonify({
                "id": f"chatcmpl-local-{uuid.uuid4().hex[:12]}",
                "object": "chat.completion",
                "created": now,
                "model": payload.get("model", "local-model"),
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": response},
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": len(str(payload)),
                    "completion_tokens": len(response.split()),
                    "total_tokens": len(str(payload)) + len(response.split())
                }
            })
        else:
            # Fallback response
            fallback = generate_fallback_response(payload)
            return jsonify(fallback)
            
    except Exception as e:
        logger.error(f"Chat completion error: {e}")
        return jsonify({
            "error": {
                "message": f"Internal server error: {str(e)}",
                "type": "internal_error"
            }
        }), 500

# ===============================
# Main
# ===============================

if __name__ == "__main__":
    logger.info("🚀 Starting ZombieCoder OpenAI Shim Server...")
    logger.info(f"📡 Available backends: {list(LOCAL_AI_CONFIG.keys())}")
    logger.info("🌐 Server will run on http://127.0.0.1:8001")
    logger.info("🔗 OpenAI API: http://127.0.0.1:8001/v1")
    
    # Start memory cleanup thread
    start_memory_cleanup_thread()
    
    try:
        app.run(
            host="127.0.0.1",
            port=8001,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
