#!/usr/bin/env python3
"""
🚀 Comprehensive Chat Testing - ZombieCoder Industry-Level Agents
Testing different inputs with various agent personalities
"""

import requests
import time
import json
from typing import Dict, Any, List

class ZombieCoderChatTester:
    """Comprehensive chat testing system"""
    
    def __init__(self):
        self.company_info = {
            "name": "ZombieCoder",
            "tagline": "যেখানে কোড ও কথা বলে",
            "owner": "Sahon Srabon",
            "company": "Developer Zone",
            "contact": "+880 1323-626282",
            "address": "235 south pirarbag, Amtala Bazar, Mirpur -60 feet",
            "website": "https://zombiecoder.my.id/",
            "email": "infi@zombiecoder.my.id"
        }
        
        self.industry_agents = {
            "Alexander Chen": "Senior Software Architect & CTO - System Architecture, Microservices, Cloud Infrastructure",
            "Sofia Rodriguez": "Lead Full-Stack Developer - React, Node.js, Python, TypeScript, Database Design",
            "Marcus Johnson": "DevOps & Infrastructure Specialist - AWS, Docker, Kubernetes, CI/CD, Monitoring",
            "Elena Petrov": "Security & QA Expert - Cybersecurity, Testing, Code Review, Compliance",
            "Kai Nakamura": "Data Science & AI Specialist - Machine Learning, Data Analytics, AI/ML, Statistics",
            "Amara Okafor": "Product & UX Specialist - Product Strategy, User Experience, Market Analysis, Agile"
        }
        
        self.test_scenarios = [
            {
                "category": "Laravel Development",
                "questions": [
                    "Laravel এর latest version কি? এবং কিভাবে install করব?",
                    "Laravel এ Eloquent ORM কিভাবে ব্যবহার করব?",
                    "Laravel এ middleware কিভাবে create করব?",
                    "Laravel এ API development এর best practices কি?"
                ]
            },
            {
                "category": "System Architecture",
                "questions": [
                    "Microservices architecture এর সুবিধা কি?",
                    "Scalable web application কিভাবে design করব?",
                    "Database sharding strategy কি?",
                    "Load balancing কিভাবে implement করব?"
                ]
            },
            {
                "category": "Security & DevOps",
                "questions": [
                    "API security best practices কি?",
                    "Docker container কিভাবে secure করব?",
                    "CI/CD pipeline কিভাবে setup করব?",
                    "Kubernetes deployment strategy কি?"
                ]
            },
            {
                "category": "Data Science & AI",
                "questions": [
                    "Machine Learning model কিভাবে deploy করব?",
                    "Data preprocessing এর best practices কি?",
                    "AI model performance কিভাবে evaluate করব?",
                    "Real-time data processing কিভাবে implement করব?"
                ]
            },
            {
                "category": "Product & UX",
                "questions": [
                    "User experience design এর principles কি?",
                    "Product roadmap কিভাবে create করব?",
                    "Market analysis কিভাবে conduct করব?",
                    "Agile methodology কিভাবে implement করব?"
                ]
            },
            {
                "category": "General Technical",
                "questions": [
                    "আজকের তারিখ কি?",
                    "আপনার provider এর নাম কি?",
                    "আপনার team members কারা?",
                    "আপনার company information কি?"
                ]
            }
        ]
        
        self.endpoints = {
            "proxy_server": "http://localhost:8080/proxy/chat",
            "unified_agent": "http://localhost:12345/chat",
            "multi_project": "http://localhost:8001/chat"
        }
    
    def test_endpoint(self, endpoint_name: str, endpoint_url: str, question: str, category: str) -> Dict[str, Any]:
        """Test a specific endpoint with a question"""
        try:
            start_time = time.time()
            
            if endpoint_name == "proxy_server":
                payload = {
                    "messages": [{"role": "user", "content": question}],
                    "context": {"category": category, "agent": "industry_level"}
                }
            else:
                payload = {
                    "message": question,
                    "context": {"category": category, "agent": "industry_level"}
                }
            
            response = requests.post(endpoint_url, json=payload, timeout=15)
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "No response")
                
                return {
                    "status": "success",
                    "time": response_time,
                    "response": response_text,
                    "agent": data.get("agent", "Unknown"),
                    "capability": data.get("capability", "Unknown"),
                    "source": data.get("source", "Unknown")
                }
            else:
                return {
                    "status": "error",
                    "time": response_time,
                    "error": f"HTTP {response.status_code}: {response.text[:100]}",
                    "response": None
                }
                
        except Exception as e:
            return {
                "status": "exception",
                "time": 0,
                "error": str(e)[:100],
                "response": None
            }
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive testing across all scenarios"""
        print("🚀 ZombieCoder Comprehensive Chat Testing")
        print("=" * 60)
        print(f"🏢 Company: {self.company_info['name']}")
        print(f"📧 Email: {self.company_info['email']}")
        print(f"🌐 Website: {self.company_info['website']}")
        print(f"👥 Team Members: {len(self.industry_agents)}")
        print("=" * 60)
        
        results = {}
        total_tests = 0
        successful_tests = 0
        
        for scenario in self.test_scenarios:
            category = scenario["category"]
            print(f"\n🔍 Testing Category: {category}")
            print("-" * 40)
            
            results[category] = {}
            
            for question in scenario["questions"]:
                print(f"\n📝 Question: {question[:50]}...")
                results[category][question] = {}
                
                for endpoint_name, endpoint_url in self.endpoints.items():
                    print(f"  🔗 Testing {endpoint_name}...")
                    
                    result = self.test_endpoint(endpoint_name, endpoint_url, question, category)
                    results[category][question][endpoint_name] = result
                    
                    total_tests += 1
                    if result["status"] == "success":
                        successful_tests += 1
                        print(f"    ✅ Success ({result['time']:.2f}s): {result['response'][:50]}...")
                        if result.get('agent'):
                            print(f"    🤖 Agent: {result['agent']}")
                        if result.get('capability'):
                            print(f"    🔧 Capability: {result['capability']}")
                    else:
                        print(f"    ❌ {result['status']}: {result.get('error', 'Unknown error')}")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Category-wise results
        print(f"\n📈 Category-wise Results:")
        for category, category_results in results.items():
            category_success = 0
            category_total = 0
            
            for question, question_results in category_results.items():
                for endpoint_name, result in question_results.items():
                    category_total += 1
                    if result["status"] == "success":
                        category_success += 1
            
            category_rate = (category_success / category_total * 100) if category_total > 0 else 0
            print(f"  {category}: {category_success}/{category_total} ({category_rate:.1f}%)")
        
        # Endpoint-wise results
        print(f"\n🔗 Endpoint-wise Results:")
        for endpoint_name in self.endpoints.keys():
            endpoint_success = 0
            endpoint_total = 0
            
            for category_results in results.values():
                for question_results in category_results.values():
                    if endpoint_name in question_results:
                        endpoint_total += 1
                        if question_results[endpoint_name]["status"] == "success":
                            endpoint_success += 1
            
            endpoint_rate = (endpoint_success / endpoint_total * 100) if endpoint_total > 0 else 0
            print(f"  {endpoint_name}: {endpoint_success}/{endpoint_total} ({endpoint_rate:.1f}%)")
        
        # Save detailed results
        with open('comprehensive_chat_test_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                "company_info": self.company_info,
                "industry_agents": self.industry_agents,
                "test_results": results,
                "summary": {
                    "total_tests": total_tests,
                    "successful_tests": successful_tests,
                    "success_rate": success_rate
                }
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed results saved to: comprehensive_chat_test_results.json")
        
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "success_rate": success_rate,
            "results": results
        }

def main():
    """Main function to run comprehensive testing"""
    tester = ZombieCoderChatTester()
    
    # Display company and agent information
    print("🏢 ZombieCoder Company Information:")
    for key, value in tester.company_info.items():
        print(f"  {key}: {value}")
    
    print(f"\n👥 Industry-Level Team Members:")
    for agent_name, description in tester.industry_agents.items():
        print(f"  {agent_name}: {description}")
    
    print(f"\n🔍 Laravel Latest Version: v12.4.0")
    print(f"📧 Provider: Local Ollama + Cloud Fallback")
    
    # Run comprehensive testing
    results = tester.run_comprehensive_test()
    
    print(f"\n✅ Comprehensive testing completed!")
    print(f"🎯 Overall Success Rate: {results['success_rate']:.1f}%")

if __name__ == "__main__":
    main()
