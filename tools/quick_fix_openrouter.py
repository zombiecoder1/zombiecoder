#!/usr/bin/env python3
"""
🔧 Quick Fix for OpenRouter Configuration
=========================================
This script helps configure OpenRouter API key and test connection
"""

import json
import requests
from pathlib import Path

def configure_openrouter():
    """Configure OpenRouter API key"""
    print("🔧 OpenRouter Configuration")
    print("="*30)
    
    config_file = Path("our-server/config.json")
    if not config_file.exists():
        print("❌ Config file not found")
        return False
    
    # Read current config
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    current_key = config.get('cloud_fallback', {}).get('api_keys', {}).get('openrouter', '')
    
    if current_key:
        print(f"✅ OpenRouter API key already configured: {current_key[:10]}...")
        test_connection = input("Test connection? (y/n): ").lower().strip()
        if test_connection == 'y':
            test_openrouter_connection(current_key)
        return True
    
    print("📝 To get OpenRouter API key:")
    print("1. Go to https://openrouter.ai")
    print("2. Sign up/Login")
    print("3. Go to API Keys section")
    print("4. Create a new API key")
    print("5. Copy the key")
    print()
    
    api_key = input("Enter your OpenRouter API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    # Update config
    if 'cloud_fallback' not in config:
        config['cloud_fallback'] = {}
    if 'api_keys' not in config['cloud_fallback']:
        config['cloud_fallback']['api_keys'] = {}
    
    config['cloud_fallback']['api_keys']['openrouter'] = api_key
    
    # Save config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ OpenRouter API key saved")
    
    # Test connection
    test_connection = input("Test connection now? (y/n): ").lower().strip()
    if test_connection == 'y':
        test_openrouter_connection(api_key)
    
    return True

def test_openrouter_connection(api_key):
    """Test OpenRouter API connection"""
    print("\n🔍 Testing OpenRouter connection...")
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'anthropic/claude-3.5-sonnet',
            'messages': [{'role': 'user', 'content': 'Hello, test message'}],
            'max_tokens': 50
        }
        
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print("✅ OpenRouter connection successful!")
            print(f"📝 Response: {content}")
            return True
        else:
            print(f"❌ OpenRouter error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def show_available_models():
    """Show available OpenRouter models"""
    print("\n📋 Available OpenRouter Models:")
    print("="*40)
    
    models = [
        "anthropic/claude-3.5-sonnet",
        "anthropic/claude-3-haiku",
        "meta-llama/llama-3.1-8b-instruct",
        "openai/gpt-4o-mini",
        "openai/gpt-3.5-turbo",
        "google/gemini-flash-1.5",
        "mistralai/mistral-7b-instruct"
    ]
    
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    print("\n💡 Tip: Use 'anthropic/claude-3.5-sonnet' for best results")

if __name__ == "__main__":
    print("🚀 Zombie Family - OpenRouter Quick Fix")
    print("="*45)
    
    show_available_models()
    
    if configure_openrouter():
        print("\n✅ Configuration completed!")
        print("🚀 You can now use OpenRouter in your Zombie Family system")
    else:
        print("\n❌ Configuration failed")
        print("🔧 Please check your API key and try again")
