#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Comprehensive Agent Testing Script
Test all agents with different types of questions
"""

import requests
import json
import time
from typing import Dict, Any, List
from datetime import datetime

class AgentTester:
    def __init__(self):
        self.endpoints = {
            "proxy_server": "http://localhost:8080",
            "unified_agent": "http://localhost:12345",
            "multi_project": "http://localhost:8001",
            "editor_chat": "http://localhost:8003"
        }
        
        # Test questions for different scenarios
        self.test_scenarios = [
            {
                "category": "Programming Help",
                "questions": [
                    "Python এ কিভাবে CSV ফাইল পড়া যায়?",
                    "JavaScript এ async/await কিভাবে ব্যবহার করব?",
                    "একটি REST API তৈরি করার পদ্ধতি কি?"
                ]
            },
            {
                "category": "Code Review",
                "questions": [
                    "এই Python কোডটি রিভিউ করুন:\n```python\ndef add(a, b):\n    return a + b\n```",
                    "এই JavaScript function এ কোন সমস্যা আছে?\n```javascript\nfunction divide(a, b) {\n    return a / b;\n}\n```"
                ]
            },
            {
                "category": "System Operations",
                "questions": [
                    "সিস্টেম পারফরমেন্স কিভাবে মনিটর করব?",
                    "Docker container কিভাবে deploy করব?",
                    "Database backup strategy কি?"
                ]
            },
            {
                "category": "Architecture & Design",
                "questions": [
                    "Microservices architecture এর সুবিধা কি?",
                    "Scalable web application কিভাবে design করব?",
                    "API security best practices কি?"
                ]
            },
            {
                "category": "General Questions",
                "questions": [
                    "আজকের তারিখ কি?",
                    "Machine Learning কি?",
                    "Git workflow কিভাবে ব্যবহার করব?"
                ]
            }
        ]
    
    def test_endpoint(self, endpoint_name: str, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Test a specific endpoint with a question"""
        if context is None:
            context = {}
        
        try:
            endpoint_url = self.endpoints[endpoint_name]
            
            if endpoint_name == "proxy_server":
                payload = {
                    "messages": [{"role": "user", "content": question}],
                    "context": context
                }
                response = requests.post(f"{endpoint_url}/proxy/chat", json=payload, timeout=30)
                
            elif endpoint_name == "unified_agent":
                payload = {
                    "message": question,
                    "context": context
                }
                response = requests.post(f"{endpoint_url}/chat", json=payload, timeout=30)
                
            elif endpoint_name == "multi_project":
                payload = {
                    "message": question,
                    "context": context
                }
                response = requests.post(f"{endpoint_url}/chat", json=payload, timeout=30)
                
            elif endpoint_name == "editor_chat":
                payload = {
                    "message": question,
                    "context": context
                }
                response = requests.post(f"{endpoint_url}/chat", json=payload, timeout=30)
            
            return {
                "endpoint": endpoint_name,
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "success": response.status_code == 200,
                "question": question
            }
            
        except Exception as e:
            return {
                "endpoint": endpoint_name,
                "status_code": 0,
                "error": str(e),
                "success": False,
                "question": question
            }
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive test across all endpoints and scenarios"""
        results = {
            "test_timestamp": datetime.now().isoformat(),
            "total_scenarios": len(self.test_scenarios),
            "total_endpoints": len(self.endpoints),
            "scenario_results": [],
            "summary": {
                "total_tests": 0,
                "successful_tests": 0,
                "failed_tests": 0,
                "endpoint_success_rates": {}
            }
        }
        
        # Initialize endpoint success tracking
        for endpoint in self.endpoints.keys():
            results["summary"]["endpoint_success_rates"][endpoint] = {
                "total": 0,
                "successful": 0,
                "rate": 0.0
            }
        
        # Test each scenario
        for scenario in self.test_scenarios:
            print(f"\n🔍 Testing scenario: {scenario['category']}")
            
            scenario_result = {
                "category": scenario["category"],
                "questions": scenario["questions"],
                "endpoint_results": {}
            }
            
            # Test each question with each endpoint
            for question in scenario["questions"]:
                print(f"  📝 Question: {question[:50]}...")
                
                for endpoint_name in self.endpoints.keys():
                    print(f"    🔗 Testing {endpoint_name}...")
                    
                    result = self.test_endpoint(endpoint_name, question, {"category": scenario["category"]})
                    
                    if endpoint_name not in scenario_result["endpoint_results"]:
                        scenario_result["endpoint_results"][endpoint_name] = []
                    
                    scenario_result["endpoint_results"][endpoint_name].append(result)
                    
                    # Update summary statistics
                    results["summary"]["total_tests"] += 1
                    results["summary"]["endpoint_success_rates"][endpoint_name]["total"] += 1
                    
                    if result["success"]:
                        results["summary"]["successful_tests"] += 1
                        results["summary"]["endpoint_success_rates"][endpoint_name]["successful"] += 1
                    else:
                        results["summary"]["failed_tests"] += 1
                    
                    time.sleep(1)  # Delay between requests
            
            results["scenario_results"].append(scenario_result)
        
        # Calculate success rates
        for endpoint in results["summary"]["endpoint_success_rates"]:
            endpoint_stats = results["summary"]["endpoint_success_rates"][endpoint]
            if endpoint_stats["total"] > 0:
                endpoint_stats["rate"] = (endpoint_stats["successful"] / endpoint_stats["total"]) * 100
        
        return results
    
    def display_results(self, results: Dict[str, Any]):
        """Display test results in a formatted way"""
        print("\n" + "="*80)
        print("🤖 ZOMBIECODER AGENT TESTING RESULTS")
        print("="*80)
        
        print(f"\n📊 Test Summary:")
        print(f"  Total Tests: {results['summary']['total_tests']}")
        print(f"  Successful: {results['summary']['successful_tests']}")
        print(f"  Failed: {results['summary']['failed_tests']}")
        print(f"  Success Rate: {(results['summary']['successful_tests']/results['summary']['total_tests']*100):.1f}%")
        
        print(f"\n🔗 Endpoint Success Rates:")
        for endpoint, stats in results["summary"]["endpoint_success_rates"].items():
            status_icon = "✅" if stats["rate"] > 80 else "⚠️" if stats["rate"] > 50 else "❌"
            print(f"  {status_icon} {endpoint}: {stats['rate']:.1f}% ({stats['successful']}/{stats['total']})")
        
        print(f"\n📝 Scenario Results:")
        for scenario in results["scenario_results"]:
            print(f"\n  🎯 {scenario['category']}:")
            
            for endpoint, endpoint_results in scenario["endpoint_results"].items():
                successful_count = sum(1 for r in endpoint_results if r["success"])
                total_count = len(endpoint_results)
                status_icon = "✅" if successful_count == total_count else "⚠️" if successful_count > 0 else "❌"
                
                print(f"    {status_icon} {endpoint}: {successful_count}/{total_count}")
                
                # Show sample responses for successful tests
                for result in endpoint_results[:1]:  # Show first result only
                    if result["success"]:
                        response = result["response"]
                        if isinstance(response, dict):
                            if "choices" in response and response["choices"]:
                                content = response["choices"][0].get("message", {}).get("content", "")
                                print(f"      💬 Sample: {content[:100]}...")
                            elif "response" in response:
                                print(f"      💬 Sample: {str(response['response'])[:100]}...")
                        else:
                            print(f"      💬 Sample: {str(response)[:100]}...")
                        break

def main():
    """Main testing function"""
    print("🚀 Starting Comprehensive Agent Testing...")
    print("="*50)
    
    tester = AgentTester()
    
    # Run comprehensive test
    results = tester.run_comprehensive_test()
    
    # Display results
    tester.display_results(results)
    
    # Save results to file
    with open("comprehensive_agent_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Detailed results saved to: comprehensive_agent_test_results.json")
    print("✅ Comprehensive agent testing completed!")

if __name__ == "__main__":
    main()
