#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ZombieCoder Multi-Project API
API endpoints for project management and agent switching
"""

import os
import json
import time
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any, Optional
from multi_project_manager import multi_project_manager

logger = logging.getLogger(__name__)

class MultiProjectAPI:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.port = 8081
        
        # Setup routes
        self.setup_routes()
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/api/projects', methods=['GET'])
        def list_projects():
            """List all projects"""
            try:
                projects = multi_project_manager.list_projects()
                active_project = multi_project_manager.get_active_project()
                
                return jsonify({
                    "projects": projects,
                    "active_project": active_project,
                    "total_projects": len(projects),
                    "timestamp": time.time()
                })
            except Exception as e:
                logger.error(f"List projects error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/projects', methods=['POST'])
        def assign_project():
            """Assign a new project"""
            try:
                data = request.get_json()
                project_path = data.get("project_path")
                project_name = data.get("project_name")
                
                if not project_path:
                    return jsonify({"error": "Project path required"}), 400
                
                project_info = multi_project_manager.assign_project(project_path, project_name)
                
                if project_info:
                    return jsonify({
                        "success": True,
                        "project": project_info,
                        "message": f"Project assigned: {project_info['name']}"
                    })
                else:
                    return jsonify({"error": "Failed to assign project"}), 500
                    
            except Exception as e:
                logger.error(f"Assign project error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/projects/<path:project_path>', methods=['PUT'])
        def switch_project(project_path):
            """Switch to a project"""
            try:
                success = multi_project_manager.switch_to_project(project_path)
                
                if success:
                    active_project = multi_project_manager.get_active_project()
                    return jsonify({
                        "success": True,
                        "active_project": active_project,
                        "message": f"Switched to: {active_project['name']}"
                    })
                else:
                    return jsonify({"error": "Failed to switch project"}), 400
                    
            except Exception as e:
                logger.error(f"Switch project error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/projects/<path:project_path>', methods=['DELETE'])
        def remove_project(project_path):
            """Remove a project"""
            try:
                success = multi_project_manager.remove_project(project_path)
                
                if success:
                    return jsonify({
                        "success": True,
                        "message": "Project removed successfully"
                    })
                else:
                    return jsonify({"error": "Project not found"}), 404
                    
            except Exception as e:
                logger.error(f"Remove project error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/projects/active', methods=['GET'])
        def get_active_project():
            """Get active project"""
            try:
                active_project = multi_project_manager.get_active_project()
                
                if active_project:
                    return jsonify({
                        "active_project": active_project,
                        "timestamp": time.time()
                    })
                else:
                    return jsonify({
                        "active_project": None,
                        "message": "No active project"
                    })
                    
            except Exception as e:
                logger.error(f"Get active project error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/projects/shortcut/<shortcut>', methods=['POST'])
        def shortcut_switch(shortcut):
            """Switch project by shortcut"""
            try:
                success = multi_project_manager.handle_shortcut_command(shortcut)
                
                if success:
                    active_project = multi_project_manager.get_active_project()
                    return jsonify({
                        "success": True,
                        "active_project": active_project,
                        "shortcut": shortcut,
                        "message": f"Switched to: {active_project['name']}"
                    })
                else:
                    return jsonify({"error": f"Shortcut not found: {shortcut}"}), 404
                    
            except Exception as e:
                logger.error(f"Shortcut switch error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/projects/suggestions', methods=['GET'])
        def get_suggestions():
            """Get project suggestions"""
            try:
                query = request.args.get('q', '')
                
                if not query:
                    return jsonify({"suggestions": []})
                
                suggestions = multi_project_manager.get_project_suggestions(query)
                
                return jsonify({
                    "suggestions": suggestions,
                    "query": query,
                    "count": len(suggestions)
                })
                
            except Exception as e:
                logger.error(f"Suggestions error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/projects/stats', methods=['GET'])
        def get_stats():
            """Get project statistics"""
            try:
                stats = multi_project_manager.get_project_stats()
                
                return jsonify({
                    "stats": stats,
                    "timestamp": time.time()
                })
                
            except Exception as e:
                logger.error(f"Stats error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/projects/detect', methods=['POST'])
        def detect_project():
            """Detect project type"""
            try:
                data = request.get_json()
                project_path = data.get("project_path")
                
                if not project_path:
                    return jsonify({"error": "Project path required"}), 400
                
                project_type = multi_project_manager.detect_project_type(project_path)
                config = multi_project_manager.get_project_config(project_type)
                
                return jsonify({
                    "project_path": project_path,
                    "detected_type": project_type,
                    "config": config,
                    "suggested_agent": config["agent"],
                    "capabilities": config["capabilities"]
                })
                
            except Exception as e:
                logger.error(f"Detect project error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/projects/status', methods=['GET'])
        def project_status():
            """Get overall project status"""
            try:
                active_project = multi_project_manager.get_active_project()
                stats = multi_project_manager.get_project_stats()
                
                return jsonify({
                    "status": "active",
                    "active_project": active_project,
                    "stats": stats,
                    "timestamp": time.time()
                })
                
            except Exception as e:
                logger.error(f"Status error: {e}")
                return jsonify({"error": str(e)}), 500
    
    def start(self):
        """Start multi-project API server"""
        logger.info(f"🚀 Starting Multi-Project API Server on port {self.port}")
        
        try:
            self.app.run(host='0.0.0.0', port=self.port, debug=False)
        except Exception as e:
            logger.error(f"Multi-project API server error: {e}")

# Global instance
multi_project_api = MultiProjectAPI()

if __name__ == "__main__":
    multi_project_api.start()
