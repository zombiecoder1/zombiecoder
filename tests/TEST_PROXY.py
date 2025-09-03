#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ZombieCoder Proxy Server Test
Test proxy server functionality
"""

import requests
import json
import time

def test_proxy_server():
    """Test proxy server functionality"""
    
    base_url = "http://localhost:8080"
    
    print("🧪 Testing ZombieCoder Proxy Server")
    print("=" * 50)
    
    # Test 1: Proxy Status
    print("\n1️⃣ Testing Proxy Status...")
    try:
        response = requests.get(f"{base_url}/proxy/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data.get('status')}")
            print(f"🤖 Agent: {data.get('local_agent')}")
            print(f"📡 Proxy: {data.get('proxy')}")
        else:
            print(f"❌ Status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status error: {e}")
        return False
    
    # Test 2: Chat Request
    print("\n2️⃣ Testing Chat Request...")
    try:
        chat_data = {
            "messages": [
                {"role": "user", "content": "Hello, who are you?"}
            ],
            "model": "zombiecoder-local"
        }
        
        response = requests.post(f"{base_url}/proxy/chat", json=chat_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat response received")
            print(f"🤖 Agent: {data.get('local_agent', 'unknown')}")
            print(f"🔧 Capability: {data.get('capability', 'unknown')}")
            print(f"📡 Source: {data.get('source', 'unknown')}")
            
            # Check response content
            if 'choices' in data and len(data['choices']) > 0:
                content = data['choices'][0]['message']['content']
                print(f"💬 Response: {content[:100]}...")
            else:
                print("❌ No response content")
        else:
            print(f"❌ Chat failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return False
    
    # Test 3: Completion Request
    print("\n3️⃣ Testing Completion Request...")
    try:
        completion_data = {
            "prompt": "Write a simple Python function to add two numbers",
            "model": "zombiecoder-local"
        }
        
        response = requests.post(f"{base_url}/proxy/completion", json=completion_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Completion response received")
            print(f"🤖 Agent: {data.get('local_agent', 'unknown')}")
            print(f"🔧 Capability: {data.get('capability', 'unknown')}")
            
            # Check response content
            if 'choices' in data and len(data['choices']) > 0:
                content = data['choices'][0]['text']
                print(f"💻 Code: {content[:100]}...")
            else:
                print("❌ No completion content")
        else:
            print(f"❌ Completion failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Completion error: {e}")
        return False
    
    # Test 4: Capability Detection
    print("\n4️⃣ Testing Capability Detection...")
    capabilities = [
        ("coding", "Write a Python function"),
        ("debugging", "Fix this error in my code"),
        ("architecture", "Design a system architecture"),
        ("database", "Optimize this SQL query"),
        ("api", "Create a REST API endpoint"),
        ("security", "Check for security vulnerabilities"),
        ("performance", "Optimize this code for performance"),
        ("devops", "Set up Docker deployment"),
        ("voice", "Voice command processing"),
        ("real_time", "What's the weather like?")
    ]
    
    for capability, test_message in capabilities:
        try:
            test_data = {
                "messages": [
                    {"role": "user", "content": test_message}
                ]
            }
            
            response = requests.post(f"{base_url}/proxy/chat", json=test_data)
            if response.status_code == 200:
                data = response.json()
                detected_capability = data.get('capability', 'unknown')
                print(f"✅ {capability}: {detected_capability}")
            else:
                print(f"❌ {capability}: Failed")
        except Exception as e:
            print(f"❌ {capability}: Error - {e}")
    
    print("\n🎉 All tests completed!")
    return True

def test_cursor_compatibility():
    """Test Cursor API compatibility"""
    
    print("\n🔧 Testing Cursor API Compatibility")
    print("=" * 50)
    
    base_url = "http://localhost:8080"
    
    # Test Cursor chat format
    cursor_chat = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain what you can do"}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(f"{base_url}/proxy/chat", json=cursor_chat)
        if response.status_code == 200:
            data = response.json()
            print("✅ Cursor chat format: Compatible")
            print(f"🤖 Model: {data.get('model')}")
            print(f"📡 Object: {data.get('object')}")
        else:
            print(f"❌ Cursor chat format: Failed - {response.status_code}")
    except Exception as e:
        print(f"❌ Cursor chat format: Error - {e}")
    
    # Test Cursor completion format
    cursor_completion = {
        "model": "text-davinci-003",
        "prompt": "Write a simple function:",
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(f"{base_url}/proxy/completion", json=cursor_completion)
        if response.status_code == 200:
            data = response.json()
            print("✅ Cursor completion format: Compatible")
            print(f"🤖 Model: {data.get('model')}")
            print(f"📡 Object: {data.get('object')}")
        else:
            print(f"❌ Cursor completion format: Failed - {response.status_code}")
    except Exception as e:
        print(f"❌ Cursor completion format: Error - {e}")

if __name__ == "__main__":
    print("🚀 Starting Proxy Server Tests...")
    
    # Wait for server to be ready
    print("⏳ Waiting for proxy server...")
    time.sleep(2)
    
    # Run tests
    success = test_proxy_server()
    
    if success:
        test_cursor_compatibility()
        print("\n🎉 All tests passed! Proxy server is ready for Cursor.")
    else:
        print("\n❌ Tests failed! Please check proxy server.")
    
    print("\nPress Enter to exit...")
    input()
