#!/usr/bin/env python3
"""
🔧 Zombie Family Fix Script
===========================
This script fixes common issues:
1. OpenRouter model ID problems
2. Ollama server connection issues
3. Port conflicts
4. Configuration validation
"""

import os
import sys
import subprocess
import requests
import json
import time
import socket
from pathlib import Path

class ZombieFamilyFixer:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.issues_found = []
        self.fixes_applied = []
        
    def check_ollama_status(self):
        """Check if Ollama server is running"""
        print("🔍 Checking Ollama server status...")
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama server is running")
                return True
            else:
                print("❌ Ollama server responded with error")
                self.issues_found.append("Ollama server error")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Ollama server is not running: {e}")
            self.issues_found.append("Ollama server offline")
            return False
    
    def start_ollama_server(self):
        """Try to start Ollama server"""
        print("🚀 Attempting to start Ollama server...")
        try:
            # Check if ollama command exists
            result = subprocess.run(["ollama", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Ollama is installed")
                
                # Try to start ollama serve
                print("🔧 Starting Ollama serve...")
                subprocess.Popen(["ollama", "serve"], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
                
                # Wait for server to start
                for i in range(10):
                    time.sleep(2)
                    if self.check_ollama_status():
                        print("✅ Ollama server started successfully")
                        self.fixes_applied.append("Started Ollama server")
                        return True
                    print(f"⏳ Waiting for Ollama to start... ({i+1}/10)")
                
                print("❌ Ollama server failed to start")
                return False
            else:
                print("❌ Ollama is not installed or not in PATH")
                self.issues_found.append("Ollama not installed")
                return False
                
        except FileNotFoundError:
            print("❌ Ollama command not found")
            self.issues_found.append("Ollama not installed")
            return False
        except Exception as e:
            print(f"❌ Error starting Ollama: {e}")
            self.issues_found.append(f"Ollama start error: {e}")
            return False
    
    def check_openrouter_config(self):
        """Check OpenRouter configuration"""
        print("🔍 Checking OpenRouter configuration...")
        
        # Check if config file exists
        config_file = self.base_dir / "our-server" / "config.json"
        if not config_file.exists():
            print("❌ Config file not found")
            self.issues_found.append("Config file missing")
            return False
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            openrouter_key = config.get('openrouter_key', '')
            if not openrouter_key:
                print("⚠️  OpenRouter API key not configured")
                self.issues_found.append("OpenRouter API key missing")
                return False
            
            print("✅ OpenRouter API key found")
            return True
            
        except Exception as e:
            print(f"❌ Error reading config: {e}")
            self.issues_found.append(f"Config read error: {e}")
            return False
    
    def test_openrouter_connection(self):
        """Test OpenRouter API connection"""
        print("🔍 Testing OpenRouter connection...")
        
        try:
            config_file = self.base_dir / "our-server" / "config.json"
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            openrouter_key = config.get('openrouter_key', '')
            if not openrouter_key:
                print("❌ No OpenRouter API key found")
                return False
            
            headers = {
                'Authorization': f'Bearer {openrouter_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'anthropic/claude-3.5-sonnet',
                'messages': [{'role': 'user', 'content': 'Hello'}],
                'max_tokens': 10
            }
            
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ OpenRouter connection successful")
                return True
            else:
                print(f"❌ OpenRouter error: {response.status_code} - {response.text}")
                self.issues_found.append(f"OpenRouter API error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ OpenRouter connection failed: {e}")
            self.issues_found.append(f"OpenRouter connection error: {e}")
            return False
    
    def check_port_availability(self):
        """Check if required ports are available"""
        print("🔍 Checking port availability...")
        
        ports = [12345, 8080, 8081, 11434]
        available_ports = []
        
        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex(('localhost', port))
                    if result == 0:
                        print(f"⚠️  Port {port} is in use")
                        self.issues_found.append(f"Port {port} in use")
                    else:
                        print(f"✅ Port {port} is available")
                        available_ports.append(port)
            except Exception as e:
                print(f"❌ Error checking port {port}: {e}")
        
        return available_ports
    
    def generate_status_report(self):
        """Generate a comprehensive status report"""
        print("\n" + "="*50)
        print("📊 ZOMBIE FAMILY STATUS REPORT")
        print("="*50)
        
        print(f"\n🔍 Issues Found: {len(self.issues_found)}")
        for issue in self.issues_found:
            print(f"  ❌ {issue}")
        
        print(f"\n🔧 Fixes Applied: {len(self.fixes_applied)}")
        for fix in self.fixes_applied:
            print(f"  ✅ {fix}")
        
        print("\n📋 Recommendations:")
        if "Ollama not installed" in self.issues_found:
            print("  1. Install Ollama from https://ollama.ai")
            print("  2. Add Ollama to your system PATH")
        
        if "OpenRouter API key missing" in self.issues_found:
            print("  3. Get OpenRouter API key from https://openrouter.ai")
            print("  4. Add it to our-server/config.json")
        
        if "Port" in str(self.issues_found):
            print("  5. Check for conflicting services on ports 12345, 8080, 8081, 11434")
        
        print("\n🚀 Next Steps:")
        print("  1. Run: start_ollama.bat (if Ollama not running)")
        print("  2. Run: python our-server/unified_agent_system.py")
        print("  3. Check browser: http://localhost:12345")
        
        print("\n" + "="*50)
    
    def run_all_checks(self):
        """Run all diagnostic checks"""
        print("🔧 Zombie Family Diagnostic Tool")
        print("="*40)
        
        # Check Ollama
        ollama_running = self.check_ollama_status()
        if not ollama_running:
            self.start_ollama_server()
        
        # Check OpenRouter
        self.check_openrouter_config()
        self.test_openrouter_connection()
        
        # Check ports
        self.check_port_availability()
        
        # Generate report
        self.generate_status_report()

if __name__ == "__main__":
    fixer = ZombieFamilyFixer()
    fixer.run_all_checks()
