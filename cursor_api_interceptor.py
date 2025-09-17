#!/usr/bin/env python3
"""
ZombieCoder Cursor API Interceptor
==================================
This server intercepts Cursor extension API calls and redirects them to local ZombieCoder agents.
No limits, no tracking, pure local AI power!
"""

import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import threading
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# ZombieCoder local endpoints
ZOMBIECODER_ENDPOINTS = {
    'main_agent': 'http://localhost:12345',
    'truth_checker': 'http://localhost:8002',
    'advanced_agent': 'http://localhost:8004',
    'editor_integration': 'http://localhost:8003',
    'multi_project': 'http://localhost:8001'
}

class CursorAPIInterceptor:
    def __init__(self):
        self.request_count = 0
        self.start_time = time.time()
        
    def get_stats(self):
        uptime = time.time() - self.start_time
        return {
            "requests_intercepted": self.request_count,
            "uptime_seconds": uptime,
            "status": "active",
            "zombiecoder_agents": len(ZOMBIECODER_ENDPOINTS)
        }
    
    def intercept_chat_completion(self, data):
        """Intercept /v1/chat/completions calls"""
        self.request_count += 1
        
        try:
            # Forward to ZombieCoder main agent
            response = requests.post(
                f"{ZOMBIECODER_ENDPOINTS['main_agent']}/chat",
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._create_fallback_response(data)
                
        except Exception as e:
            logger.error(f"Error intercepting chat completion: {e}")
            return self._create_fallback_response(data)
    
    def _create_fallback_response(self, data):
        """Create a fallback response when ZombieCoder is not available"""
        return {
            "id": f"zombiecoder-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "zombiecoder-local",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "ZombieCoder Agent (সাহন ভাই) is temporarily unavailable. Please check local services."
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }

interceptor = CursorAPIInterceptor()

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """Intercept OpenAI-style chat completions"""
    logger.info("Intercepted chat completion request")
    data = request.get_json()
    return jsonify(interceptor.intercept_chat_completion(data))

@app.route('/v1/models', methods=['GET'])
def list_models():
    """Intercept model listing requests"""
    logger.info("Intercepted models list request")
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": "zombiecoder-agent",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "zombiecoder-local"
            }
        ]
    })

@app.route('/v1/embeddings', methods=['POST'])
def embeddings():
    """Intercept embedding requests"""
    logger.info("Intercepted embedding request")
    return jsonify({
        "object": "list",
        "data": [{
            "object": "embedding",
            "index": 0,
            "embedding": [0.0] * 1536  # Dummy embedding
        }],
        "model": "zombiecoder-embeddings",
        "usage": {
            "prompt_tokens": 0,
            "total_tokens": 0
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify(interceptor.get_stats())

@app.route('/stats', methods=['GET'])
def stats():
    """Statistics endpoint"""
    return jsonify(interceptor.get_stats())

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        "message": "ZombieCoder Cursor API Interceptor",
        "status": "active",
        "intercepted_requests": interceptor.request_count,
        "zombiecoder_agents": list(ZOMBIECODER_ENDPOINTS.keys())
    })

def start_interceptor():
    """Start the interceptor server"""
    logger.info("🧟 Starting ZombieCoder Cursor API Interceptor...")
    logger.info("📍 Intercepting Cursor extension API calls...")
    logger.info("🔒 No limits, no tracking, pure local AI!")
    
app.run(
    host='127.0.0.1',
    port=8443,  # এখন non-privileged port
    debug=False,
    threaded=True
)

if __name__ == '__main__':
    start_interceptor()
