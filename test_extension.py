#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ZombieCoder Extension Test Script
====================================

Quick test to verify extension integration
"""

import requests
import json
import os

def test_extension_integration():
    """Test if extension can access local AI services"""
    
    print("🧪 Testing ZombieCoder Extension Integration...")
    print("=" * 50)
    
    # Test 1: Check if local AI services are accessible
    print("\n1️⃣ Testing Local AI Services:")
    
    # OpenAI Shim
    try:
        response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ OpenAI Shim: Active")
        else:
            print(f"   ❌ OpenAI Shim: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ OpenAI Shim: {e}")
    
    # ZombieCoder
    try:
        response = requests.get("http://127.0.0.1:12345/status", timeout=5)
        if response.status_code == 200:
            print("   ✅ ZombieCoder: Active")
        else:
            print(f"   ❌ ZombieCoder: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ ZombieCoder: {e}")
    
    # Test 2: Check configuration files
    print("\n2️⃣ Checking Configuration Files:")
    
    config_files = [".env", ".vscode/settings.json", ".cursor/settings.json", ".cursorrules"]
    for file_path in config_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}: Exists")
        else:
            print(f"   ❌ {file_path}: Missing")
    
    # Test 3: Test AI response
    print("\n3️⃣ Testing AI Response:")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8001/v1/chat/completions",
            json={
                "model": "local-model",
                "messages": [{"role": "user", "content": "Say 'ZombieCoder Extension Test Successful'"}],
                "max_tokens": 100
            },
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"   ✅ AI Response: {content[:100]}...")
        else:
            print(f"   ❌ AI Response Failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ AI Response Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Extension Test Complete!")
    print("\n💡 Next Steps:")
    print("   1. VS Code এ Ctrl+Shift+P → ZombieCoder")
    print("   2. Extension commands test করুন")
    print("   3. Local AI response verify করুন")

if __name__ == "__main__":
    test_extension_integration()
