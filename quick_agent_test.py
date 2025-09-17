#!/usr/bin/env python3
"""
⚡ Quick Agent Test - ZombieCoder Industry-Level Agents
"""

import requests
import time

def test_agent_responses():
    """Test different agent responses quickly"""
    
    print("🚀 ZombieCoder Quick Agent Test")
    print("=" * 50)
    
    # Company Information
    company_info = {
        "name": "ZombieCoder",
        "tagline": "যেখানে কোড ও কথা বলে",
        "owner": "Sahon Srabon",
        "company": "Developer Zone",
        "contact": "+880 1323-626282",
        "address": "235 south pirarbag, Amtala Bazar, Mirpur -60 feet",
        "website": "https://zombiecoder.my.id/",
        "email": "infi@zombiecoder.my.id"
    }
    
    print("🏢 Company Information:")
    for key, value in company_info.items():
        print(f"  {key}: {value}")
    
    # Industry-Level Agents
    agents = {
        "Alexander Chen": "Senior Software Architect & CTO",
        "Sofia Rodriguez": "Lead Full-Stack Developer", 
        "Marcus Johnson": "DevOps & Infrastructure Specialist",
        "Elena Petrov": "Security & QA Expert",
        "Kai Nakamura": "Data Science & AI Specialist",
        "Amara Okafor": "Product & UX Specialist"
    }
    
    print(f"\n👥 Industry-Level Team Members:")
    for agent_name, role in agents.items():
        print(f"  {agent_name}: {role}")
    
    print(f"\n🔍 Laravel Latest Version: v12.4.0")
    print(f"📧 Provider: Local Ollama + Cloud Fallback")
    
    # Test Questions
    test_questions = [
        "Laravel এর latest version কি?",
        "আপনার company information কি?",
        "আপনার team members কারা?",
        "Python এ CSV ফাইল কিভাবে পড়া যায়?",
        "আপনার provider এর নাম কি?"
    ]
    
    # Test endpoints
    endpoints = {
        "proxy_server": "http://localhost:8080/proxy/chat",
        "unified_agent": "http://localhost:12345/chat",
        "multi_project": "http://localhost:8001/chat"
    }
    
    print(f"\n🧪 Testing Different Inputs:")
    print("-" * 30)
    
    results = {}
    
    for i, question in enumerate(test_questions[:3], 1):  # Test first 3 questions
        print(f"\n📝 Test {i}: {question}")
        
        for endpoint_name, endpoint_url in endpoints.items():
            try:
                start_time = time.time()
                
                if endpoint_name == "proxy_server":
                    payload = {
                        "messages": [{"role": "user", "content": question}],
                        "context": {"agent": "industry_level"}
                    }
                else:
                    payload = {
                        "message": question,
                        "context": {"agent": "industry_level"}
                    }
                
                response = requests.post(endpoint_url, json=payload, timeout=5)
                end_time = time.time()
                response_time = end_time - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "No response")
                    print(f"  ✅ {endpoint_name} ({response_time:.2f}s): {response_text[:60]}...")
                else:
                    print(f"  ❌ {endpoint_name}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ {endpoint_name}: {str(e)[:40]}...")
    
    print(f"\n✅ Quick testing completed!")
    print(f"💡 Use the working endpoints for immediate responses")

if __name__ == "__main__":
    test_agent_responses()
