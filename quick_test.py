#!/usr/bin/env python3
"""
🚀 Quick ZombieCoder Test - Fast Response System
"""

import requests
import time

def test_fast_responses():
    """Test all services with fast responses"""
    
    print("🚀 Quick ZombieCoder Test - Fast Response System")
    print("=" * 50)
    
    # Test questions
    questions = [
        "Python এ CSV ফাইল কিভাবে পড়া যায়?",
        "JavaScript এ async/await কিভাবে ব্যবহার করব?",
        "সিস্টেম পারফরমেন্স কিভাবে মনিটর করব?"
    ]
    
    endpoints = {
        "proxy_server": "http://localhost:8080/proxy/chat",
        "unified_agent": "http://localhost:12345/chat",
        "multi_project": "http://localhost:8001/chat"
    }
    
    results = {}
    
    for endpoint_name, endpoint_url in endpoints.items():
        print(f"\n🔗 Testing {endpoint_name}...")
        results[endpoint_name] = []
        
        for i, question in enumerate(questions[:2]):  # Only test 2 questions for speed
            print(f"  📝 Question {i+1}: {question[:30]}...")
            
            try:
                start_time = time.time()
                
                if endpoint_name == "proxy_server":
                    payload = {
                        "messages": [{"role": "user", "content": question}],
                        "context": {}
                    }
                else:
                    payload = {
                        "message": question,
                        "context": {}
                    }
                
                response = requests.post(
                    endpoint_url, 
                    json=payload, 
                    timeout=10  # Short timeout
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "No response")
                    print(f"    ✅ Success ({response_time:.2f}s): {response_text[:50]}...")
                    results[endpoint_name].append({
                        "status": "success",
                        "time": response_time,
                        "response": response_text[:100]
                    })
                else:
                    print(f"    ❌ Error {response.status_code}: {response.text[:50]}")
                    results[endpoint_name].append({
                        "status": "error",
                        "time": response_time,
                        "error": response.text[:100]
                    })
                    
            except Exception as e:
                end_time = time.time()
                response_time = end_time - start_time
                print(f"    ❌ Exception ({response_time:.2f}s): {str(e)[:50]}")
                results[endpoint_name].append({
                    "status": "exception",
                    "time": response_time,
                    "error": str(e)[:100]
                })
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 QUICK TEST SUMMARY")
    print("=" * 50)
    
    for endpoint_name, tests in results.items():
        success_count = sum(1 for test in tests if test["status"] == "success")
        total_count = len(tests)
        avg_time = sum(test["time"] for test in tests) / total_count if total_count > 0 else 0
        
        print(f"🔗 {endpoint_name}:")
        print(f"   Success: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
        print(f"   Avg Time: {avg_time:.2f}s")
        
        if success_count > 0:
            print(f"   Status: ✅ Working")
        else:
            print(f"   Status: ❌ Issues")
    
    print("\n🎯 Recommendations:")
    if any(sum(1 for test in results[endpoint] if test["status"] == "success") > 0 
           for endpoint in results):
        print("✅ At least one service is working!")
        print("💡 Use the working service for immediate responses")
    else:
        print("⚠️ All services need optimization")
        print("💡 Check Ollama server and model loading")

if __name__ == "__main__":
    test_fast_responses()
