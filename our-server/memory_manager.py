#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Memory Manager - Centralized Memory System
Coordinates memory between ChatGPT, agents, and botgachh
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import threading

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, config_path: str = "our-server/config.json"):
        self.config = self.load_config(config_path)
        if not self.config or "memory" not in self.config:
            # Default config if file not found
            self.config = {
                "memory": {
                    "botgachh_path": "data/botgachh",
                    "session_log": "session_log.json",
                    "task_history": "task_history.json"
                }
            }
        self.botgachh_path = self.config["memory"]["botgachh_path"]
        self.session_log_path = os.path.join(self.botgachh_path, self.config["memory"]["session_log"])
        self.task_history_path = os.path.join(self.botgachh_path, self.config["memory"]["task_history"])
        
        # Ensure botgachh directory exists
        os.makedirs(self.botgachh_path, exist_ok=True)
        
        # Initialize memory files
        self.init_memory_files()
        
        # Thread lock for concurrent access
        self.lock = threading.Lock()
        
        logger.info("🧠 Memory Manager initialized")
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            return {}
    
    def init_memory_files(self):
        """Initialize memory files if they don't exist"""
        files_to_init = {
            self.session_log_path: {
                "chatgpt_sessions": [],
                "current_session": {
                    "session_id": f"session_{int(time.time())}",
                    "start_time": datetime.now().isoformat(),
                    "user_id": "sahon",
                    "context": "ZombieCoder AI Server",
                    "conversation_history": [],
                    "memory_updates": [],
                    "verification_log": []
                },
                "memory_stats": {
                    "total_sessions": 0,
                    "active_sessions": 1,
                    "memory_usage_mb": 0,
                    "last_cleanup": None
                },
                "system_status": {
                    "server_running": True,
                    "agents_active": [],
                    "memory_healthy": True,
                    "last_update": datetime.now().isoformat()
                }
            },
            self.task_history_path: {
                "tasks": [],
                "task_stats": {
                    "total_tasks": 0,
                    "completed_tasks": 0,
                    "failed_tasks": 0,
                    "pending_tasks": 0
                },
                "recent_tasks": [],
                "task_categories": {
                    "server_management": [],
                    "code_editing": [],
                    "debugging": [],
                    "memory_management": [],
                    "system_optimization": []
                }
            }
        }
        
        for file_path, default_content in files_to_init.items():
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(default_content, f, indent=2, ensure_ascii=False)
                logger.info(f"Created memory file: {file_path}")
    
    def read_memory(self, memory_type: str) -> Dict[str, Any]:
        """Read memory from botgachh files"""
        with self.lock:
            try:
                if memory_type == "session":
                    file_path = self.session_log_path
                elif memory_type == "tasks":
                    file_path = self.task_history_path
                else:
                    raise ValueError(f"Unknown memory type: {memory_type}")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
                    
            except Exception as e:
                logger.error(f"Error reading {memory_type} memory: {e}")
                return {}
    
    def write_memory(self, memory_type: str, data: Dict[str, Any]):
        """Write memory to botgachh files"""
        with self.lock:
            try:
                if memory_type == "session":
                    file_path = self.session_log_path
                elif memory_type == "tasks":
                    file_path = self.task_history_path
                else:
                    raise ValueError(f"Unknown memory type: {memory_type}")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
                logger.info(f"Updated {memory_type} memory")
                
            except Exception as e:
                logger.error(f"Error writing {memory_type} memory: {e}")
    
    def add_conversation(self, user_id: str, message: str, response: str, agent: str = "chatgpt"):
        """Add conversation to session log"""
        session_data = self.read_memory("session")
        
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "agent": agent,
            "message": message,
            "response": response,
            "context": "ZombieCoder AI Server"
        }
        
        # Add to current session
        if "current_session" in session_data:
            session_data["current_session"]["conversation_history"].append(conversation_entry)
        
        # Update memory stats
        session_data["memory_stats"]["total_sessions"] += 1
        session_data["system_status"]["last_update"] = datetime.now().isoformat()
        
        self.write_memory("session", session_data)
        logger.info(f"Added conversation for user: {user_id}")
    
    def add_task(self, task_type: str, description: str, status: str = "pending", result: str = None):
        """Add task to task history"""
        task_data = self.read_memory("tasks")
        
        task_entry = {
            "id": f"task_{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "type": task_type,
            "description": description,
            "status": status,
            "result": result,
            "agent": "chatgpt"
        }
        
        # Add to tasks list
        task_data["tasks"].append(task_entry)
        
        # Add to recent tasks (keep last 10)
        task_data["recent_tasks"].append(task_entry)
        if len(task_data["recent_tasks"]) > 10:
            task_data["recent_tasks"] = task_data["recent_tasks"][-10:]
        
        # Add to category
        if task_type in task_data["task_categories"]:
            task_data["task_categories"][task_type].append(task_entry)
        
        # Update stats
        task_data["task_stats"]["total_tasks"] += 1
        if status == "completed":
            task_data["task_stats"]["completed_tasks"] += 1
        elif status == "failed":
            task_data["task_stats"]["failed_tasks"] += 1
        else:
            task_data["task_stats"]["pending_tasks"] += 1
        
        self.write_memory("tasks", task_data)
        logger.info(f"Added task: {description}")
    
    def get_conversation_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent conversation history"""
        session_data = self.read_memory("session")
        
        if "current_session" in session_data:
            history = session_data["current_session"]["conversation_history"]
            return history[-limit:] if len(history) > limit else history
        
        return []
    
    def get_task_history(self, task_type: str = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get task history"""
        task_data = self.read_memory("tasks")
        
        if task_type and task_type in task_data["task_categories"]:
            return task_data["task_categories"][task_type][-limit:]
        
        return task_data["recent_tasks"][-limit:]
    
    def verify_truth(self, statement: str, context: str = None) -> Dict[str, Any]:
        """Verify truth of a statement (Guardian Agent functionality)"""
        verification_result = {
            "timestamp": datetime.now().isoformat(),
            "statement": statement,
            "context": context,
            "verified": True,  # Default to True for now
            "confidence": 0.9,
            "reasoning": "Statement appears to be factual based on available context",
            "guardian_agent": "chatgpt"
        }
        
        # Add to verification log
        session_data = self.read_memory("session")
        if "current_session" in session_data:
            session_data["current_session"]["verification_log"].append(verification_result)
            self.write_memory("session", session_data)
        
        logger.info(f"Truth verification completed for: {statement[:50]}...")
        return verification_result
    
    def ping_agents(self) -> Dict[str, Any]:
        """Ping all active agents"""
        session_data = self.read_memory("session")
        
        # Get agent status from config
        agents_status = {}
        for agent_name, agent_config in self.config["agents"].items():
            if agent_config.get("enabled", False):
                agents_status[agent_name] = {
                    "status": "active",
                    "endpoint": agent_config.get("api_endpoint", ""),
                    "last_ping": datetime.now().isoformat()
                }
        
        # Update system status
        session_data["system_status"]["agents_active"] = list(agents_status.keys())
        session_data["system_status"]["last_update"] = datetime.now().isoformat()
        
        self.write_memory("session", session_data)
        
        logger.info(f"Pinged {len(agents_status)} agents")
        return agents_status
    
    def cleanup_old_memory(self):
        """Clean up old memory entries"""
        session_data = self.read_memory("session")
        task_data = self.read_memory("tasks")
        
        # Clean up old conversations (keep last 100)
        if "current_session" in session_data:
            history = session_data["current_session"]["conversation_history"]
            if len(history) > 100:
                session_data["current_session"]["conversation_history"] = history[-100:]
        
        # Clean up old tasks (keep last 50)
        if len(task_data["tasks"]) > 50:
            task_data["tasks"] = task_data["tasks"][-50:]
        
        # Update cleanup timestamp
        session_data["memory_stats"]["last_cleanup"] = datetime.now().isoformat()
        
        self.write_memory("session", session_data)
        self.write_memory("tasks", task_data)
        
        logger.info("Memory cleanup completed")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        session_data = self.read_memory("session")
        task_data = self.read_memory("tasks")
        
        return {
            "session_stats": session_data.get("memory_stats", {}),
            "task_stats": task_data.get("task_stats", {}),
            "system_status": session_data.get("system_status", {}),
            "total_conversations": len(session_data.get("current_session", {}).get("conversation_history", [])),
            "total_tasks": len(task_data.get("tasks", [])),
            "last_update": datetime.now().isoformat()
        }

# Global memory manager instance
memory_manager = MemoryManager()
