#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 MCP Configuration Checker and Optimizer
Checks and optimizes MCP settings for ZombieCoder
"""

import json
import os
import requests
from datetime import datetime

def check_mcp_config():
    """Check current MCP configuration"""
    mcp_path = "/home/sahon/.cursor/mcp.json"
    
    print("🔧 MCP CONFIGURATION CHECKER")
    print("=" * 40)
    
    if not os.path.exists(mcp_path):
        print("❌ MCP configuration file not found!")
        return False
    
    try:
        with open(mcp_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✅ MCP configuration file found")
        
        # Check cloud AI blocking
        cloud_blocked = config.get("cloud_ai_blocked", False)
        print(f"🌐 Cloud AI Blocked: {'✅ Yes' if cloud_blocked else '❌ No'}")
        
        # Check local AI availability
        local_ai = config.get("local_ai_available", False)
        print(f"🏠 Local AI Available: {'✅ Yes' if local_ai else '❌ No'}")
        
        # Check services
        services = config.get("services", {})
        print(f"\n📊 Services Status:")
        
        for service_name, service_data in services.items():
            status = service_data.get("status", "unknown")
            url = service_data.get("url", "unknown")
            
            # Test if service is actually running
            try:
                response = requests.get(url, timeout=2)
                actual_status = "✅ Active" if response.status_code == 200 else "❌ Inactive"
            except:
                actual_status = "❌ Not responding"
            
            print(f"   {service_name}: {actual_status} ({status})")
        
        # Check timestamp
        timestamp = config.get("timestamp", "unknown")
        print(f"\n⏰ Last Update: {timestamp}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading MCP config: {e}")
        return False

def optimize_mcp_config():
    """Optimize MCP configuration for better local AI performance"""
    mcp_path = "/home/sahon/.cursor/mcp.json"
    
    print("\n🚀 OPTIMIZING MCP CONFIGURATION")
    print("=" * 40)
    
    try:
        with open(mcp_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Update cloud AI blocking
        config["cloud_ai_blocked"] = True
        
        # Update timestamp
        config["timestamp"] = datetime.now().isoformat()
        
        # Add optimization flags
        config["optimizations"] = {
            "local_only": True,
            "offline_mode": True,
            "performance_mode": True,
            "auto_fallback": False
        }
        
        # Save updated config
        with open(mcp_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ MCP configuration optimized!")
        print("   - Cloud AI blocking enabled")
        print("   - Offline mode enabled")
        print("   - Performance mode enabled")
        print("   - Auto fallback disabled")
        
        return True
        
    except Exception as e:
        print(f"❌ Error optimizing MCP config: {e}")
        return False

def test_local_ai_endpoints():
    """Test all local AI endpoints"""
    print("\n🧪 TESTING LOCAL AI ENDPOINTS")
    print("=" * 40)
    
    endpoints = [
        ("ZombieCoder Agent", "http://localhost:12345"),
        ("OpenAI Shim", "http://localhost:8001"),
        ("Truth Checker", "http://localhost:8002"),
        ("Ollama", "http://localhost:11434")
    ]
    
    results = {}
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print(f"✅ {name}: Active")
                results[name] = True
            else:
                print(f"⚠️  {name}: Responding but status {response.status_code}")
                results[name] = False
        except Exception as e:
            print(f"❌ {name}: Not responding ({str(e)[:50]})")
            results[name] = False
    
    return results

if __name__ == "__main__":
    print("🤖 ZombieCoder MCP Configuration Checker")
    print("=" * 50)
    
    # Check current config
    if check_mcp_config():
        # Optimize config
        optimize_mcp_config()
        
        # Test endpoints
        test_local_ai_endpoints()
        
        print("\n🎯 MCP CONFIGURATION COMPLETE!")
        print("=" * 40)
        print("✅ Configuration checked and optimized")
        print("✅ Local AI endpoints tested")
        print("✅ Ready for offline testing")
    else:
        print("\n❌ MCP configuration check failed!")
