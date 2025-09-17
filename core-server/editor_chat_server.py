#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 Editor Chat Server for ZombieCoder
Enhanced editor integration with proper chat endpoints
"""

import os
import json
import time
import logging
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any, Optional
from datetime import datetime

# Import unified agent system
from unified_agent_system import unified_agent

logger = logging.getLogger(__name__)

class EditorChatServer:
    """Enhanced editor chat server with proper endpoints"""
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.port = 8003
        self.unified_agent = unified_agent
        
        # Editor-specific capabilities
        self.capabilities = {
            "code_generation": "Generate code snippets and functions",
            "code_review": "Review and improve existing code",
            "bug_fixing": "Identify and fix bugs",
            "architecture": "Design system architecture",
            "documentation": "Generate documentation",
            "testing": "Create test cases and test code",
            "refactoring": "Improve code structure and performance",
            "debugging": "Help debug issues and errors"
        }
        
        # Setup routes
        self.setup_routes()
        
        # Memory storage for editor context
        self.memory = {}
    
    def setup_routes(self):
        """Setup all editor endpoints"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                "service": "editor_integration",
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "capabilities": list(self.capabilities.keys()),
                "memory_entries": len(self.memory)
            })
        
        @self.app.route('/status', methods=['GET'])
        def status():
            """Status endpoint with detailed information"""
            return jsonify({
                "service": "editor_chat_server",
                "status": "active",
                "port": self.port,
                "agent": self.unified_agent.name,
                "capabilities": self.capabilities,
                "memory_count": len(self.memory),
                "uptime": time.time(),
                "timestamp": datetime.now().isoformat()
            })
        
        @self.app.route('/capabilities', methods=['GET'])
        def get_capabilities():
            """Get available capabilities"""
            return jsonify({
                "capabilities": self.capabilities,
                "total_capabilities": len(self.capabilities),
                "timestamp": datetime.now().isoformat()
            })
        
        @self.app.route('/chat', methods=['POST'])
        def chat():
            """Main chat endpoint for editor integration"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400
                
                message = data.get("message", "")
                context = data.get("context", {})
                
                if not message:
                    return jsonify({"error": "No message provided"}), 400
                
                logger.info(f"Editor chat request: {message[:100]}...")
                
                # Process with unified agent
                response = self.unified_agent.process_message(message, context)
                
                # Store in memory for context
                memory_key = f"chat_{int(time.time())}"
                self.memory[memory_key] = {
                    "message": message,
                    "context": context,
                    "response": response,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Format response for editor
                editor_response = {
                    "response": response.get("response", "No response"),
                    "agent": response.get("agent", "unknown"),
                    "capability": response.get("capability", "general"),
                    "source": response.get("source", "local"),
                    "timestamp": response.get("timestamp", time.time()),
                    "memory_key": memory_key,
                    "context_used": context
                }
                
                logger.info(f"Editor chat response: {editor_response['response'][:100]}...")
                return jsonify(editor_response)
                
            except Exception as e:
                logger.error(f"Editor chat error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/code/generate', methods=['POST'])
        def generate_code():
            """Generate code based on requirements"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400
                
                requirements = data.get("requirements", "")
                language = data.get("language", "python")
                context = data.get("context", {})
                
                if not requirements:
                    return jsonify({"error": "No requirements provided"}), 400
                
                message = f"Generate {language} code for: {requirements}"
                
                response = self.unified_agent.process_message(message, {
                    **context,
                    "capability": "code_generation",
                    "language": language
                })
                
                return jsonify({
                    "code": response.get("response", ""),
                    "language": language,
                    "requirements": requirements,
                    "agent": response.get("agent", "unknown"),
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Code generation error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/code/review', methods=['POST'])
        def review_code():
            """Review and improve code"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400
                
                code = data.get("code", "")
                language = data.get("language", "python")
                focus_areas = data.get("focus_areas", ["quality", "performance", "security"])
                
                if not code:
                    return jsonify({"error": "No code provided"}), 400
                
                message = f"Review this {language} code and suggest improvements:\n\n```{language}\n{code}\n```\n\nFocus on: {', '.join(focus_areas)}"
                
                response = self.unified_agent.process_message(message, {
                    "capability": "code_review",
                    "language": language,
                    "focus_areas": focus_areas
                })
                
                return jsonify({
                    "review": response.get("response", ""),
                    "language": language,
                    "focus_areas": focus_areas,
                    "agent": response.get("agent", "unknown"),
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Code review error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/bug/fix', methods=['POST'])
        def fix_bug():
            """Fix bugs in code"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400
                
                error_message = data.get("error", "")
                code = data.get("code", "")
                language = data.get("language", "python")
                
                if not error_message:
                    return jsonify({"error": "No error message provided"}), 400
                
                message = f"Fix this {language} error: {error_message}\n\nCode:\n```{language}\n{code}\n```"
                
                response = self.unified_agent.process_message(message, {
                    "capability": "bug_fixing",
                    "language": language,
                    "error_type": "runtime"
                })
                
                return jsonify({
                    "fix": response.get("response", ""),
                    "language": language,
                    "error": error_message,
                    "agent": response.get("agent", "unknown"),
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Bug fix error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/memory/store', methods=['POST'])
        def store_memory():
            """Store information in memory"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400
                
                key = data.get("key", f"memory_{int(time.time())}")
                value = data.get("value", {})
                
                self.memory[key] = {
                    "value": value,
                    "timestamp": datetime.now().isoformat(),
                    "type": data.get("type", "general")
                }
                
                return jsonify({
                    "key": key,
                    "stored": True,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Memory store error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/memory/retrieve', methods=['POST'])
        def retrieve_memory():
            """Retrieve information from memory"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400
                
                key = data.get("key", "")
                
                if key in self.memory:
                    return jsonify({
                        "key": key,
                        "value": self.memory[key]["value"],
                        "timestamp": self.memory[key]["timestamp"],
                        "found": True
                    })
                else:
                    return jsonify({
                        "key": key,
                        "found": False,
                        "available_keys": list(self.memory.keys())
                    })
                
            except Exception as e:
                logger.error(f"Memory retrieve error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/memory/list', methods=['GET'])
        def list_memory():
            """List all memory entries"""
            try:
                memory_list = []
                for key, value in self.memory.items():
                    memory_list.append({
                        "key": key,
                        "type": value.get("type", "general"),
                        "timestamp": value.get("timestamp"),
                        "size": len(str(value["value"]))
                    })
                
                return jsonify({
                    "memory_entries": memory_list,
                    "total_count": len(memory_list),
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Memory list error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/context/update', methods=['POST'])
        def update_context():
            """Update editor context"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400
                
                context_type = data.get("type", "general")
                context_data = data.get("data", {})
                
                context_key = f"context_{context_type}"
                self.memory[context_key] = {
                    "value": context_data,
                    "timestamp": datetime.now().isoformat(),
                    "type": "context"
                }
                
                return jsonify({
                    "context_type": context_type,
                    "updated": True,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Context update error: {e}")
                return jsonify({"error": str(e)}), 500
    
    def start(self):
        """Start the editor chat server"""
        logger.info(f"🎨 Starting Editor Chat Server on port {self.port}")
        logger.info(f"🤖 Integrated with: {self.unified_agent.name}")
        logger.info(f"🔧 Capabilities: {list(self.capabilities.keys())}")
        
        try:
            self.app.run(host='0.0.0.0', port=self.port, debug=False)
        except Exception as e:
            logger.error(f"Editor chat server error: {e}")

# Global instance
editor_chat_server = EditorChatServer()

if __name__ == "__main__":
    editor_chat_server.start()
