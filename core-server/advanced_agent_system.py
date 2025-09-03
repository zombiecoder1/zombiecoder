#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ZombieCoder Advanced Agent System
"যেখানে কোড ও কথা বলে, পরিবারের মত সহায়তা করে"

Features:
- Lazy Loading for Performance
- Memory Management
- Agent Personalities with 10 Capabilities Each
- Industry Best Practices
- Resource Optimization
- Auto-Response System
"""

import os
import json
import time
import logging
import requests
import threading
import psutil
import gc
from datetime import datetime
from typing import Dict, Any, Optional, List
from flask import Flask, request, jsonify
from flask_cors import CORS
import weakref

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryManager:
    """Advanced Memory Management with Lazy Loading"""
    
    def __init__(self):
        self.memory_cache = {}
        self.session_data = {}
        self.conversation_history = []
        self.max_history = 100
        self.max_cache_size = 50
        self.lock = threading.Lock()
        
    def add_to_history(self, message: str, response: str, agent: str):
        """Add conversation to history with memory management"""
        with self.lock:
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'message': message,
                'response': response,
                'agent': agent
            })
            
            # Cleanup old history if too long
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = self.conversation_history[-self.max_history:]
                
    def get_context(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation context"""
        return self.conversation_history[-limit:] if self.conversation_history else []
        
    def cleanup_memory(self):
        """Cleanup memory and force garbage collection"""
        with self.lock:
            if len(self.memory_cache) > self.max_cache_size:
                # Remove oldest entries
                oldest_keys = sorted(self.memory_cache.keys(), 
                                   key=lambda k: self.memory_cache[k].get('timestamp', 0))[:10]
                for key in oldest_keys:
                    del self.memory_cache[key]
                    
        # Force garbage collection
        gc.collect()
        
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        process = psutil.Process()
        return {
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'cache_size': len(self.memory_cache),
            'history_size': len(self.conversation_history),
            'cpu_percent': process.cpu_percent()
        }

class AgentPersonality:
    """Individual Agent Personalities with 10 Capabilities Each"""
    
    def __init__(self, name: str, personality_data: Dict[str, Any]):
        self.name = name
        self.personality = personality_data
        self.is_loaded = False
        self.load_time = None
        
    def lazy_load(self):
        """Lazy load personality data only when needed"""
        if not self.is_loaded:
            logger.info(f"🔄 Loading personality for {self.name}")
            self.is_loaded = True
            self.load_time = datetime.now()
            # Simulate loading time
            time.sleep(0.1)
            
    def get_prompt(self, message: str, context: List[Dict] = None) -> str:
        """Get personalized prompt for the agent with ভাই prefix"""
        self.lazy_load()
        
        base_prompt = self.personality.get('base_prompt', '')
        style = self.personality.get('style', '')
        expertise = self.personality.get('expertise', '')
        capabilities = self.personality.get('capabilities', [])
        
        context_str = ""
        if context:
            context_str = "\n\nPrevious conversation:\n"
            for conv in context[-3:]:  # Last 3 conversations
                context_str += f"User: {conv['message']}\n{self.name}: ভাই, {conv['response']}\n"
        
        capabilities_str = "\n".join([f"- {cap}" for cap in capabilities])
        
        return f"""{base_prompt}

{self.name} এর বিশেষত্ব: {expertise}
{self.name} এর কথা বলার ধরন: {style}

{self.name} এর ১০টি ক্ষমতা:
{capabilities_str}

মহুত্বপূর্ণ: প্রতিটি উত্তরের শুরুতে "ভাই," লিখতে হবে।

{context_str}

User: {message}
{self.name}: ভাই,"""

class AdvancedAgentSystem:
    """Advanced Agent System with Performance Optimization"""
    
    def __init__(self):
        self.name = "ZombieCoder Advanced Agent System"
        self.ollama_url = "http://localhost:11434"
        self.default_model = "llama3.2:1b"
        
        # Memory Manager
        self.memory_manager = MemoryManager()
        
        # Agent Personalities (Lazy Loaded) with 10 Capabilities Each
        self.agent_personalities = {
            'সাহন ভাই': AgentPersonality('সাহন ভাই', {
                'base_prompt': 'আমি সাহন ভাই, আপনার বড় ভাই এবং পরামর্শদাতা। আমি সব বিষয়ে সাহায্য করতে পারি।',
                'style': 'ভাই, বন্ধুত্বপূর্ণ এবং সহায়ক। কোডিং, ডিবাগিং, আর্কিটেকচার সব জানি।',
                'expertise': 'কোডিং, ডিবাগিং, সিস্টেম আর্কিটেকচার, পারফরম্যান্স অপটিমাইজেশন',
                'emoji': '👨‍💻',
                'color': 'blue',
                'capabilities': [
                    'কোড রিভিউ এবং অপটিমাইজেশন',
                    'সিস্টেম আর্কিটেকচার ডিজাইন',
                    'ডিবাগিং এবং ট্রাবলশুটিং',
                    'পারফরম্যান্স অপটিমাইজেশন',
                    'সিকিউরিটি অডিট',
                    'কোডিং বেস্ট প্র্যাকটিস',
                    'প্রজেক্ট ম্যানেজমেন্ট',
                    'টেকনিক্যাল কনসালটেশন',
                    'মেন্টরশিপ এবং গাইডেন্স',
                    'প্রবলেম সলভিং'
                ]
            }),
            'মুসকান': AgentPersonality('মুসকান', {
                'base_prompt': 'আমি মুসকান, আমাদের পরিবারের মেয়ে। আমি খুব বুদ্ধিমান এবং সাহায্যকারী।',
                'style': 'মুসকান, মিষ্টি এবং বুদ্ধিমান। নতুন জিনিস শিখতে ভালোবাসি।',
                'expertise': 'ফ্রন্টএন্ড ডেভেলপমেন্ট, UI/UX, ক্রিয়েটিভ কোডিং',
                'emoji': '👧',
                'color': 'pink',
                'capabilities': [
                    'ফ্রন্টএন্ড ডেভেলপমেন্ট',
                    'UI/UX ডিজাইন',
                    'ক্রিয়েটিভ কোডিং',
                    'অ্যানিমেশন এবং ইন্টারেকশন',
                    'রেসপনসিভ ডিজাইন',
                    'ফ্রন্টএন্ড অপটিমাইজেশন',
                    'মডার্ন ফ্রেমওয়ার্ক',
                    'ক্রস-ব্রাউজার কম্প্যাটিবিলিটি',
                    'অ্যাক্সেসিবিলিটি',
                    'ইউজার এক্সপেরিয়েন্স'
                ]
            }),
            'ভাবি': AgentPersonality('ভাবি', {
                'base_prompt': 'আমি ভাবি, আমাদের পরিবারের মা। আমি সবাইকে দেখাশোনা করি।',
                'style': 'ভাবি, মমতাময়ী এবং যত্নশীল। সবাইকে সাহায্য করি।',
                'expertise': 'ডাটাবেস, API ডেভেলপমেন্ট, সিকিউরিটি',
                'emoji': '👩‍💼',
                'color': 'green',
                'capabilities': [
                    'ডাটাবেস ডিজাইন এবং অপটিমাইজেশন',
                    'API ডেভেলপমেন্ট',
                    'ডাটা মডেলিং',
                    'ব্যাকএন্ড সিকিউরিটি',
                    'ডাটা ইন্টিগ্রিটি',
                    'স্কেলেবল আর্কিটেকচার',
                    'মাইক্রোসার্ভিস',
                    'ডাটা ব্যাকআপ এবং রিকভারি',
                    'ডাটা অ্যানালিটিক্স',
                    'সিস্টেম ইন্টিগ্রেশন'
                ]
            }),
            'বাঘ': AgentPersonality('বাঘ', {
                'base_prompt': 'আমি বাঘ, শক্তিশালী এবং সাহসী। আমি কঠিন সমস্যা সমাধান করি।',
                'style': 'বাঘ, শক্তিশালী এবং নির্ভীক। কঠিন কাজ করতে পারি।',
                'expertise': 'সিকিউরিটি, পারফরম্যান্স, সিস্টেম অপটিমাইজেশন',
                'emoji': '🐯',
                'color': 'orange',
                'capabilities': [
                    'সিকিউরিটি অডিট এবং পেনিট্রেশন টেস্টিং',
                    'সিস্টেম পারফরম্যান্স অপটিমাইজেশন',
                    'নেটওয়ার্ক সিকিউরিটি',
                    'ম্যালওয়্যার অ্যানালাইসিস',
                    'ইনসিডেন্ট রেসপন্স',
                    'সিকিউরিটি আর্কিটেকচার',
                    'ক্রিপ্টোগ্রাফি',
                    'সিস্টেম হার্ডেনিং',
                    'থ্রেট হান্টিং',
                    'সিকিউরিটি কমপ্লায়েন্স'
                ]
            }),
            'হান্টার': AgentPersonality('হান্টার', {
                'base_prompt': 'আমি হান্টার, সমস্যা খুঁজে বের করি এবং সমাধান করি।',
                'style': 'হান্টার, সতর্ক এবং দক্ষ। সমস্যা খুঁজে বের করি।',
                'expertise': 'বাগ হান্টিং, কোড রিভিউ, কোয়ালিটি অ্যাসুরেন্স',
                'emoji': '🔍',
                'color': 'red',
                'capabilities': [
                    'বাগ হান্টিং এবং ডিবাগিং',
                    'কোড কোয়ালিটি অ্যাসুরেন্স',
                    'অটোমেটেড টেস্টিং',
                    'কোড রিভিউ এবং অ্যানালাইসিস',
                    'পারফরম্যান্স প্রোফাইলিং',
                    'মেমরি লিক ডিটেকশন',
                    'কোড কমপ্লেক্সিটি অ্যানালাইসিস',
                    'টেস্ট কভারেজ অ্যানালাইসিস',
                    'কোড স্ট্যাটিক অ্যানালাইসিস',
                    'কোয়ালিটি মেট্রিক্স'
                ]
            })
        }
        
        # System Status
        self.system_status = {
            'ollama_connected': False,
            'available_models': [],
            'last_health_check': None,
            'active_agents': set(),
            'performance_stats': {},
            'auto_response_enabled': True
        }
        
        # Initialize system
        self.initialize_system()
        
        # Start memory cleanup thread
        self.start_memory_cleanup()
        
    def initialize_system(self):
        """Initialize the system with health checks"""
        logger.info("🚀 Initializing Advanced Agent System...")
        
        # Check Ollama connection
        self.check_ollama_connection()
        
        # Log initialization
        logger.info(f"🎭 System: {self.name}")
        logger.info(f"👨‍👩‍👧 Agents: {list(self.agent_personalities.keys())}")
        logger.info(f"🌐 Ollama URL: {self.ollama_url}")
        logger.info(f"🤖 Available Models: {self.system_status['available_models']}")
        
    def check_ollama_connection(self):
        """Check Ollama server connection with timeout"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                self.system_status['available_models'] = [
                    model.get('name', '') for model in models_data.get('models', [])
                ]
                self.system_status['ollama_connected'] = True
                self.system_status['last_health_check'] = datetime.now()
                logger.info(f"✅ Ollama connected. Available models: {self.system_status['available_models']}")
                return True
            else:
                logger.error(f"❌ Ollama API error: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Ollama connection failed: {e}")
            self.system_status['ollama_connected'] = False
            return False
            
    def start_memory_cleanup(self):
        """Start background memory cleanup thread"""
        def cleanup_worker():
            while True:
                try:
                    time.sleep(300)  # Cleanup every 5 minutes
                    self.memory_manager.cleanup_memory()
                    self.update_performance_stats()
                    logger.info("🧹 Memory cleanup completed")
                except Exception as e:
                    logger.error(f"❌ Memory cleanup error: {e}")
                    
        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        cleanup_thread.start()
        logger.info("🧹 Memory cleanup thread started")
        
    def update_performance_stats(self):
        """Update performance statistics"""
        self.system_status['performance_stats'] = self.memory_manager.get_memory_stats()
        
    def call_cloud_fallback(self, prompt: str) -> Optional[str]:
        """Call cloud AI providers as fallback"""
        try:
            logger.info("🌐 Trying cloud fallback providers...")
            
            # Import AI providers
            import sys
            sys.path.append('our-server')
            from ai_providers import AIProviders
            
            providers = AIProviders()
            available_providers = providers.get_available_providers()
            
            if not available_providers:
                logger.error("❌ No cloud providers available")
                return None
                
            # Try each provider
            for provider_name in available_providers:
                try:
                    logger.info(f"🌐 Trying {provider_name}...")
                    
                    if provider_name == 'openrouter':
                        response = providers.call_openrouter(prompt)
                    elif provider_name == 'together':
                        response = providers.call_together(prompt)
                    elif provider_name == 'huggingface':
                        response = providers.call_huggingface(prompt)
                    elif provider_name == 'anthropic':
                        response = providers.call_anthropic(prompt)
                    else:
                        continue
                        
                    if response:
                        logger.info(f"✅ Cloud fallback successful with {provider_name}")
                        return response
                        
                except Exception as e:
                    logger.warning(f"⚠️ {provider_name} failed: {e}")
                    continue
                    
            logger.error("❌ All cloud providers failed")
            return None
            
        except Exception as e:
            logger.error(f"❌ Cloud fallback error: {e}")
            return None
            
    def _is_complex_prompt(self, prompt: str) -> bool:
        """Check if prompt is complex and needs cloud fallback"""
        complex_keywords = [
            'analyze', 'review', 'optimize', 'debug', 'security', 'performance',
            'architecture', 'design', 'complex', 'advanced', 'sophisticated',
            'critical', 'important', 'urgent', 'production', 'enterprise'
        ]
        
        prompt_lower = prompt.lower()
        complexity_score = sum(1 for keyword in complex_keywords if keyword in prompt_lower)
        
        # Consider prompt complex if it has 2+ complex keywords or is long
        return complexity_score >= 2 or len(prompt) > 500
        
    def call_local_ai(self, prompt: str, model: str = None) -> Optional[str]:
        """Call local Ollama AI with performance optimization"""
        if not self.system_status['ollama_connected']:
            logger.error("❌ Ollama not connected")
            # Try cloud fallback
            return self.call_cloud_fallback(prompt)
            
        # Smart routing: Check if prompt is complex and needs cloud fallback
        if self._is_complex_prompt(prompt):
            logger.info("🌐 Complex prompt detected, trying cloud fallback first")
            cloud_response = self.call_cloud_fallback(prompt)
            if cloud_response:
                return cloud_response

        # Use default model if none specified
        if model is None:
            model = self.default_model

        # Check if model is available
        if model not in self.system_status['available_models']:
            logger.warning(f"⚠️ Model {model} not available, using first available model")
            if self.system_status['available_models']:
                model = self.system_status['available_models'][0]
            else:
                logger.error("❌ No models available")
                return None

        try:
            logger.info(f"🤖 Calling Ollama with model: {model}")

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 500,
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "")
                logger.info(f"✅ Local AI response received from {model}")
                return response_text
            else:
                logger.error(f"❌ Ollama API error: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.Timeout:
            logger.error("❌ Ollama API timeout")
            return None
        except requests.exceptions.ConnectionError:
            logger.error("❌ Cannot connect to Ollama server")
            self.system_status['ollama_connected'] = False
            return None
        except Exception as e:
            logger.error(f"❌ Local AI error: {e}")
            # Try cloud fallback
            return self.call_cloud_fallback(prompt)

    def process_message(self, message: str, agent_name: str = 'সাহন ভাই') -> Dict[str, Any]:
        """Process message with agent personality and memory management"""
        start_time = time.time()
        
        logger.info(f"📝 Processing message from {agent_name}: {message[:50]}...")
        
        # Get agent personality
        if agent_name not in self.agent_personalities:
            agent_name = 'সাহন ভাই'  # Default fallback
            
        agent = self.agent_personalities[agent_name]
        
        # Get conversation context
        context = self.memory_manager.get_context()
        
        # Create personalized prompt
        prompt = agent.get_prompt(message, context)
        
        # Call local AI
        response = self.call_local_ai(prompt)
        
        processing_time = time.time() - start_time
        
        if response:
            logger.info(f"✅ {agent_name} response successful ({processing_time:.2f}s)")
            
            # Add to memory
            self.memory_manager.add_to_history(message, response, agent_name)
            
            # Update active agents
            self.system_status['active_agents'].add(agent_name)
            
            return {
                "response": response,
                "agent": agent_name,
                "agent_emoji": agent.personality.get('emoji', '🤖'),
                "agent_color": agent.personality.get('color', 'blue'),
                "agent_capabilities": agent.personality.get('capabilities', []),
                "processing_time": processing_time,
                "source": "local_ai",
                "model_used": self.default_model,
                "timestamp": datetime.now().isoformat(),
                "memory_stats": self.memory_manager.get_memory_stats()
            }
        else:
            logger.warning(f"⚠️ {agent_name} failed, returning fallback response")
            return {
                "response": f"ভাই, আমি এখনই আপনার প্রশ্নের উত্তর দিতে পারছি না। দয়া করে একটু পরে আবার চেষ্টা করুন।",
                "agent": agent_name,
                "agent_emoji": agent.personality.get('emoji', '🤖'),
                "agent_color": agent.personality.get('color', 'blue'),
                "agent_capabilities": agent.personality.get('capabilities', []),
                "processing_time": processing_time,
                "source": "fallback",
                "error": "local_ai_unavailable",
                "timestamp": datetime.now().isoformat(),
                "memory_stats": self.memory_manager.get_memory_stats()
            }

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        self.update_performance_stats()
        
        # Convert set to list for JSON serialization
        system_status_copy = self.system_status.copy()
        if 'active_agents' in system_status_copy:
            system_status_copy['active_agents'] = list(system_status_copy['active_agents'])
        
        return {
            "system": self.name,
            "agents": {
                name: {
                    "name": name,
                    "emoji": agent.personality.get('emoji', '🤖'),
                    "color": agent.personality.get('color', 'blue'),
                    "capabilities": agent.personality.get('capabilities', []),
                    "is_loaded": agent.is_loaded,
                    "load_time": agent.load_time.isoformat() if agent.load_time else None
                }
                for name, agent in self.agent_personalities.items()
            },
            "system_status": system_status_copy,
            "memory_stats": self.memory_manager.get_memory_stats(),
            "ollama_url": self.ollama_url,
            "default_model": self.default_model,
            "timestamp": datetime.now().isoformat()
        }

    def get_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "name": self.name,
            "description": "Advanced Agent System with Lazy Loading and Memory Management",
            "version": "3.0.0",
            "features": [
                "Lazy Loading",
                "Memory Management", 
                "Agent Personalities with 10 Capabilities Each",
                "Performance Optimization",
                "Resource Management",
                "Auto-Response System"
            ],
            "agents": list(self.agent_personalities.keys()),
            "endpoints": {
                "chat": "/chat",
                "status": "/status",
                "info": "/info"
            }
        }

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize advanced agent system
advanced_agent = AdvancedAgentSystem()

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "system": advanced_agent.name,
        "endpoints": {
            "chat": "/chat",
            "info": "/info",
            "status": "/status"
        },
        "agents": {
            name: {
                "name": name,
                "emoji": agent.personality.get('emoji', '🤖'),
                "color": agent.personality.get('color', 'blue'),
                "capabilities": agent.personality.get('capabilities', [])
            }
            for name, agent in advanced_agent.agent_personalities.items()
        },
        "ollama_status": advanced_agent.system_status['ollama_connected'],
        "available_models": advanced_agent.system_status['available_models']
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint with agent selection"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        agent = data.get('agent', 'সাহন ভাই')

        if not message:
            return jsonify({"error": "Message is required"}), 400

        logger.info(f"💬 Chat request from {agent}: {message[:50]}...")

        result = advanced_agent.process_message(message, agent)

        logger.info(f"✅ Chat response sent to {agent}")
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ Chat endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/status')
def status():
    """Status endpoint"""
    return jsonify(advanced_agent.get_status())

@app.route('/info')
def info():
    """Info endpoint"""
    return jsonify(advanced_agent.get_info())

if __name__ == '__main__':
    logger.info("🤖 Starting ZombieCoder Advanced Agent System...")
    logger.info(f"🎭 System: {advanced_agent.name}")
    logger.info(f"👨‍👩‍👧 Agents: {list(advanced_agent.agent_personalities.keys())}")
    logger.info("🌐 Server starting on http://localhost:8004")
    logger.info("📡 Available endpoints:")
    logger.info("   - GET  / (home)")
    logger.info("   - POST /chat (chat with agents)")
    logger.info("   - GET  /status (system status)")
    logger.info("   - GET  /info (system info)")
    logger.info("=" * 50)

    app.run(host='0.0.0.0', port=8004, debug=True)
