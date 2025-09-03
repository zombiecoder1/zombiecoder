#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ZombieCoder AI System - Model Test Script
Tests all AI models and services
"""

import requests
import json
import time
import sys
import os

def test_ollama_connection():
    """Test Ollama connection"""
    print("🔍 Testing Ollama connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama connected successfully")
            print(f"📦 Found {len(models)} models:")
            for model in models:
                print(f"   • {model['name']} ({model['size']})")
            return True
        else:
            print(f"❌ Ollama connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama connection error: {e}")
        return False

def test_ai_models():
    """Test AI models"""
    print("\n🧠 Testing AI models...")
    
    models = [
        "llama3:latest",
        "codegemma:7b-instruct", 
        "bakllava:latest",
        "mistral:latest"
    ]
    
    for model in models:
        print(f"🔍 Testing {model}...")
        try:
            # Test model generation
            payload = {
                "model": model,
                "prompt": "Hello, how are you?",
                "stream": False
            }
            
            response = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {model}: Working")
            else:
                print(f"❌ {model}: Failed ({response.status_code})")
                return False
                
        except Exception as e:
            print(f"❌ {model}: Error - {e}")
            return False
    
    return True

def test_main_server():
    """Test main server"""
    print("\n🌐 Testing main server...")
    try:
        response = requests.get("http://localhost:12345/api/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Main server connected")
            print(f"📊 Status: {data.get('status', 'unknown')}")
            print(f"🤖 Agents: {data.get('agents', [])}")
            return True
        else:
            print(f"❌ Main server failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main server error: {e}")
        return False

def test_admin_panel():
    """Test admin panel"""
    print("\n🎛️ Testing admin panel...")
    try:
        response = requests.get("http://localhost:12351", timeout=10)
        if response.status_code == 200:
            print("✅ Admin panel connected")
            return True
        else:
            print(f"❌ Admin panel failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Admin panel error: {e}")
        return False

def test_agent_chat():
    """Test agent chat functionality"""
    print("\n💬 Testing agent chat...")
    try:
        payload = {
            "message": "Hello, test message",
            "agent": "bhai"
        }
        
        response = requests.post(
            "http://localhost:12345/api/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Agent chat working")
            print(f"🤖 Agent: {data.get('agent', 'unknown')}")
            return True
        else:
            print(f"❌ Agent chat failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Agent chat error: {e}")
        return False

def test_system_resources():
    """Test system resources"""
    print("\n💻 Testing system resources...")
    try:
        import psutil
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"📊 CPU Usage: {cpu_percent}%")
        
        # Memory usage
        memory = psutil.virtual_memory()
        print(f"💾 Memory Usage: {memory.percent}%")
        print(f"💾 Available Memory: {memory.available / (1024**3):.2f} GB")
        
        # Disk usage
        disk = psutil.disk_usage('/')
        print(f"💿 Disk Usage: {disk.percent}%")
        print(f"💿 Free Space: {disk.free / (1024**3):.2f} GB")
        
        return True
    except Exception as e:
        print(f"❌ System resources error: {e}")
        return False

def main():
    """Main test function"""
    print("🧟‍♂️ ZombieCoder AI System - Model Test")
    print("=" * 50)
    
    tests = [
        ("Ollama Connection", test_ollama_connection),
        ("AI Models", test_ai_models),
        ("Main Server", test_main_server),
        ("Admin Panel", test_admin_panel),
        ("Agent Chat", test_agent_chat),
        ("System Resources", test_system_resources)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
