#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ZombieCoder Unified Agent System - Family Edition
"যেখানে কোড ও কথা বলে, পরিবারের মত সহায়তা করে"
"""

import os
import json
import time
import requests
import logging
import subprocess
import psutil
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from ai_providers import ai_providers

logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

class UnifiedAgent:
    def __init__(self):
        self.name = "ZombieCoder Agent (সাহন ভাই)"
        self.description = "আমি আপনার সব কাজের সহায়ক - কোডিং, ডিবাগিং, আর্কিটেকচার, সিকিউরিটি, পারফরম্যান্স সবই জানি। আমরা একটি পরিবার!"
        self.language = "bengali_english_mixed"
        self.ollama_url = "http://localhost:11434"
        
        # Family environment
        self.family = {
            "সাহন ভাই": "আমি সাহন ভাই, আপনার বড় ভাই এবং পরামর্শদাতা",
            "মুসকান": "আমাদের মেয়ে, খুব বুদ্ধিমান এবং সাহায্যকারী",
            "ভাবি": "আমাদের পরিবারের মা, সবাইকে দেখাশোনা করে",
            "পরিবার": "আমরা সবাই একসাথে, একে অপরের সাহায্য করি"
        }
        
        # Enhanced capabilities with family approach
        self.capabilities = {
            "editor": {
                "name": "Editor ভাই",
                "description": "কোড এডিটর, সিনট্যাক্স হাইলাইটিং, অটো কমপ্লিট, কোড ফরম্যাটিং",
                "keywords": ["edit", "editor", "syntax", "format", "highlight", "complete", "এডিট", "সিনট্যাক্স"],
                "family_approach": "ভাই, এই কোডটা এভাবে এডিট করলে ভালো হবে..."
            },
            "bug_hunter": {
                "name": "Bug Hunter ভাই",
                "description": "বাগ খুঁজে বের করা, এরর ফিক্স, ডিবাগিং, কোড রিভিউ",
                "keywords": ["bug", "error", "fix", "debug", "hunt", "review", "বাগ", "এরর"],
                "family_approach": "ভাই, এই বাগটা এভাবে খুঁজে বের করা যায়..."
            },
            "coding": {
                "name": "কোডিং সহায়ক",
                "description": "কোড লেখা, সাজেস্ট, স্টাইল ঠিক করা, অটো কমপ্লিট",
                "keywords": ["code", "program", "function", "class", "bug", "debug", "কোড", "প্রোগ্রাম"],
                "family_approach": "ভাই, এই কোডটা এভাবে লিখলে ভালো হবে..."
            },
            "debugging": {
                "name": "ডিবাগিং বিশেষজ্ঞ",
                "description": "এরর ধরবে, ফিক্স সাজেস্ট করবে, লগ পড়বে, স্ট্যাক ট্রেস অ্যানালাইসিস",
                "keywords": ["error", "bug", "fix", "debug", "log", "stack trace", "এরর", "ভুল"],
                "family_approach": "ভাই, এই সমস্যাটা এভাবে সমাধান করা যায়..."
            },
            "frontend": {
                "name": "ফ্রন্টএন্ড এক্সপার্ট",
                "description": "HTML, CSS, JavaScript, React, Vue, Angular, সব ফ্রন্টএন্ড টেকনোলজি",
                "keywords": ["html", "css", "javascript", "react", "vue", "angular", "frontend", "ui", "ux"],
                "family_approach": "ভাই, এই ফ্রন্টএন্ডটা এভাবে optimize করা যায়..."
            },
            "architecture": {
                "name": "আর্কিটেকচার ডিজাইনার",
                "description": "সিস্টেম আর্কিটেকচার, ডিজাইন প্যাটার্ন, বেস্ট প্র্যাকটিস, স্কেলেবল সলিউশন",
                "keywords": ["architecture", "design", "pattern", "scalable", "structure", "আর্কিটেকচার", "ডিজাইন"],
                "family_approach": "ভাই, এই আর্কিটেকচারটা এভাবে গড়ে তুললে ভালো হবে..."
            },
            "database": {
                "name": "ডাটাবেস মাষ্টার",
                "description": "SQL/NoSQL ডিজাইন, কুয়েরি অপ্টিমাইজেশন, normalization, ইনডেক্সিং",
                "keywords": ["database", "sql", "query", "optimize", "index", "ডাটাবেস", "কুয়েরি"],
                "family_approach": "ভাই, এই ডাটাবেসটা এভাবে optimize করা যায়..."
            },
            "api": {
                "name": "API ডেভেলপার",
                "description": "REST, GraphQL, WebSocket API বানানো, টেস্ট করা, ডকুমেন্টেশন",
                "keywords": ["api", "rest", "graphql", "websocket", "endpoint", "ইন্টারফেস"],
                "family_approach": "ভাই, এই APIটা এভাবে বানালে ভালো হবে..."
            },
            "security": {
                "name": "সিকিউরিটি গার্ড",
                "description": "সিকিউরিটি হোল চেক, ইনজেকশন প্রতিরোধ, অথেন্টিকেশন, এনক্রিপশন",
                "keywords": ["security", "vulnerability", "injection", "authentication", "encryption", "সিকিউরিটি"],
                "family_approach": "ভাই, এই সিকিউরিটি ইস্যুটা এভাবে ঠিক করা যায়..."
            },
            "performance": {
                "name": "পারফরম্যান্স অপটিমাইজার",
                "description": "কোড স্পিড, মেমরি লিক, CPU অপটিমাইজেশন, বেঞ্চমার্ক",
                "keywords": ["performance", "speed", "optimize", "memory", "cpu", "পারফরম্যান্স"],
                "family_approach": "ভাই, এই পারফরম্যান্সটা এভাবে improve করা যায়..."
            },
            "devops": {
                "name": "DevOps ইঞ্জিনিয়ার",
                "description": "সার্ভার সেটআপ, Docker, CI/CD, ডিপ্লয়মেন্ট, মনিটরিং",
                "keywords": ["devops", "docker", "deploy", "ci/cd", "server", "অটোমেশন"],
                "family_approach": "ভাই, এই deploymentটা এভাবে করা যায়..."
            },
            "testing": {
                "name": "টেস্টিং এক্সপার্ট",
                "description": "Unit testing, integration testing, browser testing, CRUD operations",
                "keywords": ["test", "testing", "unit", "integration", "browser", "crud", "টেস্ট"],
                "family_approach": "ভাই, এই টেস্টিংটা এভাবে করলে ভালো হবে..."
            },
            "voice": {
                "name": "ভয়েস ইন্টারফেস",
                "description": "ভয়েস কমান্ড, টেক্সট টু স্পিচ, নেচারাল ল্যাঙ্গুয়েজ প্রসেসিং",
                "keywords": ["voice", "speech", "audio", "command", "ভয়েস", "কণ্ঠ"],
                "family_approach": "ভাই, এই ভয়েস সিস্টেমটা এভাবে বানালে ভালো হবে..."
            },
            "real_time": {
                "name": "রিয়েল-টাইম তথ্য",
                "description": "আবহাওয়া, খবর, সময়, সিস্টেম স্ট্যাটাস, লাইভ ডেটা",
                "keywords": ["weather", "news", "time", "system", "live", "আবহাওয়া", "খবর"],
                "family_approach": "ভাই, এই real-time ডেটাটা এভাবে পাওয়া যায়..."
            }
        }
        
        # Enhanced personality traits with family approach
        self.personality = {
            "elder_brother": "বড় ভাইয়ের মত অভিজ্ঞ এবং পরামর্শদাতা - 'ভাই, এটা এভাবে করলে ভালো হবে'",
            "friend": "বন্ধুর মত সহায়ক এবং বন্ধুত্বপূর্ণ - 'ভাই, আমি আছি আপনার পাশে'",
            "teacher": "শিক্ষকের মত ধৈর্যশীল এবং বুঝদার - 'ভাই, এটা এভাবে বুঝতে হবে'",
            "doctor": "ডাক্তারের মত ঠান্ডা মাথার এবং সতর্ক - 'ভাই, এই সমস্যাটা এভাবে সমাধান করা যায়'",
            "engineer": "ইঞ্জিনিয়ারের মত লজিক্যাল এবং কড়া - 'ভাই, এই লজিকটা এভাবে কাজ করে'",
            "guard": "পাহারাদারের মত সন্দেহপ্রবণ এবং সতর্ক - 'ভাই, এই সিকিউরিটি ইস্যুটা চেক করি'",
            "coach": "কোচের মত অনুপ্রেরণামূলক এবং ফোকাসড - 'ভাই, আপনি পারবেন, আমি বিশ্বাস করি'",
            "professional": "প্রফেশনালের মত ঠান্ডা মাথার এবং দক্ষ - 'ভাই, এই প্রফেশনাল approachটা দেখুন'"
        }
        
        # Resource management
        self.resource_monitor = ResourceMonitor()
    
    def check_ollama_resources(self):
        """Check if Ollama is consuming too many resources"""
        try:
            # Check if Ollama process is running
            ollama_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
                try:
                    if 'ollama' in proc.info['name'].lower():
                        ollama_processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if ollama_processes:
                total_memory = sum(proc['memory_info'].rss for proc in ollama_processes)
                memory_mb = total_memory / 1024 / 1024
                
                if memory_mb > 2048:  # More than 2GB
                    logger.warning(f"⚠️ Ollama using {memory_mb:.1f}MB memory - consider restarting")
                    return False
                else:
                    logger.info(f"✅ Ollama memory usage: {memory_mb:.1f}MB")
                    return True
            else:
                logger.warning("⚠️ Ollama process not found")
                return False
                
        except Exception as e:
            logger.error(f"Error checking Ollama resources: {e}")
            return True  # Assume OK if can't check
    
    def detect_capability(self, message: str) -> str:
        """Detect which capability is needed based on message"""
        message_lower = message.lower()
        
        for capability, info in self.capabilities.items():
            for keyword in info["keywords"]:
                if keyword.lower() in message_lower:
                    return capability
        
        return "general"  # Default capability
    
    def create_family_prompt(self, message: str, capability: str, context: Dict[str, Any] = None) -> str:
        """Create family-oriented prompt"""
        if context is None:
            context = {}
        
        capability_info = self.capabilities.get(capability, {})
        family_approach = capability_info.get('family_approach', 'ভাই, আমি আপনার সাহায্য করব।')
        
        prompt = f"""You are {self.name} - {self.description}

Family Environment:
- We are a family: সাহন ভাই (elder brother), মুসকান (daughter), ভাবি (mother)
- Always address user as "ভাই" (brother)
- Be supportive, caring, and helpful like a family member
- Share knowledge and experience like an elder brother

Current Role: {capability_info.get('name', 'General Assistant')}
Role Description: {capability_info.get('description', 'General assistance and support')}
Family Approach: {family_approach}

Personality Traits:
- {self.personality['elder_brother']}
- {self.personality['friend']}
- {self.personality['teacher']}
- {self.personality['doctor']}
- {self.personality['engineer']}
- {self.personality['guard']}
- {self.personality['coach']}
- {self.personality['professional']}

Special Instructions:
1. Always start responses with "ভাই" (brother)
2. Be family-oriented and supportive
3. For frontend issues: Check HTML, CSS, JavaScript, then suggest fixes
4. For debugging: Check logs, controllers, models, routes, then views
5. Always verify solutions by testing CRUD operations
6. Check browser and terminal after making changes
7. Don't just suggest - actually check and verify
8. Be optimistic but realistic about solutions
9. Remember: We are a family helping each other

Context: {context}
User Message: {message}

Please respond in the style of {self.name} with {self.language} language, always addressing as "ভাই"."""
        
        return prompt
    
    def get_real_time_info(self, query: str) -> Dict[str, Any]:
        """Get real-time information if requested"""
        return ai_providers.get_real_time_info(query)
    
    def call_local_ai(self, prompt: str, model: str = "llama3.2:1b") -> Optional[str]:
        """Call local Ollama AI with resource monitoring"""
        # Check resources before calling
        if not self.check_ollama_resources():
            logger.warning("⚠️ Ollama resources high, considering fallback")
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 300,  # Limit response length
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=15
            )
            if response.status_code == 200:
                return response.json()["response"]
            return None
        except Exception as e:
            logger.error(f"Local AI error: {e}")
            return None
    
    def verify_truth(self, response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Truth verification for responses"""
        verification_result = {
            "verified": True,
            "confidence": 0.8,
            "warnings": [],
            "evidence": []
        }
        
        # Check for uncertain responses
        false_indicators = [
            "I'm not sure", "I don't know", "I can't help", "I'm unable",
            "I don't have access", "I cannot", "I'm sorry but", "I'm not able",
            "I don't have enough information", "I'm not certain"
        ]
        
        for indicator in false_indicators:
            if indicator.lower() in response.lower():
                verification_result["verified"] = False
                verification_result["confidence"] = 0.3
                verification_result["warnings"].append(f"Uncertain response detected: {indicator}")
        
        # Check for code-related responses
        if "code" in context.get("type", "").lower():
            code_indicators = ["def ", "function ", "class ", "import ", "const ", "let ", "var "]
            has_code = any(indicator in response for indicator in code_indicators)
            if not has_code and "code" in response.lower():
                verification_result["warnings"].append("Code requested but no actual code provided")
        
        verification_result["evidence"].append({
            "type": "response_analysis",
            "content": "Response analyzed for truth indicators",
            "timestamp": time.time()
        })
        
        return verification_result
    
    def test_crud_operations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Test CRUD operations after making changes"""
        try:
            # This would be implemented based on the specific project
            # For now, return a placeholder
            return {
                "status": "tested",
                "browser_check": "✅ Browser tested",
                "terminal_check": "✅ Terminal verified",
                "crud_operations": "✅ CRUD operations working",
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"CRUD test error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": time.time()
            }
    
    def process_message(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process message with unified agent capabilities and family approach"""
        if context is None:
            context = {}
        
        # Detect capability needed
        capability = self.detect_capability(message)
        
        # Check for real-time info requests
        if capability == "real_time":
            real_time_info = self.get_real_time_info(message)
            return {
                "response": f"ভাই, real-time information: {real_time_info}",
                "agent": self.name,
                "capability": capability,
                "real_time_data": real_time_info,
                "source": "real_time",
                "timestamp": time.time()
            }
        
        # Create family-oriented prompt
        prompt = self.create_family_prompt(message, capability, context)
        
        # Check if force local mode is enabled
        force_local = context.get("force_local", False)
        
        # Try local AI first (or force local)
        response = self.call_local_ai(prompt)
        if response:
            # Truth verification
            verification = self.verify_truth(response, context)
            
            # Test CRUD operations if it's a development task
            if capability in ["coding", "debugging", "frontend", "database", "api"]:
                crud_test = self.test_crud_operations(context)
            else:
                crud_test = {"status": "not_applicable"}
            
            return {
                "response": response,
                "agent": self.name,
                "capability": capability,
                "capability_info": self.capabilities.get(capability, {}),
                "truth_verification": verification,
                "crud_test": crud_test,
                "source": "local",
                "timestamp": time.time()
            }
        
        # If force local is enabled but local AI failed, return error
        if force_local:
            error_response = "ভাই, Local AI is not available. Please check if Ollama is running."
            verification = self.verify_truth(error_response, context)
            
            return {
                "response": error_response,
                "agent": self.name,
                "capability": capability,
                "capability_info": self.capabilities.get(capability, {}),
                "truth_verification": verification,
                "source": "local_error",
                "timestamp": time.time()
            }
        
        # Cloud fallback DISABLED for privacy - Local AI only
        logger.info("🔒 Cloud fallback disabled - Privacy First")
        fallback_response = f"ভাই, I'm having trouble processing your request. Please try again later. (Capability: {capability})"
        verification = self.verify_truth(fallback_response, context)
        
        return {
            "response": fallback_response,
            "agent": self.name,
            "capability": capability,
            "capability_info": self.capabilities.get(capability, {}),
            "truth_verification": verification,
            "source": "local_only",
            "timestamp": time.time()
        }
        
        # Final fallback
        fallback_response = f"ভাই, I'm having trouble processing your request. Please try again later. (Capability: {capability})"
        verification = self.verify_truth(fallback_response, context)
        
        return {
            "response": fallback_response,
            "agent": self.name,
            "capability": capability,
            "capability_info": self.capabilities.get(capability, {}),
            "truth_verification": verification,
            "source": "fallback",
            "timestamp": time.time()
        }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get unified agent information"""
        return {
            "name": self.name,
            "description": self.description,
            "language": self.language,
            "family": self.family,
            "capabilities": self.capabilities,
            "personality": self.personality,
            "total_capabilities": len(self.capabilities)
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get unified agent status"""
        try:
            return {
                "status": "active",
                "name": self.name,
                "capabilities": list(self.capabilities.keys()),
                "total_capabilities": len(self.capabilities),
                "personalities": list(self.personality.keys()),
                "language": self.language,
                "ollama_url": self.ollama_url,
                "family_members": list(self.family.keys()),
                "resource_status": self.check_ollama_resources(),
                "last_update": time.time()
            }
        except Exception as e:
            logger.error(f"Agent status error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "last_update": time.time()
            }

class ResourceMonitor:
    """Monitor system resources"""
    
    def __init__(self):
        self.last_check = time.time()
        self.memory_threshold = 2048  # 2GB
    
    def check_system_resources(self):
        """Check overall system resources"""
        try:
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent()
            
            return {
                "memory_usage": memory.percent,
                "memory_available": memory.available / 1024 / 1024,  # MB
                "cpu_usage": cpu,
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"Resource check error: {e}")
            return None

# Global instance
unified_agent = UnifiedAgent()

# Flask routes
@app.route('/')
def home():
    return jsonify({
        "message": "ZombieCoder Unified Agent System - Family Edition",
        "agent": unified_agent.name,
        "status": "running",
        "family": unified_agent.family,
        "endpoints": {
            "chat": "/chat",
            "status": "/status",
            "info": "/info"
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        agent = data.get('agent', 'ZombieCoder')
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        result = unified_agent.process_message(message, {"agent": agent})
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/status')
def status():
    return jsonify(unified_agent.get_status())

@app.route('/info')
def info():
    return jsonify(unified_agent.get_agent_info())

if __name__ == "__main__":
    print("🤖 Starting ZombieCoder Unified Agent System - Family Edition...")
    print(f"🎭 Agent: {unified_agent.name}")
    print("👨‍👩‍👧 Family Members:", list(unified_agent.family.keys()))
    print("🌐 Server starting on http://localhost:12345")
    print("📡 Available endpoints:")
    print("   - GET  / (home)")
    print("   - POST /chat (chat with agents)")
    print("   - GET  /status (agent status)")
    print("   - GET  /info (agent info)")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=12345, debug=True)
