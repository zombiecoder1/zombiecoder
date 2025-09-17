#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦙 Ollama Configuration for ZombieCoder
Complete Ollama model configuration and management
"""

import os
import json
import requests
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class OllamaConfig:
    """Ollama configuration and management"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.available_models = []
        self.recommended_models = {
            "programming": ["deepseek-coder:latest", "codellama:latest", "codegemma:latest"],
            "general": ["llama3.1:latest", "mistral:latest", "gemma:latest"],
            "small": ["phi3:latest", "tinyllama:latest"],
            "large": ["llama3.1:70b", "codellama:70b"]
        }
        
        # Model configurations
        self.model_configs = {
            "deepseek-coder:latest": {
                "name": "DeepSeek Coder",
                "type": "programming",
                "size": "~4GB",
                "capabilities": ["code_generation", "code_review", "debugging"],
                "languages": ["python", "javascript", "java", "cpp", "go", "rust"]
            },
            "codellama:latest": {
                "name": "Code Llama",
                "type": "programming", 
                "size": "~4GB",
                "capabilities": ["code_generation", "code_review", "documentation"],
                "languages": ["python", "javascript", "java", "cpp", "go", "rust", "php"]
            },
            "llama3.1:latest": {
                "name": "Llama 3.1",
                "type": "general",
                "size": "~4GB",
                "capabilities": ["general_chat", "reasoning", "analysis"],
                "languages": ["general"]
            },
            "mistral:latest": {
                "name": "Mistral",
                "type": "general",
                "size": "~4GB",
                "capabilities": ["general_chat", "reasoning", "writing"],
                "languages": ["general"]
            }
        }
    
    def check_ollama_status(self) -> Dict[str, Any]:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "running",
                    "models": data.get("models", []),
                    "model_count": len(data.get("models", [])),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
        except requests.exceptions.ConnectionError:
            return {
                "status": "not_running",
                "error": "Cannot connect to Ollama server",
                "recommendation": "Start Ollama with: ollama serve",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models"""
        status = self.check_ollama_status()
        if status["status"] != "running":
            return []
        
        models = []
        for model in status["models"]:
            model_info = {
                "name": model.get("name", "unknown"),
                "size": model.get("size", 0),
                "modified_at": model.get("modified_at", ""),
                "config": self.model_configs.get(model.get("name", ""), {})
            }
            models.append(model_info)
        
        return models
    
    def pull_model(self, model_name: str) -> Dict[str, Any]:
        """Pull/download a model"""
        try:
            logger.info(f"Pulling model: {model_name}")
            
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=300
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "model": model_name,
                    "message": f"Model {model_name} pulled successfully",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "model": model_name,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return {
                "status": "error",
                "model": model_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_response(self, model: str, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate response using specified model"""
        try:
            if context is None:
                context = {}
            
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": context.get("temperature", 0.7),
                    "top_p": context.get("top_p", 0.9),
                    "max_tokens": context.get("max_tokens", 1000)
                }
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "response": result.get("response", ""),
                    "model": model,
                    "response_time": response_time,
                    "context": context,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "model": model,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "response_time": response_time,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error generating response with {model}: {e}")
            return {
                "status": "error",
                "model": model,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def setup_recommended_models(self) -> Dict[str, Any]:
        """Setup recommended models for different use cases"""
        results = {
            "programming_models": [],
            "general_models": [],
            "errors": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Check which models are already available
        available_models = [model["name"] for model in self.get_available_models()]
        
        # Setup programming models
        for model in self.recommended_models["programming"]:
            if model not in available_models:
                logger.info(f"Pulling programming model: {model}")
                result = self.pull_model(model)
                if result["status"] == "success":
                    results["programming_models"].append(model)
                else:
                    results["errors"].append(f"Failed to pull {model}: {result['error']}")
            else:
                results["programming_models"].append(model)
        
        # Setup general models
        for model in self.recommended_models["general"]:
            if model not in available_models:
                logger.info(f"Pulling general model: {model}")
                result = self.pull_model(model)
                if result["status"] == "success":
                    results["general_models"].append(model)
                else:
                    results["errors"].append(f"Failed to pull {model}: {result['error']}")
            else:
                results["general_models"].append(model)
        
        return results
    
    def get_best_model_for_task(self, task_type: str, language: str = "python") -> Optional[str]:
        """Get the best model for a specific task"""
        available_models = [model["name"] for model in self.get_available_models()]
        
        if task_type == "programming" or task_type in ["code_generation", "code_review", "debugging"]:
            # Prefer programming-specific models
            for model in self.recommended_models["programming"]:
                if model in available_models:
                    return model
        
        elif task_type == "general" or task_type in ["chat", "reasoning", "analysis"]:
            # Prefer general models
            for model in self.recommended_models["general"]:
                if model in available_models:
                    return model
        
        # Fallback to any available model
        if available_models:
            return available_models[0]
        
        return None
    
    def create_ollama_config(self) -> Dict[str, Any]:
        """Create comprehensive Ollama configuration"""
        config = {
            "ollama_base_url": self.base_url,
            "available_models": self.get_available_models(),
            "recommended_models": self.recommended_models,
            "model_configs": self.model_configs,
            "status": self.check_ollama_status(),
            "setup_complete": False,
            "timestamp": datetime.now().isoformat()
        }
        
        # Check if setup is complete
        available_models = [model["name"] for model in config["available_models"]]
        programming_models = [model for model in self.recommended_models["programming"] if model in available_models]
        general_models = [model for model in self.recommended_models["general"] if model in available_models]
        
        config["setup_complete"] = len(programming_models) >= 1 and len(general_models) >= 1
        
        return config
    
    def test_model_performance(self, model: str, test_prompts: List[str] = None) -> Dict[str, Any]:
        """Test model performance with sample prompts"""
        if test_prompts is None:
            test_prompts = [
                "Hello, how are you?",
                "Write a Python function to calculate factorial",
                "Explain machine learning in simple terms"
            ]
        
        results = {
            "model": model,
            "tests": [],
            "average_response_time": 0,
            "success_rate": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        response_times = []
        successful_tests = 0
        
        for i, prompt in enumerate(test_prompts):
            test_result = self.generate_response(model, prompt)
            results["tests"].append({
                "test_number": i + 1,
                "prompt": prompt,
                "result": test_result
            })
            
            if test_result["status"] == "success":
                successful_tests += 1
                response_times.append(test_result["response_time"])
        
        if response_times:
            results["average_response_time"] = sum(response_times) / len(response_times)
        
        results["success_rate"] = successful_tests / len(test_prompts)
        
        return results

# Global instance
ollama_config = OllamaConfig()

def setup_ollama_for_zombiecoder():
    """Setup Ollama specifically for ZombieCoder"""
    logger.info("🦙 Setting up Ollama for ZombieCoder...")
    
    # Check status
    status = ollama_config.check_ollama_status()
    logger.info(f"Ollama status: {status['status']}")
    
    if status["status"] != "running":
        logger.error("❌ Ollama is not running. Please start it with: ollama serve")
        return False
    
    # Setup recommended models
    setup_results = ollama_config.setup_recommended_models()
    
    logger.info(f"✅ Programming models: {setup_results['programming_models']}")
    logger.info(f"✅ General models: {setup_results['general_models']}")
    
    if setup_results["errors"]:
        logger.warning(f"⚠️ Errors: {setup_results['errors']}")
    
    # Save configuration
    config = ollama_config.create_ollama_config()
    with open("ollama_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    logger.info("💾 Ollama configuration saved to ollama_config.json")
    return True

if __name__ == "__main__":
    setup_ollama_for_zombiecoder()
