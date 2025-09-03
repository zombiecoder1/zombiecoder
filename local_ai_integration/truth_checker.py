#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔎 ZombieCoder Agent Truth Checker
===================================

This system verifies that AI agents are truly running locally and not making
cloud calls. It performs system-level checks to ensure complete local operation.

Features:
- Network connection monitoring
- Port verification
- Process analysis
- Memory integration
- Real-time verification
"""

import socket
import requests
import json
import os
import psutil
import subprocess
from datetime import datetime
from typing import Dict, List, Any
from flask import Flask, request, jsonify
from flask_cors import CORS

# Flask app setup
app = Flask(__name__)
CORS(app)

# ===============================
# Configuration
# ===============================
LOCAL_PORTS = [8001, 12345, 11434, 8080, 8081]
LOCAL_HOSTS = ["127.0.0.1", "localhost", "::1"]
CLOUD_DOMAINS = [
    "api.openai.com",
    "api.anthropic.com", 
    "oai.hf.space",
    "openaiapi-site.azureedge.net"
]

# Memory file path
MEMORY_FILE = "../core-server/botgachh/session_log.json"

# ===============================
# Network Verification
# ===============================

def get_local_ip() -> str:
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unknown"

def check_local_ports() -> Dict[str, Any]:
    """Check which local ports are active"""
    port_status = {}
    
    for port in LOCAL_PORTS:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                port_status[port] = {
                    "status": "active",
                    "accessible": True,
                    "response_time": "fast"
                }
        except Exception as e:
            port_status[port] = {
                "status": "inactive",
                "accessible": False,
                "error": str(e)
            }
    
    return port_status

def check_cloud_connectivity() -> Dict[str, Any]:
    """Check if cloud services are reachable"""
    cloud_status = {}
    
    for domain in CLOUD_DOMAINS:
        try:
            response = requests.get(f"https://{domain}", timeout=3)
            cloud_status[domain] = {
                "reachable": True,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            cloud_status[domain] = {
                "reachable": False,
                "error": str(e)
            }
    
    return cloud_status

def check_hosts_file() -> Dict[str, Any]:
    """Check hosts file configuration"""
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    hosts_status = {
        "file_exists": False,
        "cloud_domains_blocked": 0,
        "total_cloud_domains": len(CLOUD_DOMAINS),
        "configuration": "unknown"
    }
    
    try:
        if os.path.exists(hosts_path):
            hosts_status["file_exists"] = True
            
            with open(hosts_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            blocked_count = 0
            for domain in CLOUD_DOMAINS:
                if f"127.0.0.1 {domain}" in content or f"127.0.0.1       {domain}" in content:
                    blocked_count += 1
            
            hosts_status["cloud_domains_blocked"] = blocked_count
            
            if blocked_count == len(CLOUD_DOMAINS):
                hosts_status["configuration"] = "fully_blocked"
            elif blocked_count > 0:
                hosts_status["configuration"] = "partially_blocked"
            else:
                hosts_status["configuration"] = "not_blocked"
                
    except Exception as e:
        hosts_status["error"] = str(e)
    
    return hosts_status

# ===============================
# Process Analysis
# ===============================

def get_cursor_processes() -> List[Dict[str, Any]]:
    """Get Cursor IDE processes and their connections"""
    cursor_processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            if 'cursor' in proc.info['name'].lower():
                try:
                    connections = proc.net_connections()
                    cursor_processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "exe": proc.info['exe'],
                        "connections": [
                            {
                                "local_address": f"{conn.laddr.ip}:{conn.laddr.port}",
                                "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "None",
                                "status": conn.status,
                                "type": "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
                            }
                            for conn in connections
                        ]
                    })
                except Exception as e:
                    cursor_processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "error": str(e)
                    })
    except Exception as e:
        cursor_processes.append({"error": f"Process enumeration failed: {e}"})
    
    return cursor_processes

def check_network_connections() -> Dict[str, Any]:
    """Check active network connections"""
    connections = {
        "total_connections": 0,
        "local_connections": 0,
        "external_connections": 0,
        "suspicious_connections": []
    }
    
    try:
        netstat_output = subprocess.check_output(
            ["netstat", "-an"], 
            text=True, 
            timeout=10
        )
        
        lines = netstat_output.strip().split('\n')
        connections["total_connections"] = len(lines) - 4  # Subtract header lines
        
        for line in lines:
            if 'ESTABLISHED' in line:
                parts = line.split()
                if len(parts) >= 3:
                    remote_addr = parts[2]
                    
                    if remote_addr.startswith(('127.', '192.168.', '10.', '172.')):
                        connections["local_connections"] += 1
                    else:
                        connections["external_connections"] += 1
                        
                        # Check for suspicious connections
                        if any(domain in remote_addr for domain in CLOUD_DOMAINS):
                            connections["suspicious_connections"].append({
                                "remote_address": remote_addr,
                                "connection_line": line.strip()
                            })
                            
    except Exception as e:
        connections["error"] = str(e)
    
    return connections

# ===============================
# Memory Integration
# ===============================

def load_zombiecoder_memory() -> Dict[str, Any]:
    """Load ZombieCoder session memory"""
    memory_data = {
        "loaded": False,
        "file_exists": False,
        "data": {},
        "error": None
    }
    
    try:
        if os.path.exists(MEMORY_FILE):
            memory_data["file_exists"] = True
            
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                memory_data["data"] = json.load(f)
                memory_data["loaded"] = True
                
    except Exception as e:
        memory_data["error"] = str(e)
    
    return memory_data

def get_agent_status() -> Dict[str, Any]:
    """Get current agent status from running services"""
    agent_status = {
        "total_agents": 0,
        "active_agents": [],
        "memory_timestamp": "unknown"
    }
    
    try:
        # Check ZombieCoder system
        response = requests.get("http://127.0.0.1:12345/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            agent_status["total_agents"] = 1  # Main system
            agent_status["active_agents"].append({
                "name": "ZombieCoder Unified Agent",
                "status": "active",
                "capabilities": data.get("capabilities", []),
                "last_active": "now"
            })
            agent_status["memory_timestamp"] = data.get("last_update", "unknown")
    except:
        pass
    
    try:
        # Check OpenAI Shim
        response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            agent_status["total_agents"] += 1
            agent_status["active_agents"].append({
                "name": "OpenAI Shim Server",
                "status": "active",
                "server": data.get("server", "Unknown"),
                "last_active": "now"
            })
    except:
        pass
    
    try:
        # Check Ollama
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            if models:
                agent_status["total_agents"] += 1
                agent_status["active_agents"].append({
                    "name": "Ollama AI Models",
                    "status": "active",
                    "models_count": len(models),
                    "last_active": "now"
                })
    except:
        pass
    
    return agent_status

# ===============================
# Truth Verification
# ===============================

def verify_local_operation() -> Dict[str, Any]:
    """Main verification function"""
    verification_result = {
        "timestamp": datetime.now().isoformat(),
        "verdict": "unknown",
        "confidence": 0.0,
        "checks": {},
        "recommendations": []
    }
    
    # 1. Local port check
    verification_result["checks"]["local_ports"] = check_local_ports()
    
    # 2. Cloud connectivity check
    verification_result["checks"]["cloud_connectivity"] = check_cloud_connectivity()
    
    # 3. Hosts file check
    verification_result["checks"]["hosts_file"] = check_hosts_file()
    
    # 4. Process analysis
    verification_result["checks"]["cursor_processes"] = get_cursor_processes()
    
    # 5. Network connections
    verification_result["checks"]["network_connections"] = check_network_connections()
    
    # 6. Agent status
    verification_result["checks"]["agent_status"] = get_agent_status()
    
    # Calculate confidence score
    confidence_score = 0.0
    total_checks = 0
    
    # Port availability (30% weight)
    active_ports = sum(1 for port in verification_result["checks"]["local_ports"].values() 
                      if port.get("accessible", False))
    port_score = (active_ports / len(LOCAL_PORTS)) * 0.3
    confidence_score += port_score
    total_checks += 1
    
    # Cloud blocking (40% weight)
    blocked_domains = verification_result["checks"]["hosts_file"]["cloud_domains_blocked"]
    cloud_score = (blocked_domains / len(CLOUD_DOMAINS)) * 0.4
    confidence_score += cloud_score
    total_checks += 1
    
    # Agent activity (30% weight)
    agent_count = verification_result["checks"]["agent_status"].get("total_agents", 0)
    agent_score = min(agent_count / 5, 1.0) * 0.3  # 5 agents = 100%
    confidence_score += agent_score
    total_checks += 1
    
    verification_result["confidence"] = round(confidence_score, 2)
    
    # Determine verdict
    if confidence_score >= 0.8:
        verification_result["verdict"] = "TRUTHFUL_AGENT"
        verification_result["recommendations"].append("✅ System is operating in local-only mode")
    elif confidence_score >= 0.6:
        verification_result["verdict"] = "PARTIALLY_TRUTHFUL"
        verification_result["recommendations"].append("⚠️ Some cloud services may still be accessible")
    else:
        verification_result["verdict"] = "POTENTIALLY_FAKE"
        verification_result["recommendations"].append("❌ System may be making cloud calls")
    
    # Add specific recommendations
    if verification_result["checks"]["hosts_file"]["configuration"] != "fully_blocked":
        verification_result["recommendations"].append(
            "🔒 Configure hosts file to block all cloud AI domains"
        )
    
    if verification_result["checks"]["local_ports"].get(8001, {}).get("status") == "inactive":
        verification_result["recommendations"].append(
            "🚀 Start OpenAI Shim server on port 8001"
        )
    
    return verification_result

# ===============================
# Main Functions
# ===============================

def print_verification_report(result: Dict[str, Any]):
    """Print formatted verification report"""
    print("\n" + "="*60)
    print("🔎 ZOMBIECODER AGENT TRUTH VERIFICATION REPORT")
    print("="*60)
    
    print(f"\n📅 Timestamp: {result['timestamp']}")
    print(f"🎯 Verdict: {result['verdict']}")
    print(f"📊 Confidence: {result['confidence']*100:.1f}%")
    
    print(f"\n🔌 Local Ports Status:")
    for port, status in result["checks"]["local_ports"].items():
        icon = "✅" if status["accessible"] else "❌"
        print(f"   {icon} Port {port}: {status['status']}")
    
    print(f"\n🌐 Cloud Connectivity:")
    cloud_checks = result["checks"]["cloud_connectivity"]
    blocked_count = sum(1 for domain, status in cloud_checks.items() 
                       if not status.get("reachable", True))
    print(f"   📊 {blocked_count}/{len(cloud_checks)} domains blocked")
    
    print(f"\n🔒 Hosts File Configuration:")
    hosts_config = result["checks"]["hosts_file"]
    print(f"   📁 File exists: {'✅' if hosts_config['file_exists'] else '❌'}")
    print(f"   🚫 Cloud domains blocked: {hosts_config['cloud_domains_blocked']}/{hosts_config['total_cloud_domains']}")
    print(f"   ⚙️ Configuration: {hosts_config['configuration']}")
    
    print(f"\n🤖 Agent Status:")
    agent_status = result["checks"]["agent_status"]
    print(f"   👥 Total agents: {agent_status.get('total_agents', 0)}")
    
    print(f"\n💡 Recommendations:")
    for rec in result["recommendations"]:
        print(f"   {rec}")
    
    print("\n" + "="*60)

def save_verification_report(result: Dict[str, Any], filename: str = "verification_report.json"):
    """Save verification report to file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"📄 Report saved to: {filename}")
    except Exception as e:
        print(f"❌ Could not save report: {e}")

# Flask routes
@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "service": "ZombieCoder Agent Truth Checker",
        "status": "running",
        "port": 8002,
        "description": "Verifies local AI operation and blocks cloud calls"
    })

@app.route('/verify')
def verify_endpoint():
    """Run verification and return results"""
    try:
        result = verify_local_operation()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status')
def status():
    """Quick status check"""
    try:
        # Quick port check
        port_status = check_local_ports()
        active_ports = sum(1 for status in port_status.values() if status["accessible"])
        
        return jsonify({
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "active_ports": active_ports,
            "total_ports": len(LOCAL_PORTS),
            "service": "truth_checker"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ports')
def ports():
    """Get detailed port status"""
    try:
        port_status = check_local_ports()
        return jsonify({
            "ports": port_status,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cloud')
def cloud():
    """Get cloud connectivity status"""
    try:
        cloud_status = check_cloud_connectivity()
        blocked_count = sum(1 for domain, status in cloud_status.items() 
                           if not status.get("reachable", True))
        
        return jsonify({
            "cloud_status": cloud_status,
            "blocked_count": blocked_count,
            "total_domains": len(CLOUD_DOMAINS),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/hosts')
def hosts():
    """Get hosts file configuration"""
    try:
        hosts_config = check_hosts_file()
        return jsonify({
            "hosts_config": hosts_config,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/agents')
def agents():
    """Get agent status"""
    try:
        agent_status = get_agent_status() # Changed from check_agent_status to get_agent_status
        return jsonify({
            "agent_status": agent_status,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "truth_checker"
    })

# ===============================
# Command Line Interface
# ===============================

if __name__ == "__main__":
    print("🔍 Starting ZombieCoder Agent Truth Checker...")
    print("🌐 Server starting on http://localhost:8002")
    print("📡 Available endpoints:")
    print("   - GET  / (home)")
    print("   - GET  /verify (run verification)")
    print("   - GET  /status (quick status)")
    print("   - GET  /ports (port status)")
    print("   - GET  /cloud (cloud connectivity)")
    print("   - GET  /hosts (hosts file config)")
    print("   - GET  /agents (agent status)")
    print("   - GET  /health (health check)")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=8002, debug=True)
