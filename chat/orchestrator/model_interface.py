"""
Model Interface
Editor ভাই-এর জন্য AI Model Integration
"""

import requests
import json
import os
import tempfile
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import logging
from pathlib import Path

from config import config

class ModelInterface:
    """Interface for different AI models (LLM, TTS, etc.)"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.audio_output_dir = Path(config.audio_output_dir)
        self.audio_output_dir.mkdir(exist_ok=True)
        
    def query_model(self, refined_prompt: Dict) -> Dict:
        """
        Query the appropriate model based on routing information
        
        Args:
            refined_prompt: Refined prompt with routing information
            
        Returns:
            Dict containing model response
        """
        try:
            model_route = refined_prompt["model_route"]
            primary_model = model_route["primary_model"]
            
            # Query primary model
            response = self._query_primary_model(primary_model, refined_prompt)
            
            # Query secondary models if needed
            if model_route.get("secondary_models"):
                secondary_responses = self._query_secondary_models(
                    model_route["secondary_models"], refined_prompt
                )
                response["secondary_responses"] = secondary_responses
            
            # Generate TTS if required
            if model_route.get("requires_tts", False):
                audio_path = self._generate_tts(response["content"])
                response["audio_path"] = audio_path
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error querying model: {e}")
            return self._get_error_response(str(e))
    
    def _query_primary_model(self, model_name: str, refined_prompt: Dict) -> Dict:
        """Query the primary model"""
        model_config = config.models.get(model_name)
        if not model_config:
            raise ValueError(f"Model {model_name} not found in configuration")
        
        if model_config.model_type == "llm":
            return self._query_llm(model_config, refined_prompt)
        elif model_config.model_type == "tts":
            return self._query_tts(model_config, refined_prompt)
        else:
            raise ValueError(f"Unsupported model type: {model_config.model_type}")
    
    def _query_llm(self, model_config, refined_prompt: Dict) -> Dict:
        """Query LLM model"""
        if model_config.endpoint == "http://localhost:11434/api/generate":
            return self._query_ollama(model_config, refined_prompt)
        elif "openai.com" in model_config.endpoint:
            return self._query_openai(model_config, refined_prompt)
        else:
            return self._query_generic_llm(model_config, refined_prompt)
    
    def _query_ollama(self, model_config, refined_prompt: Dict) -> Dict:
        """Query Ollama local model"""
        try:
            payload = {
                "model": "llama2",  # Default model, can be configured
                "prompt": refined_prompt["refined_prompt"],
                "stream": False,
                "options": {
                    "temperature": refined_prompt["parameters"]["temperature"],
                    "top_p": refined_prompt["parameters"]["top_p"],
                    "num_predict": refined_prompt["parameters"]["max_tokens"]
                }
            }
            
            response = requests.post(
                model_config.endpoint,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "content": result.get("response", ""),
                    "model_used": "ollama_llama2",
                    "timestamp": datetime.now().isoformat(),
                    "success": True,
                    "metadata": {
                        "total_duration": result.get("total_duration", 0),
                        "load_duration": result.get("load_duration", 0),
                        "prompt_eval_count": result.get("prompt_eval_count", 0)
                    }
                }
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Ollama query error: {e}")
            return self._get_fallback_response(refined_prompt)
    
    def _query_openai(self, model_config, refined_prompt: Dict) -> Dict:
        """Query OpenAI API"""
        try:
            headers = {
                "Authorization": f"Bearer {model_config.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": refined_prompt["refined_prompt"]}
                ],
                "temperature": refined_prompt["parameters"]["temperature"],
                "max_tokens": refined_prompt["parameters"]["max_tokens"],
                "top_p": refined_prompt["parameters"]["top_p"]
            }
            
            response = requests.post(
                model_config.endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "content": result["choices"][0]["message"]["content"],
                    "model_used": "openai_gpt-3.5-turbo",
                    "timestamp": datetime.now().isoformat(),
                    "success": True,
                    "metadata": {
                        "usage": result.get("usage", {}),
                        "finish_reason": result["choices"][0].get("finish_reason", "")
                    }
                }
            else:
                raise Exception(f"OpenAI API error: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"OpenAI query error: {e}")
            return self._get_fallback_response(refined_prompt)
    
    def _query_generic_llm(self, model_config, refined_prompt: Dict) -> Dict:
        """Query generic LLM endpoint"""
        try:
            payload = {
                "prompt": refined_prompt["refined_prompt"],
                "temperature": refined_prompt["parameters"]["temperature"],
                "max_tokens": refined_prompt["parameters"]["max_tokens"]
            }
            
            response = requests.post(
                model_config.endpoint,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "content": result.get("response", result.get("text", "")),
                    "model_used": model_config.name,
                    "timestamp": datetime.now().isoformat(),
                    "success": True,
                    "metadata": result
                }
            else:
                raise Exception(f"Generic LLM API error: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Generic LLM query error: {e}")
            return self._get_fallback_response(refined_prompt)
    
    def _query_secondary_models(self, secondary_models: List[str], refined_prompt: Dict) -> List[Dict]:
        """Query secondary models for verification or enhancement"""
        responses = []
        
        for model_name in secondary_models:
            try:
                model_config = config.models.get(model_name)
                if model_config and model_config.model_type == "llm":
                    response = self._query_llm(model_config, refined_prompt)
                    responses.append({
                        "model": model_name,
                        "response": response
                    })
            except Exception as e:
                self.logger.warning(f"Secondary model {model_name} failed: {e}")
                responses.append({
                    "model": model_name,
                    "error": str(e)
                })
        
        return responses
    
    def _generate_tts(self, text: str) -> str:
        """Generate TTS audio from text"""
        try:
            # Use Coqui TTS for Bengali/English
            from TTS.api import TTS
            
            # Initialize TTS model
            tts = TTS("tts_models/bn/custom/vits")
            
            # Generate audio file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_filename = f"tts_output_{timestamp}.wav"
            audio_path = self.audio_output_dir / audio_filename
            
            # Generate speech
            tts.tts_to_file(text=text, file_path=str(audio_path))
            
            return str(audio_path)
            
        except Exception as e:
            self.logger.error(f"TTS generation error: {e}")
            # Fallback to simple TTS or return None
            return self._fallback_tts(text)
    
    def _fallback_tts(self, text: str) -> Optional[str]:
        """Fallback TTS using system TTS"""
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            
            # Configure voice properties
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'bengali' in voice.name.lower() or 'bn' in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            # Generate audio file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_filename = f"fallback_tts_{timestamp}.wav"
            audio_path = self.audio_output_dir / audio_filename
            
            engine.save_to_file(text, str(audio_path))
            engine.runAndWait()
            
            return str(audio_path)
            
        except Exception as e:
            self.logger.error(f"Fallback TTS error: {e}")
            return None
    
    def _get_fallback_response(self, refined_prompt: Dict) -> Dict:
        """Get fallback response when model query fails"""
        return {
            "content": f"দুঃখিত, আমি এখন আপনার প্রশ্নের উত্তর দিতে পারছি না। অনুগ্রহ করে আবার চেষ্টা করুন।\n\nSorry, I cannot answer your question right now. Please try again.",
            "model_used": "fallback",
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "error": "Model query failed, using fallback response"
        }
    
    def _get_error_response(self, error_message: str) -> Dict:
        """Get error response"""
        return {
            "content": f"একটি ত্রুটি হয়েছে: {error_message}\n\nAn error occurred: {error_message}",
            "model_used": "error",
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "error": error_message
        }
    
    def get_model_status(self) -> Dict:
        """Get status of all configured models"""
        status = {}
        
        for model_name, model_config in config.models.items():
            try:
                if model_config.model_type == "llm":
                    # Test LLM connectivity
                    test_response = requests.get(
                        model_config.endpoint.replace("/api/generate", "/api/tags"),
                        timeout=5
                    )
                    status[model_name] = {
                        "status": "online" if test_response.status_code == 200 else "offline",
                        "type": model_config.model_type,
                        "endpoint": model_config.endpoint
                    }
                else:
                    status[model_name] = {
                        "status": "configured",
                        "type": model_config.model_type,
                        "endpoint": model_config.endpoint
                    }
            except Exception as e:
                status[model_name] = {
                    "status": "error",
                    "type": model_config.model_type,
                    "error": str(e)
                }
        
        return status

# Example usage and testing
if __name__ == "__main__":
    interface = ModelInterface()
    
    # Test model status
    print("=== Model Status ===")
    status = interface.get_model_status()
    for model, info in status.items():
        print(f"{model}: {info['status']}")
    
    print("\n=== Model Interface Test ===")
    print("Model interface is ready for testing with the main orchestration system.")
