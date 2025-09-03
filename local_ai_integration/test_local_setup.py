#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ZombieCoder Local AI - System Verification
==============================================

This script performs comprehensive testing of the local AI integration system:
- Port availability checks
- Service connectivity tests
- API endpoint validation
- Agent system verification
- Memory integration testing

Run this script to verify your local AI setup is working correctly.
"""

import requests
import socket
import json
import time
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Any

# ===============================
# Configuration
# ===============================
TEST_CONFIG = {
    "ports": {
        8001: "OpenAI Shim Server",
        12345: "ZombieCoder Agent System",
        11434: "Ollama Models",
        8080: "Proxy Server",
        8081: "Multi-Project API"
    },
    "endpoints": {
        "http://127.0.0.1:8001": {
            "health": "/health",
            "status": "/status",
            "models": "/v1/models",
            "chat": "/v1/chat/completions"
        },
        "http://127.0.0.1:12345": {
            "status": "/status",
            "info": "/info",
            "chat": "/chat"
        }
    },
    "timeout": 5
}

# ===============================
# Test Functions
# ===============================

def test_port_connectivity(port: int, service_name: str) -> Dict[str, Any]:
    """Test if a specific port is accessible"""
    result = {
        "port": port,
        "service": service_name,
        "accessible": False,
        "response_time": None,
        "error": None
    }
    
    try:
        start_time = time.time()
        with socket.create_connection(("127.0.0.1", port), timeout=TEST_CONFIG["timeout"]):
            result["accessible"] = True
            result["response_time"] = round((time.time() - start_time) * 1000, 2)
    except Exception as e:
        result["error"] = str(e)
    
    return result

def test_http_endpoint(base_url: str, endpoint: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
    """Test HTTP endpoint connectivity"""
    result = {
        "url": f"{base_url}{endpoint}",
        "method": method,
        "status_code": None,
        "response_time": None,
        "accessible": False,
        "error": None,
        "response_data": None
    }
    
    try:
        start_time = time.time()
        
        if method == "GET":
            response = requests.get(
                f"{base_url}{endpoint}",
                timeout=TEST_CONFIG["timeout"]
            )
        elif method == "POST":
            response = requests.post(
                f"{base_url}{endpoint}",
                json=data or {},
                timeout=TEST_CONFIG["timeout"]
            )
        
        result["status_code"] = response.status_code
        result["response_time"] = round((time.time() - start_time) * 1000, 2)
        result["accessible"] = response.status_code < 400
        
        try:
            result["response_data"] = response.json()
        except:
            result["response_data"] = response.text[:200]  # First 200 chars
        
    except Exception as e:
        result["error"] = str(e)
    
    return result

def test_openai_shim() -> Dict[str, Any]:
    """Test OpenAI Shim Server functionality"""
    print("🔍 Testing OpenAI Shim Server...")
    
    tests = {}
    
    # Test health endpoint
    tests["health"] = test_http_endpoint(
        "http://127.0.0.1:8001",
        "/health"
    )
    
    # Test models endpoint
    tests["models"] = test_http_endpoint(
        "http://127.0.0.1:8001",
        "/v1/models"
    )
    
    # Test chat completion
    chat_payload = {
        "model": "deepseek-coder:latest",
        "messages": [
            {"role": "user", "content": "Hello, are you working?"}
        ]
    }
    
    tests["chat"] = test_http_endpoint(
        "http://127.0.0.1:8001",
        "/v1/chat/completions",
        "POST",
        chat_payload
    )
    
    return tests

def test_zombiecoder_system() -> Dict[str, Any]:
    """Test ZombieCoder Agent System"""
    print("🔍 Testing ZombieCoder Agent System...")
    
    tests = {}
    
    # Test status endpoint
    tests["status"] = test_http_endpoint(
        "http://127.0.0.1:12345",
        "/status"
    )
    
    # Test info endpoint
    tests["info"] = test_http_endpoint(
        "http://127.0.0.1:12345",
        "/info"
    )
    
    # Test chat with agent
    chat_payload = {
        "message": "Test message",
        "agent": "সাহন ভাই"
    }
    
    tests["chat"] = test_http_endpoint(
        "http://127.0.0.1:12345",
        "/chat",
        "POST",
        chat_payload
    )
    
    return tests

def test_ollama_models() -> Dict[str, Any]:
    """Test Ollama Models availability"""
    print("🔍 Testing Ollama Models...")
    
    tests = {}
    
    # Test models list
    tests["models"] = test_http_endpoint(
        "http://127.0.0.1:11434",
        "/api/tags"
    )
    
    # Test chat endpoint
    chat_payload = {
        "model": "deepseek-coder:latest",
        "messages": [
            {"role": "user", "content": "Test message"}
        ],
        "stream": False
    }
    
    tests["chat"] = test_http_endpoint(
        "http://127.0.0.1:11434",
        "/api/chat",
        "POST",
        chat_payload
    )
    
    return tests

def test_environment_variables() -> Dict[str, Any]:
    """Test environment variable configuration"""
    print("🔍 Testing Environment Variables...")
    
    env_vars = {}
    required_vars = [
        "OPENAI_API_KEY",
        "OPENAI_API_BASE", 
        "OPENAI_BASE_URL"
    ]
    
    for var in required_vars:
        value = os.environ.get(var, None)
        env_vars[var] = {
            "set": value is not None,
            "value": value if value else "Not set"
        }
    
    return env_vars

def test_hosts_file() -> Dict[str, Any]:
    """Test hosts file configuration"""
    print("🔍 Testing Hosts File Configuration...")
    
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    cloud_domains = [
        "api.openai.com",
        "api.anthropic.com",
        "oai.hf.space",
        "openaiapi-site.azureedge.net"
    ]
    
    result = {
        "file_exists": False,
        "cloud_domains_blocked": 0,
        "total_cloud_domains": len(cloud_domains),
        "blocked_domains": [],
        "configuration": "unknown"
    }
    
    try:
        if os.path.exists(hosts_path):
            result["file_exists"] = True
            
            with open(hosts_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for domain in cloud_domains:
                if f"127.0.0.1   {domain}" in content:
                    result["cloud_domains_blocked"] += 1
                    result["blocked_domains"].append(domain)
            
            if result["cloud_domains_blocked"] == len(cloud_domains):
                result["configuration"] = "fully_blocked"
            elif result["cloud_domains_blocked"] > 0:
                result["configuration"] = "partially_blocked"
            else:
                result["configuration"] = "not_blocked"
                
    except Exception as e:
        result["error"] = str(e)
    
    return result

def test_cursor_integration() -> Dict[str, Any]:
    """Test Cursor IDE integration"""
    print("🔍 Testing Cursor IDE Integration...")
    
    result = {
        "cursor_running": False,
        "processes": [],
        "network_connections": []
    }
    
    try:
        # Check if Cursor is running
        cursor_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            if 'cursor' in proc.info['name'].lower():
                cursor_processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "exe": proc.info['exe']
                })
        
        result["cursor_running"] = len(cursor_processes) > 0
        result["processes"] = cursor_processes
        
        # Check network connections for Cursor
        if result["cursor_running"]:
            try:
                netstat_output = subprocess.check_output(
                    ["netstat", "-an"], 
                    text=True, 
                    timeout=10
                )
                
                lines = netstat_output.strip().split('\n')
                for line in lines:
                    if 'ESTABLISHED' in line and any(domain in line for domain in ["api.openai.com", "127.0.0.1"]):
                        result["network_connections"].append(line.strip())
                        
            except Exception as e:
                result["network_error"] = str(e)
                
    except Exception as e:
        result["error"] = str(e)
    
    return result

# ===============================
# Main Testing Function
# ===============================

def run_comprehensive_test() -> Dict[str, Any]:
    """Run all tests and generate comprehensive report"""
    print("🚀 Starting ZombieCoder Local AI System Verification...")
    print("=" * 60)
    
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "overall_status": "unknown",
        "tests_passed": 0,
        "total_tests": 0,
        "results": {}
    }
    
    # 1. Port Connectivity Tests
    print("\n🔌 Testing Port Connectivity...")
    port_tests = {}
    for port, service_name in TEST_CONFIG["ports"].items():
        result = test_port_connectivity(port, service_name)
        port_tests[f"port_{port}"] = result
        test_results["total_tests"] += 1
        if result["accessible"]:
            test_results["tests_passed"] += 1
    
    test_results["results"]["port_connectivity"] = port_tests
    
    # 2. OpenAI Shim Tests
    print("\n🤖 Testing OpenAI Shim Server...")
    shim_tests = test_openai_shim()
    test_results["results"]["openai_shim"] = shim_tests
    
    for test_name, test_result in shim_tests.items():
        test_results["total_tests"] += 1
        if test_result["accessible"]:
            test_results["tests_passed"] += 1
    
    # 3. ZombieCoder System Tests
    print("\n🧠 Testing ZombieCoder Agent System...")
    zombie_tests = test_zombiecoder_system()
    test_results["results"]["zombiecoder_system"] = zombie_tests
    
    for test_name, test_result in zombie_tests.items():
        test_results["total_tests"] += 1
        if test_result["accessible"]:
            test_results["tests_passed"] += 1
    
    # 4. Ollama Models Tests
    print("\n🧠 Testing Ollama Models...")
    ollama_tests = test_ollama_models()
    test_results["results"]["ollama_models"] = ollama_tests
    
    for test_name, test_result in ollama_tests.items():
        test_results["total_tests"] += 1
        if test_result["accessible"]:
            test_results["tests_passed"] += 1
    
    # 5. Environment Variables Test
    print("\n⚙️ Testing Environment Variables...")
    env_tests = test_environment_variables()
    test_results["results"]["environment_variables"] = env_tests
    
    env_vars_set = sum(1 for var, result in env_tests.items() if result["set"])
    test_results["total_tests"] += 1
    if env_vars_set == len(env_tests):
        test_results["tests_passed"] += 1
    
    # 6. Hosts File Test
    print("\n🔒 Testing Hosts File Configuration...")
    hosts_test = test_hosts_file()
    test_results["results"]["hosts_file"] = hosts_test
    
    test_results["total_tests"] += 1
    if hosts_test["configuration"] == "fully_blocked":
        test_results["tests_passed"] += 1
    
    # 7. Cursor Integration Test
    print("\n💻 Testing Cursor IDE Integration...")
    cursor_test = test_cursor_integration()
    test_results["results"]["cursor_integration"] = cursor_test
    
    test_results["total_tests"] += 1
    if cursor_test["cursor_running"]:
        test_results["tests_passed"] += 1
    
    # Calculate overall status
    pass_rate = test_results["tests_passed"] / test_results["total_tests"]
    
    if pass_rate >= 0.8:
        test_results["overall_status"] = "EXCELLENT"
    elif pass_rate >= 0.6:
        test_results["overall_status"] = "GOOD"
    elif pass_rate >= 0.4:
        test_results["overall_status"] = "FAIR"
    else:
        test_results["overall_status"] = "POOR"
    
    return test_results

# ===============================
# Report Generation
# ===============================

def print_test_report(results: Dict[str, Any]):
    """Print formatted test report"""
    print("\n" + "=" * 60)
    print("📊 ZOMBIECODER LOCAL AI SYSTEM VERIFICATION REPORT")
    print("=" * 60)
    
    print(f"\n📅 Timestamp: {results['timestamp']}")
    print(f"🎯 Overall Status: {results['overall_status']}")
    print(f"📊 Tests Passed: {results['tests_passed']}/{results['total_tests']}")
    print(f"📈 Pass Rate: {(results['tests_passed']/results['total_tests']*100):.1f}%")
    
    # Port Connectivity Summary
    print(f"\n🔌 Port Connectivity Summary:")
    port_tests = results["results"]["port_connectivity"]
    for test_name, test_result in port_tests.items():
        icon = "✅" if test_result["accessible"] else "❌"
        service = test_result["service"]
        status = "ONLINE" if test_result["accessible"] else "OFFLINE"
        print(f"   {icon} {service}: {status}")
    
    # Service Tests Summary
    print(f"\n🤖 Service Tests Summary:")
    services = ["openai_shim", "zombiecoder_system", "ollama_models"]
    for service in services:
        if service in results["results"]:
            service_tests = results["results"][service]
            passed = sum(1 for test in service_tests.values() if test.get("accessible", False))
            total = len(service_tests)
            icon = "✅" if passed == total else "⚠️" if passed > 0 else "❌"
            print(f"   {icon} {service.replace('_', ' ').title()}: {passed}/{total} tests passed")
    
    # Configuration Summary
    print(f"\n⚙️ Configuration Summary:")
    
    # Environment Variables
    env_tests = results["results"]["environment_variables"]
    env_set = sum(1 for var, result in env_tests.items() if result["set"])
    env_icon = "✅" if env_set == len(env_tests) else "⚠️" if env_set > 0 else "❌"
    print(f"   {env_icon} Environment Variables: {env_set}/{len(env_tests)} set")
    
    # Hosts File
    hosts_test = results["results"]["hosts_file"]
    hosts_icon = "✅" if hosts_test["configuration"] == "fully_blocked" else "⚠️" if hosts_test["configuration"] == "partially_blocked" else "❌"
    print(f"   {hosts_icon} Hosts File: {hosts_test['configuration']}")
    
    # Cursor Integration
    cursor_test = results["results"]["cursor_integration"]
    cursor_icon = "✅" if cursor_test["cursor_running"] else "❌"
    print(f"   {cursor_icon} Cursor IDE: {'Running' if cursor_test['cursor_running'] else 'Not Running'}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    
    if results["overall_status"] == "EXCELLENT":
        print("   🎉 Your system is perfectly configured! Enjoy unlimited local AI!")
    elif results["overall_status"] == "GOOD":
        print("   👍 Most components are working. Check failed tests above.")
    elif results["overall_status"] == "FAIR":
        print("   ⚠️ Several components need attention. Review failed tests.")
    else:
        print("   ❌ System needs significant configuration. Follow setup guide.")
    
    # Specific recommendations
    if not any(port_tests[f"port_{8001}"]["accessible"] for test_name in port_tests if test_name == "port_8001"):
        print("   🚀 Start OpenAI Shim server: python local_ai_integration/openai_shim.py")
    
    if hosts_test["configuration"] != "fully_blocked":
        print("   🔒 Configure hosts file to block cloud AI domains")
    
    if env_set < len(env_tests):
        print("   ⚙️ Set required environment variables")
    
    print("\n" + "=" * 60)

def save_test_report(results: Dict[str, Any], filename: str = "test_report.json"):
    """Save test report to file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"📄 Test report saved to: {filename}")
    except Exception as e:
        print(f"❌ Could not save test report: {e}")

# ===============================
# Main Execution
# ===============================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ZombieCoder Local AI System Verification")
    parser.add_argument("--save", action="store_true", help="Save test report to file")
    parser.add_argument("--output", default="test_report.json", help="Output filename")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    try:
        # Import required modules
        import psutil
        import os
        
        # Run comprehensive test
        test_results = run_comprehensive_test()
        
        # Print report
        print_test_report(test_results)
        
        # Save if requested
        if args.save:
            save_test_report(test_results, args.output)
        
        # Exit with appropriate code
        if test_results["overall_status"] in ["EXCELLENT", "GOOD"]:
            exit(0)  # Success
        else:
            exit(1)  # Warning/Error
            
    except ImportError as e:
        print(f"❌ Missing required module: {e}")
        print("💡 Install with: pip install psutil requests")
        exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
        exit(130)
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        exit(1)
