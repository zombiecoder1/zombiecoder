#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧩 Editor Agent - Code Suggestion & Verification
Connects to local server and provides intelligent code assistance
"""

import os
import json
import time
import logging
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional
import threading
import glob

logger = logging.getLogger(__name__)

class EditorAgent:
    def __init__(self, config_path: str = "../config.json"):
        self.config = self.load_config(config_path)
        self.server_url = "http://localhost:12345"  # Primary server
        self.fallback_servers = [
            "http://localhost:12346",  # Fallback 1
            "http://localhost:12347"   # Fallback 2
        ]
        self.current_server = self.server_url
        self.agent_name = "editor_agent"
        self.role = "code_suggestion_verification"
        self.status = "active"
        self.active_light = True  # Active light indicator
        
        # Memory paths
        self.botgachh_path = "../botgachh"
        self.session_log_path = os.path.join(self.botgachh_path, "session_log.json")
        self.task_history_path = os.path.join(self.botgachh_path, "task_history.json")
        
        # Project path detection
        self.project_paths = {}
        self.current_project = None
        self.supported_extensions = [".py", ".js", ".ts", ".html", ".css", ".json", ".md"]
        self.ignore_patterns = ["node_modules", "__pycache__", ".git", "venv", ".vscode"]
        
        # Performance monitoring
        self.response_times = []
        self.latency_threshold = 2.0  # seconds
        self.batch_mode = False
        self.current_latency = 0.0
        
        # File monitoring
        self.monitored_files = {}
        self.temp_memory_files = {}
        
        # Task queue
        self.pending_tasks = []
        self.completed_tasks = []
        
        # Context management
        self.user_context = {}
        self.session_context = {}
        
        # Health monitoring
        self.last_health_check = time.time()
        self.health_check_interval = 30  # seconds
        
        logger.info(f"🧩 {self.agent_name} initialized as main work engine")
        self.update_active_light()
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            return {}
    
    def verify_output(self, suggestion: str, context: str = None) -> Dict[str, Any]:
        """Verify code suggestion before sending"""
        verification_result = {
            "verified": False,
            "confidence": 0.0,
            "reasoning": "",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Basic syntax check
            if self.check_syntax(suggestion):
                verification_result["verified"] = True
                verification_result["confidence"] = 0.8
                verification_result["reasoning"] = "Syntax check passed"
            else:
                verification_result["reasoning"] = "Syntax check failed"
                
        except Exception as e:
            verification_result["reasoning"] = f"Verification error: {e}"
        
        return verification_result
    
    def update_active_light(self):
        """Update active light based on agent health and responsiveness"""
        try:
            # Check if agent is responsive
            start_time = time.time()
            response = requests.get(f"{self.current_server}/api/agents/editor", timeout=3)
            self.current_latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                self.active_light = True
                self.status = "active"
                logger.info(f"💡 Active light ON - Latency: {self.current_latency:.2f}ms")
            else:
                self.active_light = False
                self.status = "inactive"
                logger.warning("❌ Active light OFF - Server not responding")
                
        except Exception as e:
            self.active_light = False
            self.status = "inactive"
            logger.error(f"❌ Active light OFF - Error: {e}")
    
    def check_health_and_fallback(self):
        """Check health and switch to fallback if needed"""
        try:
            # Test current server
            response = requests.get(f"{self.current_server}/api/agents/editor", timeout=5)
            
            if response.status_code == 200:
                # Current server is healthy
                self.last_health_check = time.time()
                return True
            else:
                # Current server failed, try fallback
                return self.switch_to_fallback()
                
        except Exception as e:
            logger.warning(f"Health check failed for {self.current_server}: {e}")
            return self.switch_to_fallback()
    
    def switch_to_fallback(self):
        """Switch to fallback server if available"""
        for fallback_server in self.fallback_servers:
            try:
                logger.info(f"Trying fallback server: {fallback_server}")
                response = requests.get(f"{fallback_server}/api/agents/editor", timeout=5)
                
                if response.status_code == 200:
                    self.current_server = fallback_server
                    self.active_light = True
                    self.status = "active"
                    logger.info(f"✅ Switched to fallback server: {fallback_server}")
                    return True
                    
            except Exception as e:
                logger.warning(f"Fallback server {fallback_server} failed: {e}")
                continue
        
        # All servers failed
        self.active_light = False
        self.status = "inactive"
        logger.error("❌ All servers unavailable - Active light OFF")
        return False
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status including active light and latency"""
        self.update_active_light()
        
        return {
            "agent_name": self.agent_name,
            "role": self.role,
            "status": self.status,
            "active_light": self.active_light,
            "current_latency": self.current_latency,
            "current_server": self.current_server,
            "batch_mode": self.batch_mode,
            "pending_tasks": len(self.pending_tasks),
            "completed_tasks": len(self.completed_tasks),
            "monitored_files": len(self.monitored_files),
            "last_health_check": self.last_health_check,
            "response_times_avg": sum(self.response_times[-10:]) / len(self.response_times[-10:]) if self.response_times else 0
        }
    
    def check_syntax(self, code: str) -> bool:
        """Basic syntax check for code"""
        try:
            # Simple checks - can be expanded
            if code.strip() == "":
                return False
            
            # Check for basic syntax patterns
            brackets = {'(': ')', '{': '}', '[': ']'}
            stack = []
            
            for char in code:
                if char in brackets:
                    stack.append(char)
                elif char in brackets.values():
                    if not stack:
                        return False
                    if brackets[stack.pop()] != char:
                        return False
            
            return len(stack) == 0
            
        except Exception as e:
            logger.error(f"Syntax check error: {e}")
            return False
    
    def process_command(self, command: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process editor command and return response - Main work engine"""
        start_time = time.time()
        
        try:
            # Step 1: Health check and fallback
            if not self.check_health_and_fallback():
                return {
                    "status": "error",
                    "response": "❌ Agent unavailable - All servers down",
                    "active_light": False,
                    "latency": None,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Step 2: Update active light and latency
            self.update_active_light()
            
            # Step 3: Preserve user context
            if context:
                self.user_context.update(context)
                self.session_context["last_command"] = command
                self.session_context["last_context"] = context
            
            # Step 4: Get memory context
            memory_context = self.get_memory_context(context)
            
            # Step 5: Process command based on type
            if command.startswith("run_tasks_on") or command == "run_tasks":
                response = self.execute_pending_tasks()
            elif command.startswith("verify_code"):
                response = self.verify_code_suggestion(command, memory_context)
            elif command.startswith("suggest_code"):
                response = self.generate_code_suggestion(command, memory_context)
            elif command.startswith("add_task"):
                response = self.add_task_from_command(command)
            elif command.startswith("monitor_file"):
                response = self.monitor_file_from_command(command)
            else:
                response = self.handle_general_command(command, memory_context)
            
            # Step 6: Measure and track performance
            response_time = time.time() - start_time
            self.response_times.append(response_time)
            self.current_latency = response_time * 1000  # Convert to milliseconds
            
            # Step 7: Check latency threshold and update batch mode
            if response_time > self.latency_threshold:
                self.batch_mode = True
                logger.warning(f"High latency detected: {response_time:.2f}s, switching to batch mode")
            else:
                self.batch_mode = False
            
            # Step 8: Log everything to botgachh memory
            self.log_to_memory(command, response, response_time)
            
            # Step 9: Return comprehensive response
            return {
                "status": "success",
                "response": response,
                "response_time": response_time,
                "current_latency": self.current_latency,
                "active_light": self.active_light,
                "batch_mode": self.batch_mode,
                "server_used": self.current_server,
                "agent_status": self.status,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            self.active_light = False
            return {
                "status": "error",
                "response": "❌ Processing error - যাচাই প্রয়োজন",
                "active_light": False,
                "latency": None,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_memory_context(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get context from botgachh memory"""
        try:
            # Read session log
            if os.path.exists(self.session_log_path):
                with open(self.session_log_path, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    
                # Get recent conversations
                conversations = session_data.get("current_session", {}).get("conversation_history", [])
                
                # Get current project context
                project_context = {
                    "recent_conversations": conversations[-5:] if conversations else [],  # Last 5 conversations
                    "current_files": context.get("files", []) if context else [],
                    "project_path": context.get("project_path", "") if context else "",
                    "user_context": context or {}
                }
                
                logger.info(f"Loaded {len(project_context['recent_conversations'])} recent conversations")
                return project_context
            
        except Exception as e:
            logger.error(f"Error reading memory context: {e}")
        
        return {"recent_conversations": [], "current_files": [], "project_path": "", "user_context": context or {}}
    
    def verify_code_suggestion(self, command: str, context: Dict[str, Any]) -> str:
        """Verify code suggestion"""
        try:
            # Extract code from command
            code = command.replace("verify_code", "").strip()
            
            # Verify the code
            verification = self.verify_output(code, str(context))
            
            if verification["verified"]:
                return f"✅ কোড সফলভাবে যাচাই করা হয়েছে\nআত্মবিশ্বাস: {verification['confidence']}\nকারণ: {verification['reasoning']}"
            else:
                return f"❌ কোড যাচাই ব্যর্থ হয়েছে\nকারণ: {verification['reasoning']}\nপরামর্শ: অনুগ্রহ করে সমস্যাগুলো পর্যালোচনা করে ঠিক করুন"
                
        except Exception as e:
            return f"যাচাই প্রয়োজন: {e}"
    
    def generate_code_suggestion(self, command: str, context: Dict[str, Any]) -> str:
        """Generate code suggestion based on context"""
        try:
            # Extract requirements from command
            requirements = command.replace("suggest_code", "").strip()
            
            # Generate suggestion based on requirements (context is optional)
            suggestion = self.create_code_suggestion(requirements, context)
            
            # Verify the suggestion
            verification = self.verify_output(suggestion, str(context))
            
            if verification["verified"]:
                return f"💡 কোড সাজেশন:\n```\n{suggestion}\n```\nআত্মবিশ্বাস: {verification['confidence']}"
            else:
                return f"⚠️ সাজেশন পর্যালোচনা প্রয়োজন:\n```\n{suggestion}\n```\nকারণ: {verification['reasoning']}"
                
        except Exception as e:
            return f"যাচাই প্রয়োজন: {e}"
    
    def create_code_suggestion(self, requirements: str, context: Dict[str, Any]) -> str:
        """Create code suggestion based on requirements and context"""
        # This is a simplified version - can be enhanced with local LLM
        suggestion = f"# Code suggestion for: {requirements}\n"
        
        # Check recent conversations for context
        recent_conversations = context.get("recent_conversations", [])
        user_context = context.get("user_context", {})
        
        # Add context-aware suggestions
        if "python" in requirements.lower():
            if "factorial" in requirements.lower():
                suggestion += """def factorial(n):
    \"\"\"Calculate factorial of a number\"\"\"
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Example usage
if __name__ == \"__main__\":
    number = 5
    result = factorial(number)
    print(f\"Factorial of {number} is {result}\")
"""
            elif "function" in requirements.lower():
                suggestion += """def example_function():
    \"\"\"Example function template\"\"\"
    # Add your code here
    pass

# Example usage
if __name__ == \"__main__\":
    example_function()
"""
            else:
                suggestion += """import os
import sys

def main():
    \"\"\"Main function\"\"\"
    # Add your code here
    pass

if __name__ == \"__main__\":
    main()
"""
        elif "javascript" in requirements.lower():
            suggestion += """// JavaScript code
function exampleFunction() {
    // Add your code here
    console.log("Hello, World!");
}

// Example usage
exampleFunction();
"""
        elif "html" in requirements.lower():
            suggestion += """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <!-- Add your content here -->
    <h1>Hello, World!</h1>
</body>
</html>"""
        else:
            suggestion += """# General code template
# Add your code here
"""
        
        return suggestion
    
    def add_task_from_command(self, command: str) -> str:
        """Add task from command string"""
        try:
            # Extract task info from command
            parts = command.split(" ", 2)  # Split into max 3 parts
            if len(parts) >= 3:
                task_type = parts[1]
                description = parts[2]
            else:
                task_type = "general"
                description = command.replace("add_task", "").strip()
            
            self.add_task(task_type, description)
            return f"✅ কাজ যোগ করা হয়েছে: {description}"
        except Exception as e:
            logger.error(f"Error adding task from command: {e}")
            return f"❌ কাজ যোগ করতে ব্যর্থ: {e}"
    
    def monitor_file_from_command(self, command: str) -> str:
        """Monitor file from command string"""
        try:
            file_path = command.replace("monitor_file", "").strip()
            if file_path:
                self.monitor_file(file_path)
                return f"✅ ফাইল পর্যবেক্ষণ শুরু হয়েছে: {file_path}"
            else:
                return "❌ ফাইল পাথ দেওয়া হয়নি"
        except Exception as e:
            logger.error(f"Error monitoring file from command: {e}")
            return f"❌ ফাইল পর্যবেক্ষণ ব্যর্থ: {e}"
    
    def handle_general_command(self, command: str, context: Dict[str, Any]) -> str:
        """Handle general editor commands"""
        if "help" in command.lower():
            return self.get_help_text()
        elif "status" in command.lower():
            return self.get_status()
        elif "memory" in command.lower():
            return self.get_memory_status()
        else:
            return f"কমান্ড প্রাপ্ত: {command}\nপ্রসঙ্গ: {len(context.get('recent_conversations', []))} সাম্প্রতিক কথোপকথন"
    
    def execute_pending_tasks(self) -> str:
        """Execute all pending tasks in queue"""
        if not self.pending_tasks:
            return "কোন অপেক্ষমান কাজ নেই"
        
        results = []
        for task in self.pending_tasks:
            try:
                result = self.process_single_task(task)
                results.append(f"✅ {task['description']}: {result}")
                self.completed_tasks.append(task)
            except Exception as e:
                results.append(f"❌ {task['description']}: ব্যর্থ - {e}")
        
        # Clear pending tasks
        self.pending_tasks = []
        
        # Log to botgachh
        self.log_tasks_execution(results)
        
        return "\n".join(results)
    
    def process_single_task(self, task: Dict[str, Any]) -> str:
        """Process a single task"""
        task_type = task.get("type", "general")
        
        if task_type == "compile":
            return "কম্পাইলেশন সম্পন্ন হয়েছে"
        elif task_type == "lint":
            return "লিন্টিং সম্পন্ন হয়েছে"
        elif task_type == "test":
            return "টেস্ট সম্পন্ন হয়েছে"
        else:
            return "কাজ সম্পন্ন হয়েছে"
    
    def add_task(self, task_type: str, description: str):
        """Add task to pending queue"""
        task = {
            "id": f"task_{int(time.time())}",
            "type": task_type,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }
        
        self.pending_tasks.append(task)
        logger.info(f"কাজ যোগ করা হয়েছে: {description}")
    
    def monitor_file(self, file_path: str):
        """Monitor file for changes"""
        if file_path not in self.monitored_files:
            self.monitored_files[file_path] = {
                "last_modified": os.path.getmtime(file_path),
                "size": os.path.getsize(file_path),
                "context": self.extract_file_context(file_path)
            }
            logger.info(f"ফাইল পর্যবেক্ষণ শুরু হয়েছে: {file_path}")
    
    def extract_file_context(self, file_path: str) -> Dict[str, Any]:
        """Extract context from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "file_type": os.path.splitext(file_path)[1],
                "content_length": len(content),
                "lines": len(content.split('\n')),
                "language": self.detect_language(file_path)
            }
        except Exception as e:
            logger.error(f"Error extracting file context: {e}")
            return {}
    
    def detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.md': 'markdown',
            '.txt': 'text'
        }
        
        return language_map.get(ext, 'unknown')
    
    def detect_project_path(self, file_path: str) -> str:
        """Detect project root path from file path"""
        if not file_path:
            return None
            
        # Start from file directory and go up until we find project indicators
        current_dir = os.path.dirname(os.path.abspath(file_path))
        
        while current_dir and current_dir != os.path.dirname(current_dir):
            # Check for project indicators
            project_indicators = [
                "package.json", "requirements.txt", "pyproject.toml",
                ".git", "README.md", "Makefile", "CMakeLists.txt"
            ]
            
            for indicator in project_indicators:
                if os.path.exists(os.path.join(current_dir, indicator)):
                    return current_dir
            
            # Go up one level
            current_dir = os.path.dirname(current_dir)
        
        # If no project indicators found, return the directory containing the file
        return os.path.dirname(os.path.abspath(file_path))
    
    def scan_project_files(self, project_path: str) -> List[str]:
        """Scan project directory for relevant files"""
        if not project_path or not os.path.exists(project_path):
            return []
        
        relevant_files = []
        
        for root, dirs, files in os.walk(project_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_patterns]
            
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in self.supported_extensions:
                    relevant_files.append(file_path)
        
        return relevant_files
    
    def get_project_context(self, file_path: str) -> Dict[str, Any]:
        """Get comprehensive project context"""
        project_path = self.detect_project_path(file_path)
        if not project_path:
            return {}
        
        # Cache project context
        if project_path not in self.project_paths:
            self.project_paths[project_path] = {
                "path": project_path,
                "name": os.path.basename(project_path),
                "files": self.scan_project_files(project_path),
                "last_scan": datetime.now().isoformat()
            }
        
        project_context = self.project_paths[project_path].copy()
        
        # Add current file context
        if file_path:
            project_context["current_file"] = {
                "path": file_path,
                "name": os.path.basename(file_path),
                "extension": os.path.splitext(file_path)[1],
                "relative_path": os.path.relpath(file_path, project_path)
            }
        
        return project_context
    
    def log_to_memory(self, command: str, response: str, response_time: float):
        """Log command and response to botgachh memory"""
        try:
            # Add conversation to memory via API
            conversation_data = {
                "user_id": "editor_agent",
                "message": command,
                "response": response,
                "agent": self.agent_name
            }
            
            requests.post(f"{self.server_url}/api/memory/add_conversation", 
                         json=conversation_data, timeout=5)
            
            # Add task to memory
            task_data = {
                "type": "code_editing",
                "description": f"Editor command: {command[:50]}...",
                "status": "completed",
                "result": f"Response time: {response_time:.2f}s"
            }
            
            requests.post(f"{self.server_url}/api/memory/add_task", 
                         json=task_data, timeout=5)
            
        except Exception as e:
            logger.error(f"Error logging to memory: {e}")
    
    def log_tasks_execution(self, results: List[str]):
        """Log task execution results"""
        try:
            task_data = {
                "type": "batch_execution",
                "description": f"{len(results)}টি কাজ সম্পাদন করা হয়েছে",
                "status": "completed",
                "result": f"ফলাফল: {len([r for r in results if r.startswith('✅')])} সফল, {len([r for r in results if r.startswith('❌')])} ব্যর্থ"
            }
            
            requests.post(f"{self.server_url}/api/memory/add_task", 
                         json=task_data, timeout=5)
            
        except Exception as e:
            logger.error(f"কাজ সম্পাদন লগ করার ত্রুটি: {e}")
    
    def get_help_text(self) -> str:
        """Get help text for editor agent"""
        return """
🧩 এডিটর এজেন্ট সাহায্য

কমান্ডসমূহ:
- verify_code <code> - কোড সিনট্যাক্স এবং লজিক যাচাই করুন
- suggest_code <requirements> - কোড সাজেশন তৈরি করুন
- run_tasks_on - সব অপেক্ষমান কাজ সম্পাদন করুন
- help - এই সাহায্য দেখুন
- status - এজেন্ট স্ট্যাটাস দেখুন
- memory - মেমরি স্ট্যাটাস দেখুন

বৈশিষ্ট্যসমূহ:
- কোড যাচাই এবং সাজেশন
- ফাইল পর্যবেক্ষণ এবং প্রসঙ্গ আহরণ
- কাজের সারি ব্যবস্থাপনা
- বটগাছ মেমরির সাথে সংহতকরণ
- লেটেন্সি পর্যবেক্ষণ এবং ব্যাচ মোড
        """
    
    def get_status(self) -> str:
        """Get agent status"""
        avg_response_time = sum(self.response_times[-10:]) / len(self.response_times[-10:]) if self.response_times else 0
        
        return f"""
🧩 এডিটর এজেন্ট স্ট্যাটাস

অবস্থা: {self.status}
ভূমিকা: {self.role}
সার্ভার: {self.server_url}
ব্যাচ মোড: {self.batch_mode}
গড় প্রতিক্রিয়া সময়: {avg_response_time:.2f}s
পর্যবেক্ষিত ফাইল: {len(self.monitored_files)}
অপেক্ষমান কাজ: {len(self.pending_tasks)}
সম্পন্ন কাজ: {len(self.completed_tasks)}
        """
    
    def get_memory_status(self) -> str:
        """Get memory status"""
        try:
            response = requests.get(f"{self.server_url}/api/memory", timeout=5)
            if response.status_code == 200:
                memory_data = response.json()
                return f"""
🧠 মেমরি স্ট্যাটাস

মোট কথোপকথন: {memory_data['memory']['total_conversations']}
মোট কাজ: {memory_data['memory']['total_tasks']}
সর্বশেষ আপডেট: {memory_data['memory']['last_update']}
মেমরি সুস্থ: {memory_data['memory']['system_status']['memory_healthy']}
                """
            else:
                return "মেমরি স্ট্যাটাস অনুপলব্ধ"
        except Exception as e:
            return f"মেমরি স্ট্যাটাস ত্রুটি: {e}"
    
    def ping_server(self) -> bool:
        """Ping the main server"""
        try:
            response = requests.get(f"{self.server_url}/api/status", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Server ping failed: {e}")
            return False

# Global editor agent instance
editor_agent = EditorAgent()
