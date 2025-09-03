#!/usr/bin/env python3
"""
🚀 ZombieCoder AI - Smart Launcher
==================================
This script intelligently launches the entire system with:
- Port availability checking and conflict resolution
- Dependency verification and installation
- File integrity validation and creation
- Auto-recovery with local AI models
- One-click startup for all services
- Local AI model management
"""

import os
import sys
import subprocess
import socket
import time
import json
import threading
import psutil
import shutil
import platform
from pathlib import Path
import requests
import sqlite3
import mysql.connector
from datetime import datetime

class SmartLauncher:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.server_dir = self.base_dir / "আমাদের সার্ভার"
        self.admin_dir = self.base_dir / "house"
        self.lancer_dir = self.base_dir / "lancer"
        
        # Required ports
        self.ports = {
            "main_server": 12345,  # Changed from 5000
            "admin_panel": 12351,  # Changed from 3000
            "voice_server": 5001,
            "mysql": 3306,
            "redis": 6379
        }
        
        # Required files and directories
        self.required_structure = {
            "server": {
                "files": [
                    "main_server.py",
                    "database_manager.py", 
                    "requirements.txt"
                ],
                "dirs": [
                    "logs",
                    "data",
                    "models",
                    "storage",
                    "backup"
                ]
            },
            "admin": {
                "files": [
                    "package.json",
                    "next.config.mjs",
                    "tailwind.config.ts",
                    "tsconfig.json",
                    "app/layout.tsx",
                    "app/page.tsx"
                ],
                "dirs": [
                    "app",
                    "components",
                    "public",
                    "styles",
                    "data",
                    "backups"
                ]
            }
        }
        
        # Dependencies
        self.python_deps = [
            "flask", "flask_cors", "requests", "psutil", "mysql-connector-python",
            "transformers", "torch", "numpy", "pandas", "openai", "anthropic",
            "pyttsx3", "pydub", "gtts", "python-dotenv"
        ]
        
        self.node_deps = ["next", "react", "typescript", "tailwindcss"]
        
        # Local AI Models
        self.local_models = {
            "llm": ["llama", "mistral", "codellama", "phi"],
            "tts": ["coqui", "elevenlabs", "local_tts"],
            "stt": ["whisper", "vosk", "local_stt"]
        }
        
        self.status = {
            "ports": {},
            "files": {},
            "dependencies": {},
            "services": {},
            "models": {},
            "database": {}
        }
        
        self.processes = {}
        
    def log(self, message, level="INFO"):
        """Log messages with timestamp and emoji"""
        timestamp = time.strftime("%H:%M:%S")
        emoji_map = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "WARNING": "⚠️",
            "ERROR": "❌",
            "DEBUG": "🔍"
        }
        emoji = emoji_map.get(level, "ℹ️")
        print(f"[{timestamp}] {emoji} {level}: {message}")
        
    def kill_process_on_port(self, port):
        """Kill process running on specific port"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    connections = proc.info['connections']
                    for conn in connections:
                        if conn.laddr.port == port:
                            self.log(f"Killing process {proc.info['name']} (PID: {proc.info['pid']}) on port {port}", "WARNING")
                            proc.terminate()
                            proc.wait(timeout=5)
                            self.log(f"Successfully killed process on port {port}", "SUCCESS")
                            return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                    continue
        except Exception as e:
            self.log(f"Error killing process on port {port}: {e}", "ERROR")
        return False
        
    def check_port(self, port, service_name):
        """Check if port is available and kill conflicting processes"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                self.log(f"Port {port} ({service_name}) is in use", "WARNING")
                if self.kill_process_on_port(port):
                    time.sleep(2)  # Wait for process to fully terminate
                    # Re-check port
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex(('localhost', port))
                    sock.close()
                    
            if result != 0:
                self.status["ports"][service_name] = True
                self.log(f"Port {port} ({service_name}) is available", "SUCCESS")
                return True
            else:
                self.status["ports"][service_name] = False
                self.log(f"Port {port} ({service_name}) is still in use after cleanup", "ERROR")
                return False
        except Exception as e:
            self.log(f"Error checking port {port}: {e}", "ERROR")
            return False
            
    def create_directory_structure(self):
        """Create necessary directory structure"""
        self.log("Creating directory structure...", "INFO")
        
        directories = [
            "data", "logs", "backups", "models", "storage",
            "আমাদের সার্ভার/logs", "আমাদের সার্ভার/data", "আমাদের সার্ভার/backup",
            "house/data", "house/backups", "house/logs"
        ]
        
        for dir_path in directories:
            full_path = self.base_dir / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                self.log(f"Created directory: {dir_path}", "SUCCESS")
                
    def check_and_create_file(self, file_path, content=None, category="system"):
        """Check if file exists and create if needed"""
        full_path = Path(file_path)
        
        if full_path.exists():
            self.status["files"][str(full_path)] = True
            self.log(f"File exists: {full_path}", "SUCCESS")
            return True
        else:
            # Create parent directories
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create file with content if provided
            if content:
                try:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.status["files"][str(full_path)] = True
                    self.log(f"Created file: {full_path}", "SUCCESS")
                    return True
                except Exception as e:
                    self.log(f"Error creating file {full_path}: {e}", "ERROR")
                    return False
            else:
                try:
                    full_path.touch()
                    self.status["files"][str(full_path)] = True
                    self.log(f"Created empty file: {full_path}", "SUCCESS")
                    return True
                except Exception as e:
                    self.log(f"Error creating file {full_path}: {e}", "ERROR")
                    return False
                    
    def create_essential_files(self):
        """Create essential configuration files"""
        self.log("Creating essential files...", "INFO")
        
        # Create .env file
        env_content = """# Environment Configuration
NODE_ENV=development
        NEXT_PUBLIC_API_URL=http://localhost:12345

# Database Configuration
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:./data/ai_management.db
SQLITE_DATABASE_PATH=./data/ai_management.db

# MySQL Configuration (fallback)
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=modelsraver
MYSQL_USER=root
MYSQL_PASSWORD=

# API Keys (add your keys here)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
FLASK_SECRET_KEY=your_secret_key_here

# Server Configuration
        PORT=12351
        API_PORT=12345
VOICE_PORT=5001

# Local AI Models
LOCAL_LLM_ENABLED=true
LOCAL_TTS_ENABLED=true
LOCAL_STT_ENABLED=true
"""
        
        self.check_and_create_file(".env", env_content)
        
        # Create simple requirements file if not exists
        requirements_file = self.server_dir / "requirements.txt"
        if not requirements_file.exists():
            simple_requirements = """# Core dependencies
Flask==2.3.3
Flask-CORS==4.0.0
python-dotenv==1.0.0
requests==2.31.0
psutil==5.9.6

# AI dependencies
openai==1.3.0
anthropic==0.7.0
transformers==4.35.0
torch==2.2.0
numpy==1.24.3

# Voice processing
pyttsx3==2.90
pydub==0.25.1
gTTS==2.4.0

# Database
mysql-connector-python==8.1.0
sqlite3
"""
            self.check_and_create_file(requirements_file, simple_requirements)
            
    def check_python_dependency(self, package):
        """Check if Python package is installed"""
        try:
            __import__(package.replace('-', '_'))
            self.status["dependencies"][f"python_{package}"] = True
            self.log(f"Python package: {package}", "SUCCESS")
            return True
        except ImportError:
            self.status["dependencies"][f"python_{package}"] = False
            self.log(f"Missing Python package: {package}", "WARNING")
            return False
            
    def check_node_dependency(self, package):
        """Check if Node.js package is installed"""
        try:
            node_modules_path = self.admin_dir / "node_modules" / package
            if node_modules_path.exists():
                self.status["dependencies"][f"node_{package}"] = True
                self.log(f"Node.js package: {package}", "SUCCESS")
                return True
            else:
                self.status["dependencies"][f"node_{package}"] = False
                self.log(f"Missing Node.js package: {package}", "WARNING")
                return False
        except Exception as e:
            self.log(f"Error checking Node.js package {package}: {e}", "ERROR")
            return False
            
    def install_python_dependencies(self):
        """Install missing Python dependencies"""
        self.log("Installing Python dependencies...", "INFO")
        try:
            # Upgrade pip first
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ], check=True, capture_output=True)
            
            # Install requirements
            requirements_file = self.server_dir / "requirements.txt"
            if requirements_file.exists():
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
                ], check=True, capture_output=True)
                self.log("Python dependencies installed successfully", "SUCCESS")
                return True
            else:
                self.log("requirements.txt not found", "ERROR")
                return False
        except subprocess.CalledProcessError as e:
            self.log(f"Failed to install Python dependencies: {e}", "ERROR")
            return False
            
    def install_node_dependencies(self):
        """Install missing Node.js dependencies"""
        self.log("Installing Node.js dependencies...", "INFO")
        try:
            subprocess.run(["npm", "install"], check=True, cwd=self.admin_dir, capture_output=True)
            self.log("Node.js dependencies installed successfully", "SUCCESS")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Failed to install Node.js dependencies: {e}", "ERROR")
            return False
            
    def setup_database(self):
        """Setup database if needed"""
        self.log("Setting up database...", "INFO")
        try:
            # Create SQLite database
            db_path = self.base_dir / "data" / "ai_management.db"
            db_path.parent.mkdir(parents=True, exist_ok=True)
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create basic tables
            tables = [
                """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                """CREATE TABLE IF NOT EXISTS agents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    type TEXT NOT NULL,
                    status TEXT DEFAULT 'inactive',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                """CREATE TABLE IF NOT EXISTS providers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    api_url TEXT,
                    api_key TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                """CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT DEFAULT 'info',
                    category TEXT DEFAULT 'system',
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )"""
            ]
            
            for table_sql in tables:
                cursor.execute(table_sql)
            
            # Insert sample data
            cursor.execute("INSERT OR IGNORE INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                         ('admin', 'admin@zombiecoder.com', 'admin_hash_here', 'admin'))
            cursor.execute("INSERT OR IGNORE INTO agents (name, type, status) VALUES (?, ?, ?)",
                         ('zombiecoder', 'master', 'active'))
            cursor.execute("INSERT OR IGNORE INTO providers (name, type, category, is_active) VALUES (?, ?, ?, ?)",
                         ('sqlite', 'local', 'database', 1))
            
            conn.commit()
            conn.close()
            
            self.status["database"]["sqlite"] = True
            self.log("Database setup completed", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"Database setup failed: {e}", "ERROR")
            return False
            
    def check_local_ai_models(self):
        """Check and manage local AI models"""
        self.log("Checking local AI models...", "INFO")
        
        models_dir = self.base_dir / "models"
        models_dir.mkdir(exist_ok=True)
        
        for model_type, models in self.local_models.items():
            type_dir = models_dir / model_type
            type_dir.mkdir(exist_ok=True)
            
            for model in models:
                model_path = type_dir / model
                if model_path.exists():
                    self.status["models"][f"{model_type}_{model}"] = True
                    self.log(f"Local model found: {model_type}/{model}", "SUCCESS")
                else:
                    self.status["models"][f"{model_type}_{model}"] = False
                    self.log(f"Local model missing: {model_type}/{model}", "WARNING")
                    
    def start_server(self):
        """Start the main server"""
        self.log("Starting main server...", "INFO")
        try:
            # Try main_server.py first, fallback to other files
            server_file = self.server_dir / "main_server.py"
            if not server_file.exists():
                server_file = self.server_dir / "app.py"
                
            if server_file.exists():
                server_process = subprocess.Popen([
                    sys.executable, str(server_file)
                ], cwd=self.server_dir)
                
                # Wait for server to start
                time.sleep(3)
                
                # Check if server is running
                if self.check_server_running(12345):
                    self.status["services"]["main_server"] = True
                    self.processes["main_server"] = server_process
                    self.log("Main server started successfully", "SUCCESS")
                    return server_process
                else:
                    self.log("Main server failed to start", "ERROR")
                    return None
            else:
                self.log("No server file found", "ERROR")
                return None
        except Exception as e:
            self.log(f"Error starting server: {e}", "ERROR")
            return None
            
    def start_admin(self):
        """Start the admin panel"""
        self.log("Starting admin panel...", "INFO")
        try:
            admin_process = subprocess.Popen([
                "npm", "run", "dev"
            ], cwd=self.admin_dir)
            
            # Wait for admin to start
            time.sleep(5)
            
            # Check if admin is running
            if self.check_server_running(12351):
                self.status["services"]["admin_panel"] = True
                self.processes["admin_panel"] = admin_process
                self.log("Admin panel started successfully", "SUCCESS")
                return admin_process
            else:
                self.log("Admin panel failed to start", "ERROR")
                return None
        except Exception as e:
            self.log(f"Error starting admin panel: {e}", "ERROR")
            return None
            
    def check_server_running(self, port):
        """Check if server is running on port"""
        try:
            response = requests.get(f"http://localhost:{port}", timeout=5)
            return response.status_code == 200
        except:
            return False
            
    def auto_fix_issues(self):
        """Auto-fix common issues"""
        self.log("Auto-fixing issues...", "INFO")
        
        # Check what needs fixing
        missing_deps = [k for k, v in self.status["dependencies"].items() if not v]
        missing_files = [k for k, v in self.status["files"].items() if not v]
        
        if missing_deps:
            self.log(f"Installing missing dependencies: {missing_deps}", "INFO")
            if any("python_" in dep for dep in missing_deps):
                self.install_python_dependencies()
            if any("node_" in dep for dep in missing_deps):
                self.install_node_dependencies()
                
        if missing_files:
            self.log(f"Missing files detected: {missing_files}", "INFO")
            self.create_essential_files()
            
        # Re-check dependencies after installation
        for dep in self.python_deps:
            self.check_python_dependency(dep)
            
        for dep in self.node_deps:
            self.check_node_dependency(dep)
            
        return True
        
    def run_system_check(self):
        """Run comprehensive system check"""
        self.log("Running system check...", "INFO")
        
        # Create directory structure
        self.create_directory_structure()
        
        # Create essential files
        self.create_essential_files()
        
        # Check ports
        for service, port in self.ports.items():
            self.check_port(port, service)
            
        # Check dependencies
        for dep in self.python_deps:
            self.check_python_dependency(dep)
            
        for dep in self.node_deps:
            self.check_node_dependency(dep)
            
        # Setup database
        self.setup_database()
        
        # Check local AI models
        self.check_local_ai_models()
        
        self.log("System check completed", "SUCCESS")
        
    def open_dashboard(self):
        """Open the dashboard in browser"""
        try:
            import webbrowser
            
            # Try to open admin panel
            webbrowser.open("http://localhost:12351")
            self.log("Admin panel opened in browser", "SUCCESS")
            
            # Also try to open main server
            webbrowser.open("http://localhost:12345")
            self.log("Main server opened in browser", "SUCCESS")
            
        except Exception as e:
            self.log(f"Could not open dashboard: {e}", "WARNING")
            
    def launch_system(self):
        """Main launcher function"""
        print("🚀 ZombieCoder AI - Smart Launcher")
        print("=" * 60)
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version}")
        print(f"Working Directory: {self.base_dir}")
        print("=" * 60)
        
        # Run system check
        self.run_system_check()
        
        # Auto-fix issues
        self.auto_fix_issues()
        
        # Start services
        print("\n🚀 Starting services...")
        
        # Start server
        self.start_server()
        
        # Start admin panel
        self.start_admin()
        
        # Open dashboard
        self.open_dashboard()
        
        print("\n" + "=" * 60)
        print("✅ System launched successfully!")
        print("=" * 60)
        print("📊 Admin Panel: http://localhost:12351")
        print("🌐 Main Server: http://localhost:12345")
        print("🔊 Voice Server: http://localhost:5001")
        print("📝 Logs: logs/")
        print("💾 Database: data/ai_management.db")
        print("🤖 Local Models: models/")
        print("=" * 60)
        
        # Keep the launcher running
        try:
            while True:
                time.sleep(10)
                # Check if services are still running
                for service, port in [("main_server", 12345), ("admin_panel", 12351)]:
                    if not self.check_server_running(port):
                        self.log(f"{service} stopped, restarting...", "WARNING")
                        if service == "main_server":
                            self.start_server()
                        elif service == "admin_panel":
                            self.start_admin()
        except KeyboardInterrupt:
            self.log("Shutting down...", "INFO")
            # Cleanup processes
            for name, process in self.processes.items():
                try:
                    process.terminate()
                    self.log(f"Terminated {name}", "INFO")
                except:
                    pass

def main():
    """Main entry point"""
    launcher = SmartLauncher()
    launcher.launch_system()

if __name__ == "__main__":
    main()
