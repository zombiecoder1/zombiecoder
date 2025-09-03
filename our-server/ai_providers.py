#!/usr/bin/env python3
"""
🤖 ZombieCoder Agent Personal - AI Providers
"যেখানে কোড ও কথা বলে"

Cloud AI providers for fallback when local models are unavailable or insufficient.
Supports OpenRouter, Together AI, HuggingFace, and OpenAI.
"""

import os
import json
import logging
import requests
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class AIProviders:
    """Cloud AI providers for fallback support"""
    
    def __init__(self):
        # API Keys from environment variables (REMOVED FOR SECURITY)
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
        self.huggingface_key = os.getenv("HUGGINGFACE_API_KEY", "")
        self.together_key = os.getenv("TOGETHER_API_KEY", "")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        # Provider configurations
        self.providers = {
            'openrouter': {
                'name': 'OpenRouter',
                'url': 'https://openrouter.ai/api/v1/chat/completions',
                'models': ['anthropic/claude-3.5-sonnet', 'meta-llama/llama-3.1-8b-instruct', 'openai/gpt-4o-mini'],
                'enabled': bool(self.openrouter_key),
                'timeout': 30
            },
            'together': {
                'name': 'Together AI',
                'url': 'https://api.together.xyz/v1/chat/completions',
                'models': ['togethercomputer/llama-3.1-8b-instruct', 'microsoft/DialoGPT-medium'],
                'enabled': bool(self.together_key),
                'timeout': 30
            },
            'huggingface': {
                'name': 'HuggingFace',
                'url': 'https://api-inference.huggingface.co/models/',
                'models': ['microsoft/DialoGPT-medium', 'gpt2', 'gpt2-medium'],
                'enabled': bool(self.huggingface_key),
                'timeout': 45
            },
            'openai': {
                'name': 'OpenAI',
                'url': 'https://api.openai.com/v1/chat/completions',
                'models': ['gpt-4o-mini', 'gpt-3.5-turbo'],
                'enabled': bool(self.openai_key),
                'timeout': 30
            },
            'anthropic': {
                'name': 'Anthropic',
                'url': 'https://api.anthropic.com/v1/messages',
                'models': ['claude-3-5-sonnet-20241022', 'claude-3-haiku-20240307'],
                'enabled': bool(self.anthropic_key),
                'timeout': 30
            }
        }
        
        # Performance tracking
        self.response_times = {}
        self.success_rates = {}
        self.last_used = {}
        
        logger.info("🌐 AI Providers initialized")
        self._log_provider_status()
    
    def _log_provider_status(self):
        """Log provider availability"""
        enabled_count = sum(1 for p in self.providers.values() if p['enabled'])
        logger.info(f"✅ {enabled_count}/{len(self.providers)} providers enabled")
        
        for name, config in self.providers.items():
            status = "✅" if config['enabled'] else "❌"
            logger.info(f"  {status} {config['name']}: {config['enabled']}")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return [name for name, config in self.providers.items() if config['enabled']]
    
    def get_best_provider(self) -> Optional[str]:
        """Get the best performing provider based on response times and success rates"""
        available = self.get_available_providers()
        if not available:
            return None
        
        # Simple scoring based on response time and success rate
        scores = {}
        for provider in available:
            response_time = self.response_times.get(provider, 30)
            success_rate = self.success_rates.get(provider, 0.5)
            
            # Lower response time and higher success rate = better score
            score = (1 / response_time) * success_rate
            scores[provider] = score
        
        # Return provider with highest score
        return max(scores.items(), key=lambda x: x[1])[0] if scores else available[0]
    
    def call_openrouter(self, message: str, model: str = "anthropic/claude-3.5-sonnet") -> Optional[str]:
        """Call OpenRouter API"""
        if not self.openrouter_key:
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.openrouter_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': model,
                'messages': [{'role': 'user', 'content': message}],
                'max_tokens': 1000,
                'temperature': 0.7
            }
            
            start_time = time.time()
            response = requests.post(
                self.providers['openrouter']['url'],
                headers=headers,
                json=data,
                timeout=self.providers['openrouter']['timeout']
            )
            
            response_time = time.time() - start_time
            self.response_times['openrouter'] = response_time
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                self.success_rates['openrouter'] = 1.0
                self.last_used['openrouter'] = datetime.now()
                return content
            else:
                logger.error(f"OpenRouter error: {response.status_code} - {response.text}")
                self.success_rates['openrouter'] = 0.0
                return None
                
        except Exception as e:
            logger.error(f"OpenRouter exception: {e}")
            self.success_rates['openrouter'] = 0.0
            return None
    
    def call_together(self, message: str, model: str = "meta-llama/Llama-3.1-8B-Instruct") -> Optional[str]:
        """Call Together AI API"""
        if not self.together_key:
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.together_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': model,
                'messages': [{'role': 'user', 'content': message}],
                'max_tokens': 1000,
                'temperature': 0.7
            }
            
            start_time = time.time()
            response = requests.post(
                self.providers['together']['url'],
                headers=headers,
                json=data,
                timeout=self.providers['together']['timeout']
            )
            
            response_time = time.time() - start_time
            self.response_times['together'] = response_time
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                self.success_rates['together'] = 1.0
                self.last_used['together'] = datetime.now()
                return content
            else:
                logger.error(f"Together AI error: {response.status_code} - {response.text}")
                self.success_rates['together'] = 0.0
                return None
                
        except Exception as e:
            logger.error(f"Together AI exception: {e}")
            self.success_rates['together'] = 0.0
            return None
    
    def call_huggingface(self, message: str, model: str = "microsoft/DialoGPT-medium") -> Optional[str]:
        """Call HuggingFace API"""
        if not self.huggingface_key:
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.huggingface_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'inputs': message,
                'parameters': {
                    'max_length': 1000,
                    'temperature': 0.7
                }
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.providers['huggingface']['url']}{model}",
                headers=headers,
                json=data,
                timeout=self.providers['huggingface']['timeout']
            )
            
            response_time = time.time() - start_time
            self.response_times['huggingface'] = response_time
            
            if response.status_code == 200:
                result = response.json()
                # HuggingFace response format varies by model
                if isinstance(result, list) and len(result) > 0:
                    content = result[0].get('generated_text', '')
                else:
                    content = str(result)
                
                self.success_rates['huggingface'] = 1.0
                self.last_used['huggingface'] = datetime.now()
                return content
            else:
                logger.error(f"HuggingFace error: {response.status_code} - {response.text}")
                self.success_rates['huggingface'] = 0.0
                return None
                
        except Exception as e:
            logger.error(f"HuggingFace exception: {e}")
            self.success_rates['huggingface'] = 0.0
            return None
    
    def call_openai(self, message: str, model: str = "gpt-4o-mini") -> Optional[str]:
        """Call OpenAI API"""
        if not self.openai_key:
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': model,
                'messages': [{'role': 'user', 'content': message}],
                'max_tokens': 1000,
                'temperature': 0.7
            }
            
            start_time = time.time()
            response = requests.post(
                self.providers['openai']['url'],
                headers=headers,
                json=data,
                timeout=self.providers['openai']['timeout']
            )
            
            response_time = time.time() - start_time
            self.response_times['openai'] = response_time
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                self.success_rates['openai'] = 1.0
                self.last_used['openai'] = datetime.now()
                return content
            else:
                logger.error(f"OpenAI error: {response.status_code} - {response.text}")
                self.success_rates['openai'] = 0.0
                return None
                
        except Exception as e:
            logger.error(f"OpenAI exception: {e}")
            self.success_rates['openai'] = 0.0
            return None
    
    def call_anthropic(self, message: str, model: str = "claude-3-5-sonnet-20241022") -> Optional[str]:
        """Call Anthropic API"""
        if not self.anthropic_key:
            return None
        
        try:
            headers = {
                'x-api-key': self.anthropic_key,
                'anthropic-version': '2023-06-01',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': model,
                'max_tokens': 1000,
                'messages': [{'role': 'user', 'content': message}]
            }
            
            start_time = time.time()
            response = requests.post(
                self.providers['anthropic']['url'],
                headers=headers,
                json=data,
                timeout=self.providers['anthropic']['timeout']
            )
            
            response_time = time.time() - start_time
            self.response_times['anthropic'] = response_time
            
            if response.status_code == 200:
                result = response.json()
                content = result['content'][0]['text']
                self.success_rates['anthropic'] = 1.0
                self.last_used['anthropic'] = datetime.now()
                return content
            else:
                logger.error(f"Anthropic error: {response.status_code} - {response.text}")
                self.success_rates['anthropic'] = 0.0
                return None
                
        except Exception as e:
            logger.error(f"Anthropic exception: {e}")
            self.success_rates['anthropic'] = 0.0
            return None
    
    def get_fallback_response(self, message: str) -> Optional[str]:
        """Get response from best available provider"""
        provider = self.get_best_provider()
        if not provider:
            logger.warning("❌ No cloud providers available")
            return None
        
        logger.info(f"🌐 Using {self.providers[provider]['name']} for fallback")
        
        # Try the best provider first
        if provider == 'openrouter':
            return self.call_openrouter(message)
        elif provider == 'together':
            return self.call_together(message)
        elif provider == 'huggingface':
            return self.call_huggingface(message)
        elif provider == 'openai':
            return self.call_openai(message)
        elif provider == 'anthropic':
            return self.call_anthropic(message)
        
        # If best provider fails, try others
        for alt_provider in self.get_available_providers():
            if alt_provider == provider:
                continue
            
            logger.info(f"🔄 Trying {self.providers[alt_provider]['name']} as backup")
            
            if alt_provider == 'openrouter':
                result = self.call_openrouter(message)
            elif alt_provider == 'together':
                result = self.call_together(message)
            elif alt_provider == 'huggingface':
                result = self.call_huggingface(message)
            elif alt_provider == 'openai':
                result = self.call_openai(message)
            elif alt_provider == 'anthropic':
                result = self.call_anthropic(message)
            else:
                continue
            
            if result:
                return result
        
        logger.error("❌ All cloud providers failed")
        return None
    
    def fallback_chain(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fallback chain for AI providers"""
        if context is None:
            context = {}
        
        # Try to get response from best provider
        response = self.get_fallback_response(message)
        
        if response:
            return {
                "response": response,
                "provider": self.get_best_provider(),
                "source": "cloud_fallback",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "response": "Sorry, I'm unable to process your request at the moment. Please try again later.",
                "provider": None,
                "source": "fallback",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get provider status"""
        return {
            'providers': {
                name: {
                    'enabled': config['enabled'],
                    'name': config['name'],
                    'response_time': self.response_times.get(name, 0),
                    'success_rate': self.success_rates.get(name, 0),
                    'last_used': self.last_used.get(name, None)
                }
                for name, config in self.providers.items()
            },
            'available_count': len(self.get_available_providers()),
            'best_provider': self.get_best_provider()
        }

# Global instance
ai_providers = AIProviders()
