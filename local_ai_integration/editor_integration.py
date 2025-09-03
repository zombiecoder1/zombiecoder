#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔌 Editor Integration Helper for ZombieCoder Local AI
===================================================

This script helps editors (Cursor, VS Code) detect and configure
local AI integration automatically.
"""

import os
import json
import requests
import socket
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Flask app setup
app = Flask(__name__)
CORS(app)

class EditorIntegrationHelper:
    """Helper class for editor integration"""
    
    def __init__(self):
        self.local_services = {
            "openai_shim": "http://127.0.0.1:8001",
            "zombiecoder": "http://127.0.0.1:12345",
            "ollama": "http://127.0.0.1:11434"
        }
        
        self.cloud_domains = [
            "api.openai.com",
            "api.anthropic.com",
            "oai.hf.space",
            "openaiapi-site.azureedge.net"
        ]
        
        self.config_files = [
            ".env",
            ".vscode/settings.json",
            ".cursor/settings.json",
            ".cursorrules"
        ]
    
    def detect_local_ai_status(self) -> Dict[str, Any]:
        """Detect local AI services status"""
        status = {
            "local_ai_available": False,
            "cloud_ai_blocked": False,
            "services": {},
            "recommendations": []
        }
        
        # Check local services
        for service_name, url in self.local_services.items():
            try:
                if service_name == "openai_shim":
                    response = requests.get(f"{url}/health", timeout=3)
                    if response.status_code == 200:
                        status["services"][service_name] = {
                            "status": "active",
                            "url": url,
                            "response": response.json()
                        }
                    else:
                        status["services"][service_name] = {
                            "status": "inactive",
                            "url": url,
                            "error": f"Status: {response.status_code}"
                        }
                
                elif service_name == "zombiecoder":
                    response = requests.get(f"{url}/status", timeout=3)
                    if response.status_code == 200:
                        status["services"][service_name] = {
                            "status": "active",
                            "url": url,
                            "response": response.json()
                        }
                    else:
                        status["services"][service_name] = {
                            "status": "inactive",
                            "url": url,
                            "error": f"Status: {response.status_code}"
                        }
                
                elif service_name == "ollama":
                    response = requests.get(f"{url}/api/tags", timeout=3)
                    if response.status_code == 200:
                        data = response.json()
                        status["services"][service_name] = {
                            "status": "active",
                            "url": url,
                            "models": data.get("models", []),
                            "model_count": len(data.get("models", []))
                        }
                    else:
                        status["services"][service_name] = {
                            "status": "inactive",
                            "url": url,
                            "error": f"Status: {response.status_code}"
                        }
                        
            except Exception as e:
                status["services"][service_name] = {
                    "status": "error",
                    "url": url,
                    "error": str(e)
                }
        
        # Check if local AI is available
        active_services = sum(1 for service in status["services"].values() 
                            if service["status"] == "active")
        status["local_ai_available"] = active_services >= 2
        
        # Check cloud AI blocking
        blocked_count = 0
        for domain in self.cloud_domains:
            try:
                socket.gethostbyname(domain)
                # If we can resolve, it's accessible
            except socket.gaierror:
                # If we can't resolve, it's blocked
                blocked_count += 1
        
        status["cloud_ai_blocked"] = blocked_count == len(self.cloud_domains)
        
        # Generate recommendations
        if not status["local_ai_available"]:
            status["recommendations"].append("Start local AI services using SIMPLE_LAUNCHER.bat")
        
        if not status["cloud_ai_blocked"]:
            status["recommendations"].append("Configure hosts file to block cloud AI domains")
        
        if status["local_ai_available"] and status["cloud_ai_blocked"]:
            status["recommendations"].append("✅ Local AI is properly configured and enforced")
        
        return status
    
    def create_editor_configs(self) -> Dict[str, Any]:
        """Create editor configuration files"""
        configs = {}
        
        # Create .env file
        env_content = """# ZombieCoder Local AI Configuration
OPENAI_API_BASE=http://127.0.0.1:8001/v1
OPENAI_API_KEY=local-ai-key
FORCE_LOCAL_AI=true
LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1
ZOMBIECODER_HOST=http://127.0.0.1:12345
OLLAMA_HOST=http://127.0.0.1:11434
AI_PROVIDER=zombiecoder
AI_MODEL=local-llama
EDITOR_MODE=local_ai
"""
        
        try:
            with open(".env", "w", encoding="utf-8") as f:
                f.write(env_content)
            configs[".env"] = "created"
        except Exception as e:
            configs[".env"] = f"error: {e}"
        
        # Create VS Code settings
        vscode_settings = {
            "openai.apiBase": "http://127.0.0.1:8001/v1",
            "openai.apiKey": "local-ai-key",
            "openai.forceLocal": True,
            "zombiecoder.endpoint": "http://127.0.0.1:8001/v1",
            "zombiecoder.apiKey": "local-ai-key",
            "zombiecoder.provider": "local",
            "zombiecoder.model": "local-llama",
            "zombiecoder.forceLocal": True
        }
        
        try:
            os.makedirs(".vscode", exist_ok=True)
            with open(".vscode/settings.json", "w", encoding="utf-8") as f:
                json.dump(vscode_settings, f, indent=2)
            configs[".vscode/settings.json"] = "created"
        except Exception as e:
            configs[".vscode/settings.json"] = f"error: {e}"
        
        # Create Cursor settings
        cursor_settings = {
            "openai.apiBase": "http://127.0.0.1:8001/v1",
            "openai.apiKey": "local-ai-key",
            "openai.forceLocal": True,
            "zombiecoder.endpoint": "http://127.0.0.1:8001/v1",
            "zombiecoder.apiKey": "local-ai-key",
            "zombiecoder.provider": "local",
            "zombiecoder.model": "local-llama",
            "zombiecoder.forceLocal": True
        }
        
        try:
            os.makedirs(".cursor", exist_ok=True)
            with open(".cursor/settings.json", "w", encoding="utf-8") as f:
                json.dump(cursor_settings, f, indent=2)
            configs[".cursor/settings.json"] = "created"
        except Exception as e:
            configs[".cursor/settings.json"] = f"error: {e}"
        
        # Create .cursorrules
        cursorrules_content = """# Cursor AI Local Configuration
# This file configures Cursor to use local AI

# Force local AI usage
FORCE_LOCAL_AI=true
LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1
LOCAL_AI_KEY=local-ai-key
AI_PROVIDER=zombiecoder
AI_MODEL=local-llama
EDITOR_MODE=local_ai

# AI Model Configuration
AI_MODEL=local-llama
AI_PROVIDER=zombiecoder
"""
        
        try:
            with open(".cursorrules", "w", encoding="utf-8") as f:
                f.write(cursorrules_content)
            configs[".cursorrules"] = "created"
        except Exception as e:
            configs[".cursorrules"] = f"error: {e}"
        
        return configs
    
    def test_local_ai_integration(self) -> Dict[str, Any]:
        """Test local AI integration with shorter timeouts"""
        test_results = {
            "openai_shim": {},
            "zombiecoder": {},
            "ollama": {},
            "overall": "unknown"
        }
        
        # Test OpenAI Shim with shorter timeout
        try:
            response = requests.post(
                "http://127.0.0.1:8001/v1/chat/completions",
                json={
                    "model": "local-model",
                    "messages": [{"role": "user", "content": "Say hello briefly"}],
                    "max_tokens": 50
                },
                timeout=10  # Reduced timeout
            )
            
            if response.status_code == 200:
                test_results["openai_shim"] = {
                    "status": "success",
                    "response_time": response.elapsed.total_seconds(),
                    "response": response.json()
                }
            else:
                test_results["openai_shim"] = {
                    "status": "failed",
                    "status_code": response.status_code,
                    "error": response.text
                }
        except Exception as e:
            test_results["openai_shim"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Test ZombieCoder
        try:
            response = requests.get("http://127.0.0.1:12345/status", timeout=5)
            if response.status_code == 200:
                test_results["zombiecoder"] = {
                    "status": "success",
                    "response": response.json()
                }
            else:
                test_results["zombiecoder"] = {
                    "status": "failed",
                    "status_code": response.status_code
                }
        except Exception as e:
            test_results["zombiecoder"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Test Ollama with shorter timeout
        try:
            response = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json={
                    "model": "llama3.2:1b",
                    "prompt": "Say hello briefly",
                    "stream": False
                },
                timeout=10  # Reduced timeout
            )
            
            if response.status_code == 200:
                test_results["ollama"] = {
                    "status": "success",
                    "response_time": response.elapsed.total_seconds(),
                    "response": response.json()
                }
            else:
                test_results["ollama"] = {
                    "status": "failed",
                    "status_code": response.status_code
                }
        except Exception as e:
            test_results["ollama"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Determine overall status
        success_count = sum(1 for service in test_results.values() 
                          if isinstance(service, dict) and service.get("status") == "success")
        
        if success_count >= 2:
            test_results["overall"] = "success"
        elif success_count >= 1:
            test_results["overall"] = "partial"
        else:
            test_results["overall"] = "failed"
        
        return test_results
    
    def generate_integration_report(self) -> str:
        """Generate comprehensive integration report"""
        report = []
        report.append("🔌 ZombieCoder Editor Integration Report")
        report.append("=" * 50)
        report.append("")
        
        # Status detection
        status = self.detect_local_ai_status()
        report.append("📊 STATUS DETECTION:")
        report.append(f"   Local AI Available: {'✅ Yes' if status['local_ai_available'] else '❌ No'}")
        report.append(f"   Cloud AI Blocked: {'✅ Yes' if status['cloud_ai_blocked'] else '❌ No'}")
        report.append("")
        
        # Service status
        report.append("🔧 SERVICE STATUS:")
        for service_name, service_info in status["services"].items():
            icon = "✅" if service_info["status"] == "active" else "❌"
            report.append(f"   {icon} {service_name}: {service_info['status']}")
        report.append("")
        
        # Configuration files
        configs = self.create_editor_configs()
        report.append("📁 CONFIGURATION FILES:")
        for file_path, status in configs.items():
            icon = "✅" if status == "created" else "❌"
            report.append(f"   {icon} {file_path}: {status}")
        report.append("")
        
        # Integration test
        test_results = self.test_local_ai_integration()
        report.append("🧪 INTEGRATION TEST:")
        report.append(f"   Overall Status: {test_results['overall'].upper()}")
        
        for service_name, test_info in test_results.items():
            if service_name != "overall":
                icon = "✅" if test_info.get("status") == "success" else "❌"
                report.append(f"   {icon} {service_name}: {test_info.get('status', 'unknown')}")
        report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS:")
        if "recommendations" in status and isinstance(status["recommendations"], list):
            for rec in status["recommendations"]:
                report.append(f"   • {rec}")
        else:
            report.append("   • No specific recommendations available")
        report.append("")
        
        # Editor setup instructions
        report.append("🚀 EDITOR SETUP INSTRUCTIONS:")
        report.append("")
        report.append("📱 Cursor AI:")
        report.append("   1. Restart Cursor after running this script")
        report.append("   2. Use Ctrl+Shift+I to access AI")
        report.append("   3. AI will automatically use local services")
        report.append("")
        report.append("💻 VS Code:")
        report.append("   1. Install ZombieCoder extension")
        report.append("   2. Use Ctrl+Shift+P → ZombieCoder")
        report.append("   3. AI will use local endpoint automatically")
        report.append("")
        report.append("🔧 Manual Configuration:")
        report.append("   - Environment variables are set automatically")
        report.append("   - .env files created in project directories")
        report.append("   - Settings files configured for local AI")
        
        return "\n".join(report)

# Global instance
helper = EditorIntegrationHelper()

# Flask routes
@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "service": "ZombieCoder Editor Integration",
        "status": "running",
        "port": 8003,
        "description": "Helps editors integrate with local AI services"
    })

@app.route('/status')
def status():
    """Get integration status"""
    try:
        status = helper.detect_local_ai_status()
        return jsonify({
            "status": "running",
            "local_ai_available": status["local_ai_available"],
            "cloud_ai_blocked": status["cloud_ai_blocked"],
            "services": status["services"],
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/services')
def services():
    """Get service status"""
    try:
        status = helper.detect_local_ai_status()
        return jsonify({
            "services": status["services"],
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/config')
def config():
    """Get configuration status"""
    try:
        configs = helper.create_editor_configs()
        return jsonify({
            "configs": configs,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test')
def test():
    """Run integration test"""
    try:
        test_results = helper.test_local_ai_integration()
        return jsonify({
            "test_results": test_results,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/setup', methods=['POST'])
def setup():
    """Setup editor integration"""
    try:
        data = request.get_json() or {}
        editor_type = data.get('editor', 'cursor')  # cursor or vscode
        
        # Create configurations
        configs = helper.create_editor_configs()
        
        return jsonify({
            "message": f"Editor integration setup completed for {editor_type}",
            "configs": configs,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/instructions')
def instructions():
    """Get setup instructions"""
    instructions = {
        "cursor": {
            "steps": [
                "Restart Cursor after running this script",
                "Use Ctrl+Shift+I to access AI",
                "AI will automatically use local services"
            ]
        },
        "vscode": {
            "steps": [
                "Install ZombieCoder extension",
                "Use Ctrl+Shift+P → ZombieCoder",
                "AI will use local endpoint automatically"
            ]
        }
    }
    
    return jsonify({
        "instructions": instructions,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "editor_integration"
    })

if __name__ == "__main__":
    print("🔌 Starting ZombieCoder Editor Integration...")
    print("🌐 Server starting on http://localhost:8003")
    print("📡 Available endpoints:")
    print("   - GET  / (home)")
    print("   - GET  /status (integration status)")
    print("   - GET  /services (service status)")
    print("   - GET  /config (configuration status)")
    print("   - GET  /test (run integration test)")
    print("   - POST /setup (setup integration)")
    print("   - GET  /instructions (setup instructions)")
    print("   - GET  /health (health check)")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=8003, debug=True)
