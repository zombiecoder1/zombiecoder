#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ZombieCoder Proxy Server
Intercepts Cursor API calls and redirects to local agents
"""

import os
import json
import time
import logging
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any, Optional
from unified_agent_system import unified_agent

logger = logging.getLogger(__name__)

class CursorProxy:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.port = 8080
        self.local_agent = unified_agent
        
        # Cursor API endpoints to intercept
        self.cursor_endpoints = [
            "api.openai.com",
            "api.anthropic.com", 
            "api.together.xyz",
            "api-inference.huggingface.co"
        ]
        
        # Setup routes
        self.setup_routes()
    
    def setup_routes(self):
        """Setup proxy routes"""
        
        @self.app.route('/proxy/chat', methods=['POST'])
        def proxy_chat():
            """Intercept chat requests"""
            try:
                data = request.get_json()
                logger.info(f"Intercepted chat request: {data}")
                
                # Extract message from Cursor format
                message = self.extract_message(data)
                if not message:
                    return jsonify({"error": "No message found"}), 400
                
                # Process with local agent
                response = self.local_agent.process_message(message)
                
                # Format response for Cursor
                cursor_response = self.format_for_cursor(response)
                
                logger.info(f"Local agent response: {cursor_response}")
                return jsonify(cursor_response)
                
            except Exception as e:
                logger.error(f"Proxy error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/proxy/completion', methods=['POST'])
        def proxy_completion():
            """Intercept completion requests"""
            try:
                data = request.get_json()
                logger.info(f"Intercepted completion request: {data}")
                
                # Extract prompt from Cursor format
                prompt = self.extract_prompt(data)
                if not prompt:
                    return jsonify({"error": "No prompt found"}), 400
                
                # Process with local agent
                response = self.local_agent.process_message(prompt)
                
                # Format response for Cursor
                cursor_response = self.format_completion_for_cursor(response)
                
                logger.info(f"Local agent completion: {cursor_response}")
                return jsonify(cursor_response)
                
            except Exception as e:
                logger.error(f"Proxy completion error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/proxy/status', methods=['GET'])
        def proxy_status():
            """Proxy status endpoint"""
            return jsonify({
                "status": "active",
                "proxy": "cursor",
                "local_agent": self.local_agent.name,
                "timestamp": time.time()
            })
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint for monitoring"""
            try:
                # Check if local agent is responsive
                agent_status = "healthy" if hasattr(self.local_agent, 'name') else "unhealthy"
                
                return jsonify({
                    "status": "healthy",
                    "service": "proxy_server",
                    "agent_status": agent_status,
                    "uptime": time.time(),
                    "version": "1.0.0",
                    "endpoints": {
                        "proxy_chat": "/proxy/chat",
                        "proxy_completion": "/proxy/completion",
                        "proxy_status": "/proxy/status",
                        "health_check": "/health",
                        "force_local": "/proxy/force-local",
                        "truth_check": "/proxy/truth-check"
                    },
                    "timestamp": time.time()
                }), 200
                
            except Exception as e:
                logger.error(f"Health check error: {e}")
                return jsonify({
                    "status": "unhealthy",
                    "service": "proxy_server",
                    "error": str(e),
                    "timestamp": time.time()
                }), 503
        
        @self.app.route('/health/detailed', methods=['GET'])
        def detailed_health():
            """Detailed health check with system metrics"""
            try:
                import psutil
                
                # System metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # Agent metrics
                agent_metrics = {
                    "name": getattr(self.local_agent, 'name', 'unknown'),
                    "status": "active" if hasattr(self.local_agent, 'name') else "inactive",
                    "last_response": getattr(self.local_agent, 'last_response_time', 0)
                }
                
                return jsonify({
                    "status": "healthy",
                    "service": "proxy_server",
                    "system_metrics": {
                        "cpu_percent": cpu_percent,
                        "memory_percent": memory.percent,
                        "memory_available_gb": round(memory.available / (1024**3), 2),
                        "disk_percent": disk.percent,
                        "disk_free_gb": round(disk.free / (1024**3), 2)
                    },
                    "agent_metrics": agent_metrics,
                    "active_connections": len(self.app.url_map._rules),
                    "uptime_seconds": time.time(),
                    "timestamp": time.time()
                }), 200
                
            except Exception as e:
                logger.error(f"Detailed health check error: {e}")
                return jsonify({
                    "status": "unhealthy",
                    "service": "proxy_server",
                    "error": str(e),
                    "timestamp": time.time()
                }), 503
        
        @self.app.route('/proxy/force-local', methods=['POST'])
        def force_local():
            """Force local AI mode"""
            try:
                data = request.get_json()
                logger.info(f"Force local request: {data}")
                
                # Extract message
                message = self.extract_message(data)
                if not message:
                    return jsonify({"error": "No message found"}), 400
                
                # Force local AI processing
                response = self.local_agent.process_message(message, {"force_local": True})
                
                # Format response
                cursor_response = self.format_for_cursor(response)
                
                logger.info(f"Force local response: {cursor_response}")
                return jsonify(cursor_response)
                
            except Exception as e:
                logger.error(f"Force local error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/proxy/truth-check', methods=['POST'])
        def truth_check():
            """Truth verification endpoint"""
            try:
                data = request.get_json()
                logger.info(f"Truth check request: {data}")
                
                # Extract message and response
                message = data.get("message", "")
                response_text = data.get("response", "")
                context = data.get("context", {})
                
                if not message or not response_text:
                    return jsonify({"error": "Message and response required"}), 400
                
                # Verify truth
                verification = self.local_agent.verify_truth(response_text, {
                    "message": message,
                    "context": context
                })
                
                result = {
                    "verified": verification.get("verified", False),
                    "confidence": verification.get("confidence", 0.0),
                    "warnings": verification.get("warnings", []),
                    "evidence": verification.get("evidence", []),
                    "timestamp": time.time()
                }
                
                logger.info(f"Truth check result: {result}")
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Truth check error: {e}")
                return jsonify({"error": str(e)}), 500
    
    def extract_message(self, data: Dict[str, Any]) -> Optional[str]:
        """Extract message from Cursor API format"""
        try:
            # Cursor chat format
            if "messages" in data:
                messages = data["messages"]
                if messages and len(messages) > 0:
                    return messages[-1].get("content", "")
            
            # Cursor completion format
            if "prompt" in data:
                return data["prompt"]
            
            # Direct message
            if "message" in data:
                return data["message"]
            
            return None
        except Exception as e:
            logger.error(f"Message extraction error: {e}")
            return None
    
    def extract_prompt(self, data: Dict[str, Any]) -> Optional[str]:
        """Extract prompt from Cursor completion format"""
        try:
            if "prompt" in data:
                return data["prompt"]
            
            if "messages" in data:
                messages = data["messages"]
                if messages:
                    return messages[-1].get("content", "")
            
            return None
        except Exception as e:
            logger.error(f"Prompt extraction error: {e}")
            return None
    
    def format_for_cursor(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Format local agent response for Cursor"""
        try:
            return {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": response.get("response", "No response")
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                },
                "model": "zombiecoder-local",
                "object": "chat.completion",
                "created": int(time.time()),
                "id": f"local-{int(time.time())}",
                "local_agent": response.get("agent", "unknown"),
                "capability": response.get("capability", "general"),
                "source": response.get("source", "local"),
                "latency": response.get("timestamp", 0)
            }
        except Exception as e:
            logger.error(f"Cursor formatting error: {e}")
            return {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": "Error formatting response"
                    },
                    "finish_reason": "stop"
                }]
            }
    
    def format_completion_for_cursor(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Format completion response for Cursor"""
        try:
            return {
                "choices": [{
                    "text": response.get("response", "No response"),
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                },
                "model": "zombiecoder-local",
                "object": "text_completion",
                "created": int(time.time()),
                "id": f"local-completion-{int(time.time())}",
                "local_agent": response.get("agent", "unknown"),
                "capability": response.get("capability", "general"),
                "source": response.get("source", "local")
            }
        except Exception as e:
            logger.error(f"Completion formatting error: {e}")
            return {
                "choices": [{
                    "text": "Error formatting completion",
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "stop"
                }]
            }
    
    def should_intercept(self, url: str) -> bool:
        """Check if URL should be intercepted"""
        return any(endpoint in url for endpoint in self.cursor_endpoints)
    
    def start(self):
        """Start proxy server"""
        logger.info(f"🚀 Starting Cursor Proxy Server on port {self.port}")
        logger.info(f"📡 Intercepting endpoints: {self.cursor_endpoints}")
        logger.info(f"🤖 Local Agent: {self.local_agent.name}")
        
        try:
            self.app.run(host='0.0.0.0', port=self.port, debug=False)
        except Exception as e:
            logger.error(f"Proxy server error: {e}")

# Global instance
cursor_proxy = CursorProxy()

if __name__ == "__main__":
    cursor_proxy.start()
