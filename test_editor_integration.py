#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 Editor Integration Test Script
Tests editor-specific functionality and chat capabilities
"""

import requests
import json
import time
from typing import Dict, Any

class EditorIntegrationTester:
    def __init__(self):
        self.editor_url = "http://localhost:8003"
        self.proxy_url = "http://localhost:8080"
        self.unified_agent_url = "http://localhost:12345"
        
    def test_editor_endpoints(self) -> Dict[str, Any]:
        """Test all editor integration endpoints"""
        results = {
            "timestamp": time.time(),
            "endpoints": {}
        }
        
        # Test health endpoint
        try:
            response = requests.get(f"{self.editor_url}/health", timeout=10)
            results["endpoints"]["health"] = {
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "status": "✅" if response.status_code == 200 else "❌"
            }
        except Exception as e:
            results["endpoints"]["health"] = {"error": str(e), "status": "❌"}
        
        # Test editor status
        try:
            response = requests.get(f"{self.editor_url}/status", timeout=10)
            results["endpoints"]["status"] = {
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "status": "✅" if response.status_code == 200 else "❌"
            }
        except Exception as e:
            results["endpoints"]["status"] = {"error": str(e), "status": "❌"}
        
        # Test editor capabilities
        try:
            response = requests.get(f"{self.editor_url}/capabilities", timeout=10)
            results["endpoints"]["capabilities"] = {
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "status": "✅" if response.status_code == 200 else "❌"
            }
        except Exception as e:
            results["endpoints"]["capabilities"] = {"error": str(e), "status": "❌"}
        
        return results
    
    def test_editor_chat_scenarios(self) -> Dict[str, Any]:
        """Test editor-specific chat scenarios"""
        
        test_scenarios = [
            {
                "name": "Code Generation Request",
                "payload": {
                    "message": "একটি Python function লিখুন যা CSV ফাইল পড়ে এবং ডেটা clean করে",
                    "context": {
                        "file_type": "python",
                        "cursor_position": {"line": 10, "column": 5},
                        "project_type": "data_processing"
                    }
                }
            },
            {
                "name": "Code Review Request", 
                "payload": {
                    "message": "এই কোডটি রিভিউ করুন এবং উন্নতির পরামর্শ দিন",
                    "context": {
                        "file_type": "javascript",
                        "code_snippet": "function add(a, b) {\n    return a + b;\n}",
                        "project_type": "frontend"
                    }
                }
            },
            {
                "name": "Bug Fix Request",
                "payload": {
                    "message": "এই error টি কিভাবে fix করব? TypeError: Cannot read property 'map' of undefined",
                    "context": {
                        "file_type": "javascript",
                        "error_type": "TypeError",
                        "project_type": "react_app"
                    }
                }
            },
            {
                "name": "Architecture Question",
                "payload": {
                    "message": "একটি scalable web application এর architecture কিভাবে design করব?",
                    "context": {
                        "file_type": "general",
                        "project_type": "fullstack",
                        "scale": "enterprise"
                    }
                }
            },
            {
                "name": "Performance Optimization",
                "payload": {
                    "message": "এই React component এর performance কিভাবে optimize করব?",
                    "context": {
                        "file_type": "jsx",
                        "component_type": "react_component",
                        "issue": "slow_rendering"
                    }
                }
            }
        ]
        
        results = {
            "timestamp": time.time(),
            "total_scenarios": len(test_scenarios),
            "scenarios": []
        }
        
        for scenario in test_scenarios:
            print(f"Testing scenario: {scenario['name']}")
            
            scenario_result = {
                "name": scenario["name"],
                "payload": scenario["payload"],
                "endpoint_results": {}
            }
            
            # Test with editor integration
            try:
                response = requests.post(
                    f"{self.editor_url}/chat",
                    json=scenario["payload"],
                    timeout=30
                )
                scenario_result["endpoint_results"]["editor"] = {
                    "status_code": response.status_code,
                    "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                    "status": "✅" if response.status_code == 200 else "❌"
                }
            except Exception as e:
                scenario_result["endpoint_results"]["editor"] = {
                    "error": str(e),
                    "status": "❌"
                }
            
            # Test with proxy server
            try:
                proxy_payload = {
                    "messages": [
                        {
                            "role": "user", 
                            "content": scenario["payload"]["message"]
                        }
                    ],
                    "context": scenario["payload"].get("context", {})
                }
                
                response = requests.post(
                    f"{self.proxy_url}/proxy/chat",
                    json=proxy_payload,
                    timeout=30
                )
                scenario_result["endpoint_results"]["proxy"] = {
                    "status_code": response.status_code,
                    "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                    "status": "✅" if response.status_code == 200 else "❌"
                }
            except Exception as e:
                scenario_result["endpoint_results"]["proxy"] = {
                    "error": str(e),
                    "status": "❌"
                }
            
            # Test with unified agent
            try:
                response = requests.post(
                    f"{self.unified_agent_url}/chat",
                    json=scenario["payload"],
                    timeout=30
                )
                scenario_result["endpoint_results"]["unified_agent"] = {
                    "status_code": response.status_code,
                    "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                    "status": "✅" if response.status_code == 200 else "❌"
                }
            except Exception as e:
                scenario_result["endpoint_results"]["unified_agent"] = {
                    "error": str(e),
                    "status": "❌"
                }
            
            results["scenarios"].append(scenario_result)
            time.sleep(1)  # Delay between requests
        
        return results
    
    def test_memory_integration(self) -> Dict[str, Any]:
        """Test editor memory integration"""
        
        memory_tests = [
            {
                "action": "store",
                "payload": {
                    "key": "user_preference",
                    "value": {
                        "language": "python",
                        "coding_style": "clean_code",
                        "framework": "fastapi"
                    }
                }
            },
            {
                "action": "retrieve",
                "payload": {
                    "key": "user_preference"
                }
            },
            {
                "action": "store",
                "payload": {
                    "key": "project_context",
                    "value": {
                        "project_name": "test_project",
                        "technologies": ["python", "react", "postgresql"],
                        "last_activity": time.time()
                    }
                }
            }
        ]
        
        results = {
            "timestamp": time.time(),
            "memory_tests": []
        }
        
        for test in memory_tests:
            try:
                endpoint = f"/memory/{test['action']}"
                response = requests.post(
                    f"{self.editor_url}{endpoint}",
                    json=test["payload"],
                    timeout=10
                )
                
                results["memory_tests"].append({
                    "action": test["action"],
                    "status_code": response.status_code,
                    "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                    "status": "✅" if response.status_code == 200 else "❌"
                })
            except Exception as e:
                results["memory_tests"].append({
                    "action": test["action"],
                    "error": str(e),
                    "status": "❌"
                })
        
        return results

def main():
    """Main test function"""
    print("🎨 ZombieCoder Editor Integration Test")
    print("=" * 50)
    
    tester = EditorIntegrationTester()
    
    # Test 1: Editor endpoints
    print("\n1. Testing Editor Endpoints...")
    endpoint_results = tester.test_editor_endpoints()
    
    print("Editor Endpoint Status:")
    for endpoint, result in endpoint_results["endpoints"].items():
        print(f"  {endpoint}: {result['status']}")
        if "error" in result:
            print(f"    Error: {result['error']}")
    
    # Test 2: Editor chat scenarios
    print("\n2. Testing Editor Chat Scenarios...")
    chat_results = tester.test_editor_chat_scenarios()
    
    print(f"Total Scenarios Tested: {chat_results['total_scenarios']}")
    for scenario in chat_results["scenarios"]:
        print(f"\n📝 {scenario['name']}:")
        for endpoint, result in scenario["endpoint_results"].items():
            print(f"  {endpoint}: {result['status']}")
            if "error" in result:
                print(f"    Error: {result['error']}")
            elif result["status_code"] == 200:
                response = result["response"]
                if isinstance(response, dict):
                    if "choices" in response and response["choices"]:
                        content = response["choices"][0].get("message", {}).get("content", "")
                        print(f"    Response: {content[:100]}...")
                    elif "response" in response:
                        print(f"    Response: {str(response['response'])[:100]}...")
    
    # Test 3: Memory integration
    print("\n3. Testing Memory Integration...")
    memory_results = tester.test_memory_integration()
    
    print("Memory Integration Tests:")
    for test in memory_results["memory_tests"]:
        print(f"  {test['action']}: {test['status']}")
        if "error" in test:
            print(f"    Error: {test['error']}")
    
    # Save comprehensive results
    comprehensive_results = {
        "test_timestamp": time.time(),
        "endpoint_tests": endpoint_results,
        "chat_scenarios": chat_results,
        "memory_tests": memory_results
    }
    
    with open("editor_integration_test_results.json", "w", encoding="utf-8") as f:
        json.dump(comprehensive_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Detailed results saved to: editor_integration_test_results.json")
    print("✅ Editor integration test completed!")

if __name__ == "__main__":
    main()
