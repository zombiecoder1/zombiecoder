#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Chat Endpoints Test Script
Tests different types of questions through various endpoints
"""

import requests
import json
import time
from typing import Dict, Any

class ChatEndpointTester:
    def __init__(self):
        self.base_urls = {
            "proxy": "http://localhost:8080",
            "multi_project": "http://localhost:8001",
            "unified_agent": "http://localhost:12345"
        }
        
    def test_question(self, endpoint: str, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Test a question on specific endpoint"""
        try:
            if endpoint == "proxy":
                return self._test_proxy_chat(question, context)
            elif endpoint == "multi_project":
                return self._test_multi_project_chat(question, context)
            elif endpoint == "unified_agent":
                return self._test_unified_agent_chat(question, context)
            else:
                return {"error": f"Unknown endpoint: {endpoint}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _test_proxy_chat(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Test proxy server chat endpoint"""
        url = f"{self.base_urls['proxy']}/proxy/chat"
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ],
            "context": context or {}
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        return {
            "endpoint": "proxy",
            "status_code": response.status_code,
            "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "question": question
        }
    
    def _test_multi_project_chat(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Test multi-project manager chat endpoint"""
        url = f"{self.base_urls['multi_project']}/chat"
        
        payload = {
            "message": question,
            "context": context or {}
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        return {
            "endpoint": "multi_project",
            "status_code": response.status_code,
            "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "question": question
        }
    
    def _test_unified_agent_chat(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Test unified agent system chat endpoint"""
        url = f"{self.base_urls['unified_agent']}/chat"
        
        payload = {
            "message": question,
            "context": context or {}
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        return {
            "endpoint": "unified_agent",
            "status_code": response.status_code,
            "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "question": question
        }
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive test with different types of questions"""
        
        test_questions = [
            {
                "category": "প্রোগ্রামিং প্রশ্ন",
                "question": "Python এ কিভাবে CSV ফাইল পড়া যায়?",
                "context": {"language": "python", "topic": "file_handling"}
            },
            {
                "category": "কোড রিভিউ প্রশ্ন", 
                "question": "এই কোডের মধ্যে কোন সমস্যা আছে?\n\n```python\ndef add(a, b):\n    return a + b\n```",
                "context": {"language": "python", "topic": "code_review"}
            },
            {
                "category": "সিস্টেম প্রশ্ন",
                "question": "সিস্টেম পারফরমেন্স কিভাবে মনিটর করব?",
                "context": {"topic": "system_monitoring"}
            },
            {
                "category": "সাধারণ প্রশ্ন",
                "question": "আজকের আবহাওয়া কেমন?",
                "context": {"topic": "general"}
            },
            {
                "category": "এডিটর প্রশ্ন",
                "question": "কিভাবে একটি React component তৈরি করব?",
                "context": {"language": "javascript", "framework": "react", "topic": "frontend"}
            }
        ]
        
        results = {
            "test_timestamp": time.time(),
            "total_questions": len(test_questions),
            "endpoints_tested": list(self.base_urls.keys()),
            "results": []
        }
        
        for test_case in test_questions:
            question_results = {
                "category": test_case["category"],
                "question": test_case["question"],
                "context": test_case["context"],
                "endpoint_results": {}
            }
            
            # Test each endpoint
            for endpoint in self.base_urls.keys():
                print(f"Testing {test_case['category']} on {endpoint}...")
                
                result = self.test_question(
                    endpoint, 
                    test_case["question"], 
                    test_case["context"]
                )
                
                question_results["endpoint_results"][endpoint] = result
                
                # Add delay between requests
                time.sleep(1)
            
            results["results"].append(question_results)
        
        return results

def main():
    """Main test function"""
    print("🧪 ZombieCoder Chat Endpoints Comprehensive Test")
    print("=" * 60)
    
    tester = ChatEndpointTester()
    
    # Run comprehensive test
    print("Starting comprehensive test...")
    results = tester.run_comprehensive_test()
    
    # Display results
    print(f"\n📊 Test Results Summary:")
    print(f"Total Questions Tested: {results['total_questions']}")
    print(f"Endpoints Tested: {', '.join(results['endpoints_tested'])}")
    
    for question_result in results["results"]:
        print(f"\n🔍 Category: {question_result['category']}")
        print(f"Question: {question_result['question'][:50]}...")
        
        for endpoint, result in question_result["endpoint_results"].items():
            status = "✅" if result["status_code"] == 200 else "❌"
            print(f"  {endpoint}: {status} (Status: {result['status_code']})")
            
            if "error" in result:
                print(f"    Error: {result['error']}")
            elif result["status_code"] == 200:
                # Try to extract response content
                response = result["response"]
                if isinstance(response, dict):
                    if "choices" in response and response["choices"]:
                        content = response["choices"][0].get("message", {}).get("content", "")
                        print(f"    Response: {content[:100]}...")
                    elif "response" in response:
                        print(f"    Response: {str(response['response'])[:100]}...")
                    else:
                        print(f"    Response: {str(response)[:100]}...")
                else:
                    print(f"    Response: {str(response)[:100]}...")
    
    # Save results to file
    with open("chat_endpoint_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Detailed results saved to: chat_endpoint_test_results.json")
    print("✅ Chat endpoints test completed!")

if __name__ == "__main__":
    main()
