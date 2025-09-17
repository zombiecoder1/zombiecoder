#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ZombieCoder Multi-Project Manager
Dynamic agent assignment and project-specific configurations
"""

import os
import json
import time
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from unified_agent_system import unified_agent

# Flask app setup
app = Flask(__name__)
CORS(app)

logger = logging.getLogger(__name__)

class MultiProjectManager:
    def __init__(self):
        self.projects = {}
        self.active_project = None
        self.agent_mappings = {}
        self.shortcut_keys = {}
        self.project_configs = {}
        
        # Default project configurations
        self.default_config = {
            "agent": "ZombieCoder Agent (সাহন ভাই)",
            "capabilities": ["coding", "debugging", "architecture", "database", "api", "security", "performance", "devops", "voice", "real_time"],
            "personalities": ["elder_brother", "friend", "teacher", "doctor", "engineer", "guard", "coach", "professional"],
            "auto_detect": True,
            "context_aware": True,
            "truth_verification": True,
            "real_time_support": True,
            "cloud_fallback": False
        }
        
        # Project type mappings
        self.project_types = {
            "web": {
                "capabilities": ["coding", "api", "security", "performance"],
                "agent_focus": "web_development"
            },
            "mobile": {
                "capabilities": ["coding", "api", "security", "performance"],
                "agent_focus": "mobile_development"
            },
            "backend": {
                "capabilities": ["coding", "database", "api", "security", "performance", "devops"],
                "agent_focus": "backend_development"
            },
            "frontend": {
                "capabilities": ["coding", "api", "performance"],
                "agent_focus": "frontend_development"
            },
            "ai_ml": {
                "capabilities": ["coding", "architecture", "performance", "devops"],
                "agent_focus": "ai_ml_development"
            },
            "devops": {
                "capabilities": ["devops", "security", "performance", "architecture"],
                "agent_focus": "devops_engineering"
            },
            "database": {
                "capabilities": ["database", "architecture", "security", "performance"],
                "agent_focus": "database_engineering"
            }
        }
        
        # Load existing projects
        self.load_projects()
    
    def detect_project_type(self, project_path: str) -> str:
        """Detect project type based on files and structure"""
        try:
            path = Path(project_path)
            
            # Check for common project files
            if (path / "package.json").exists():
                return "web"
            elif (path / "pom.xml").exists() or (path / "build.gradle").exists():
                return "backend"
            elif (path / "requirements.txt").exists() or (path / "setup.py").exists():
                return "ai_ml"
            elif (path / "Dockerfile").exists() or (path / "docker-compose.yml").exists():
                return "devops"
            elif (path / "index.html").exists() or (path / "app.js").exists():
                return "frontend"
            elif (path / "app.py").exists() or (path / "main.py").exists():
                return "backend"
            elif (path / "AndroidManifest.xml").exists() or (path / "Info.plist").exists():
                return "mobile"
            elif (path / "schema.sql").exists() or (path / "migrations").exists():
                return "database"
            else:
                return "general"
        except Exception as e:
            logger.error(f"Project type detection error: {e}")
            return "general"
    
    def assign_project(self, project_path: str, project_name: str = None) -> Dict[str, Any]:
        """Assign a project with dynamic agent configuration"""
        try:
            if not project_name:
                project_name = Path(project_path).name
            
            # Detect project type
            project_type = self.detect_project_type(project_path)
            
            # Get project-specific configuration
            config = self.get_project_config(project_type)
            
            # Create project entry
            project_info = {
                "name": project_name,
                "path": project_path,
                "type": project_type,
                "config": config,
                "assigned_at": time.time(),
                "last_accessed": time.time(),
                "agent": config["agent"],
                "capabilities": config["capabilities"],
                "shortcut_key": self.generate_shortcut_key(project_name)
            }
            
            # Store project
            self.projects[project_path] = project_info
            self.agent_mappings[project_path] = config["agent"]
            
            # Save to file
            self.save_projects()
            
            logger.info(f"✅ Project assigned: {project_name} ({project_type})")
            return project_info
            
        except Exception as e:
            logger.error(f"Project assignment error: {e}")
            return {}
    
    def get_project_config(self, project_type: str) -> Dict[str, Any]:
        """Get configuration for project type"""
        config = self.default_config.copy()
        
        if project_type in self.project_types:
            type_config = self.project_types[project_type]
            config["capabilities"] = type_config["capabilities"]
            config["agent_focus"] = type_config["agent_focus"]
        
        return config
    
    def generate_shortcut_key(self, project_name: str) -> str:
        """Generate shortcut key for project"""
        # Simple mapping: first letter + number
        base_key = project_name[0].upper()
        counter = 1
        
        while base_key in self.shortcut_keys.values():
            base_key = f"{project_name[0].upper()}{counter}"
            counter += 1
        
        return base_key
    
    def switch_to_project(self, project_path: str) -> bool:
        """Switch to a specific project"""
        try:
            if project_path not in self.projects:
                logger.error(f"Project not found: {project_path}")
                return False
            
            self.active_project = project_path
            project_info = self.projects[project_path]
            project_info["last_accessed"] = time.time()
            
            # Update agent configuration
            self.update_agent_for_project(project_info)
            
            logger.info(f"✅ Switched to project: {project_info['name']}")
            return True
            
        except Exception as e:
            logger.error(f"Project switch error: {e}")
            return False
    
    def update_agent_for_project(self, project_info: Dict[str, Any]):
        """Update agent configuration for project"""
        try:
            # Update unified agent with project-specific settings
            unified_agent.capabilities = project_info["config"]["capabilities"]
            unified_agent.project_context = {
                "name": project_info["name"],
                "type": project_info["type"],
                "path": project_info["path"],
                "focus": project_info["config"].get("agent_focus", "general")
            }
            
            logger.info(f"✅ Agent updated for project: {project_info['name']}")
            
        except Exception as e:
            logger.error(f"Agent update error: {e}")
    
    def get_active_project(self) -> Optional[Dict[str, Any]]:
        """Get currently active project"""
        if self.active_project and self.active_project in self.projects:
            return self.projects[self.active_project]
        return None
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all assigned projects"""
        return list(self.projects.values())
    
    def remove_project(self, project_path: str) -> bool:
        """Remove project assignment"""
        try:
            if project_path in self.projects:
                project_name = self.projects[project_path]["name"]
                del self.projects[project_path]
                
                if project_path in self.agent_mappings:
                    del self.agent_mappings[project_path]
                
                # If this was the active project, clear it
                if self.active_project == project_path:
                    self.active_project = None
                
                self.save_projects()
                logger.info(f"✅ Project removed: {project_name}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Project removal error: {e}")
            return False
    
    def get_project_by_shortcut(self, shortcut: str) -> Optional[Dict[str, Any]]:
        """Get project by shortcut key"""
        for project_info in self.projects.values():
            if project_info.get("shortcut_key") == shortcut:
                return project_info
        return None
    
    def handle_shortcut_command(self, shortcut: str) -> bool:
        """Handle shortcut key command"""
        try:
            project_info = self.get_project_by_shortcut(shortcut)
            if project_info:
                return self.switch_to_project(project_info["path"])
            else:
                logger.warning(f"Shortcut not found: {shortcut}")
                return False
                
        except Exception as e:
            logger.error(f"Shortcut command error: {e}")
            return False
    
    def get_project_stats(self) -> Dict[str, Any]:
        """Get project statistics"""
        try:
            total_projects = len(self.projects)
            active_project = self.get_active_project()
            
            project_types = {}
            for project_info in self.projects.values():
                project_type = project_info["type"]
                project_types[project_type] = project_types.get(project_type, 0) + 1
            
            return {
                "total_projects": total_projects,
                "active_project": active_project["name"] if active_project else None,
                "project_types": project_types,
                "shortcuts_available": len(self.shortcut_keys),
                "last_updated": time.time()
            }
            
        except Exception as e:
            logger.error(f"Stats error: {e}")
            return {}
    
    def load_projects(self):
        """Load projects from file"""
        try:
            config_file = Path("data/multi_project_config.json")
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.projects = data.get("projects", {})
                    self.agent_mappings = data.get("agent_mappings", {})
                    self.shortcut_keys = data.get("shortcut_keys", {})
                    self.active_project = data.get("active_project")
                
                logger.info(f"✅ Loaded {len(self.projects)} projects")
            else:
                logger.info("No existing project configuration found")
                
        except Exception as e:
            logger.error(f"Project loading error: {e}")
    
    def save_projects(self):
        """Save projects to file"""
        try:
            config_file = Path("data/multi_project_config.json")
            config_file.parent.mkdir(exist_ok=True)
            
            data = {
                "projects": self.projects,
                "agent_mappings": self.agent_mappings,
                "shortcut_keys": self.shortcut_keys,
                "active_project": self.active_project,
                "last_saved": time.time()
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info("✅ Projects configuration saved")
            
        except Exception as e:
            logger.error(f"Project saving error: {e}")
    
    def get_project_suggestions(self, query: str) -> List[Dict[str, Any]]:
        """Get project suggestions based on query"""
        try:
            suggestions = []
            query_lower = query.lower()
            
            for project_info in self.projects.values():
                project_name = project_info["name"].lower()
                project_type = project_info["type"].lower()
                
                if (query_lower in project_name or 
                    query_lower in project_type or
                    any(cap.lower() in query_lower for cap in project_info["capabilities"])):
                    
                    suggestions.append({
                        "name": project_info["name"],
                        "type": project_info["type"],
                        "path": project_info["path"],
                        "shortcut": project_info["shortcut_key"],
                        "capabilities": project_info["capabilities"],
                        "score": self.calculate_suggestion_score(project_info, query_lower)
                    })
            
            # Sort by score
            suggestions.sort(key=lambda x: x["score"], reverse=True)
            return suggestions[:5]  # Top 5 suggestions
            
        except Exception as e:
            logger.error(f"Suggestion error: {e}")
            return []
    
    def calculate_suggestion_score(self, project_info: Dict[str, Any], query: str) -> float:
        """Calculate suggestion relevance score"""
        score = 0.0
        
        # Name match
        if query in project_info["name"].lower():
            score += 10.0
        
        # Type match
        if query in project_info["type"].lower():
            score += 5.0
        
        # Capability match
        for capability in project_info["capabilities"]:
            if query in capability.lower():
                score += 3.0
        
        # Recent access bonus
        last_accessed = project_info.get("last_accessed", 0)
        if last_accessed > time.time() - 86400:  # Last 24 hours
            score += 2.0
        
        return score

# Global instance
multi_project_manager = MultiProjectManager()

# Flask routes
@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "service": "ZombieCoder Multi-Project Manager",
        "status": "running",
        "port": 8001,
        "projects_count": len(multi_project_manager.projects),
        "active_project": multi_project_manager.active_project
    })

@app.route('/status')
def status():
    """Status endpoint"""
    return jsonify({
        "status": "running",
        "timestamp": time.time(),
        "projects": len(multi_project_manager.projects),
        "active_project": multi_project_manager.active_project,
        "agent_mappings": len(multi_project_manager.agent_mappings)
    })

@app.route('/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    return jsonify({
        "projects": multi_project_manager.projects,
        "count": len(multi_project_manager.projects)
    })

@app.route('/projects', methods=['POST'])
def add_project():
    """Add a new project"""
    try:
        data = request.get_json()
        project_path = data.get('path')
        project_name = data.get('name', os.path.basename(project_path))
        
        if not project_path:
            return jsonify({"error": "Project path is required"}), 400
        
        # Add project using existing method
        multi_project_manager.assign_project(project_path, project_name)
        
        return jsonify({
            "message": "Project added successfully",
            "project": project_name,
            "path": project_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/projects/<project_name>', methods=['GET'])
def get_project(project_name):
    """Get specific project"""
    if project_name in multi_project_manager.projects:
        return jsonify(multi_project_manager.projects[project_name])
    else:
        return jsonify({"error": "Project not found"}), 404

@app.route('/projects/<project_name>/activate', methods=['POST'])
def activate_project(project_name):
    """Activate a project"""
    try:
        # Find the project by name to get its path
        project_path = None
        for p_info in multi_project_manager.projects.values():
            if p_info["name"] == project_name:
                project_path = p_info["path"]
                break

        if not project_path:
            return jsonify({"error": "Project not found"}), 404

        multi_project_manager.switch_to_project(project_path)
        return jsonify({
            "message": f"Project '{project_name}' activated",
            "active_project": project_name
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get project suggestions"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({"suggestions": []})
    
    suggestions = multi_project_manager.get_project_suggestions(query)
    return jsonify({"suggestions": suggestions})

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for multi-project manager"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', {})
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        # Use unified agent for chat functionality
        result = unified_agent.process_message(message, context)
        response = result.get("response", "Sorry, I couldn't process your request.")
        
        return jsonify({
            "response": response,
            "service": "multi_project_manager",
            "timestamp": time.time()
        })
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "service": "multi_project_manager"
    })

if __name__ == '__main__':
    print("🤖 Starting ZombieCoder Multi-Project Manager...")
    print("🌐 Server starting on http://localhost:8001")
    print("📡 Available endpoints:")
    print("   - GET  / (home)")
    print("   - GET  /status (status)")
    print("   - GET  /projects (list projects)")
    print("   - POST /projects (add project)")
    print("   - GET  /projects/<name> (get project)")
    print("   - POST /projects/<name>/activate (activate project)")
    print("   - GET  /suggestions?q=<query> (get suggestions)")
    print("   - GET  /health (health check)")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=8001, debug=True)
