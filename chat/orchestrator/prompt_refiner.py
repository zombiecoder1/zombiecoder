"""
Prompt Refiner and Smart Router
Editor ভাই-এর জন্য Intelligent Prompt Processing
"""

import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from config import PROMPT_TEMPLATES, config

class PromptRefiner:
    """Refines and routes prompts based on user intent and context"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.conversation_history = []
        
    def refine_prompt(self, processed_input: Dict) -> Dict:
        """
        Refine the prompt based on user input analysis
        
        Args:
            processed_input: Processed input from InputHandler
            
        Returns:
            Dict containing refined prompt and routing information
        """
        try:
            # Get base template
            template = self._select_template(processed_input)
            
            # Enhance prompt with context
            enhanced_prompt = self._enhance_prompt(template, processed_input)
            
            # Determine model routing
            model_route = self._determine_model_route(processed_input)
            
            # Add conversation context
            context = self._get_conversation_context()
            
            refined_prompt = {
                "original_prompt": processed_input["cleaned_input"],
                "refined_prompt": enhanced_prompt,
                "template_used": template,
                "model_route": model_route,
                "context": context,
                "parameters": self._get_model_parameters(processed_input),
                "timestamp": datetime.now().isoformat(),
                "processing_metadata": {
                    "language": processed_input["detected_language"],
                    "intent": processed_input["intent"],
                    "confidence": processed_input["confidence"]
                }
            }
            
            # Store in conversation history
            self._update_conversation_history(refined_prompt)
            
            return refined_prompt
            
        except Exception as e:
            self.logger.error(f"Error refining prompt: {e}")
            return self._get_fallback_prompt(processed_input)
    
    def _select_template(self, processed_input: Dict) -> str:
        """Select appropriate prompt template based on intent"""
        intent = processed_input["intent"]
        language = processed_input["detected_language"]
        
        # Map intent to template
        template_mapping = {
            "coding": "coding_help",
            "translation": "translation", 
            "weather": "weather",
            "question": "general_question",
            "greeting": "general_question",
            "general": "general_question"
        }
        
        template_key = template_mapping.get(intent, "general_question")
        base_template = PROMPT_TEMPLATES.get(template_key, PROMPT_TEMPLATES["general_question"])
        
        # Customize template based on language
        if language == "bengali":
            return self._customize_for_bengali(base_template)
        elif language == "english":
            return self._customize_for_english(base_template)
        else:
            return base_template
    
    def _customize_for_bengali(self, template: str) -> str:
        """Customize template for Bengali language"""
        return template.replace(
            "আপনি একজন সহায়ক AI।",
            "আপনি একজন সহায়ক AI (সাহন ভাই)। আপনি বাঙালি এবং খুব বন্ধুত্বপূর্ণ।"
        )
    
    def _customize_for_english(self, template: str) -> str:
        """Customize template for English language"""
        return template.replace(
            "আপনি একজন সহায়ক AI।",
            "You are a helpful AI assistant (Sahon Bhai). You are friendly and supportive."
        )
    
    def _enhance_prompt(self, template: str, processed_input: Dict) -> str:
        """Enhance the prompt with additional context and instructions"""
        user_input = processed_input["cleaned_input"]
        language = processed_input["detected_language"]
        intent = processed_input["intent"]
        
        # Format the template with user input
        enhanced_prompt = template.format(user_input=user_input)
        
        # Add language-specific instructions
        if language == "bengali":
            enhanced_prompt += "\n\nবিশেষ নির্দেশনা:\n- উত্তর দিন সহজ এবং বোধগম্য বাংলায়\n- প্রয়োজনে উদাহরণ দিন\n- বন্ধুত্বপূর্ণ এবং সহায়ক ভাবে উত্তর দিন"
        elif language == "english":
            enhanced_prompt += "\n\nSpecial Instructions:\n- Answer in clear and simple English\n- Provide examples when helpful\n- Be friendly and supportive"
        
        # Add intent-specific enhancements
        if intent == "coding":
            enhanced_prompt += "\n\nকোডিং নির্দেশনা:\n- কোডের ব্যাখ্যা দিন\n- সম্ভাব্য সমস্যা এবং সমাধান উল্লেখ করুন\n- Best practices শেয়ার করুন"
        elif intent == "translation":
            enhanced_prompt += "\n\nঅনুবাদ নির্দেশনা:\n- সঠিক এবং প্রাকৃতিক অনুবাদ দিন\n- সাংস্কৃতিক প্রেক্ষাপট বিবেচনা করুন"
        
        return enhanced_prompt
    
    def _determine_model_route(self, processed_input: Dict) -> Dict:
        """Determine which model(s) to use for processing"""
        intent = processed_input["intent"]
        language = processed_input["detected_language"]
        
        # Default routing
        route = {
            "primary_model": "llm_local",
            "secondary_models": [],
            "requires_tts": False,
            "output_format": "text"
        }
        
        # Intent-based routing
        if intent == "coding":
            route["primary_model"] = "llm_local"
            route["output_format"] = "code"
        elif intent == "translation":
            route["primary_model"] = "llm_local"
            route["secondary_models"] = ["llm_openai"]  # For verification
        elif intent == "weather":
            route["primary_model"] = "llm_local"
            route["requires_tts"] = True
        elif intent == "greeting":
            route["requires_tts"] = True
            route["output_format"] = "conversation"
        
        # Language-based adjustments
        if language == "bengali":
            route["requires_tts"] = True  # Bengali TTS is preferred
        
        return route
    
    def _get_model_parameters(self, processed_input: Dict) -> Dict:
        """Get model-specific parameters"""
        intent = processed_input["intent"]
        
        base_params = {
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 0.9
        }
        
        # Adjust parameters based on intent
        if intent == "coding":
            base_params["temperature"] = 0.3  # More deterministic for code
            base_params["max_tokens"] = 2000
        elif intent == "translation":
            base_params["temperature"] = 0.5
        elif intent == "greeting":
            base_params["temperature"] = 0.8  # More creative for conversation
        
        return base_params
    
    def _get_conversation_context(self) -> List[Dict]:
        """Get recent conversation context"""
        # Return last 3 exchanges for context
        return self.conversation_history[-6:] if len(self.conversation_history) > 6 else self.conversation_history
    
    def _update_conversation_history(self, refined_prompt: Dict):
        """Update conversation history"""
        self.conversation_history.append({
            "timestamp": refined_prompt["timestamp"],
            "user_input": refined_prompt["original_prompt"],
            "intent": refined_prompt["processing_metadata"]["intent"],
            "language": refined_prompt["processing_metadata"]["language"]
        })
        
        # Keep only last 10 exchanges
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def _get_fallback_prompt(self, processed_input: Dict) -> Dict:
        """Get fallback prompt when refinement fails"""
        return {
            "original_prompt": processed_input["cleaned_input"],
            "refined_prompt": f"Please help with: {processed_input['cleaned_input']}",
            "template_used": "fallback",
            "model_route": {
                "primary_model": "llm_local",
                "secondary_models": [],
                "requires_tts": False,
                "output_format": "text"
            },
            "context": [],
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 1000,
                "top_p": 0.9
            },
            "timestamp": datetime.now().isoformat(),
            "processing_metadata": {
                "language": processed_input.get("detected_language", "unknown"),
                "intent": processed_input.get("intent", "general"),
                "confidence": 0.0
            },
            "error": "Fallback prompt used due to processing error"
        }
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of conversation history"""
        if not self.conversation_history:
            return {"message": "No conversation history"}
        
        languages = [item["language"] for item in self.conversation_history]
        intents = [item["intent"] for item in self.conversation_history]
        
        return {
            "total_exchanges": len(self.conversation_history),
            "most_common_language": max(set(languages), key=languages.count),
            "most_common_intent": max(set(intents), key=intents.count),
            "recent_topics": [item["intent"] for item in self.conversation_history[-5:]],
            "conversation_start": self.conversation_history[0]["timestamp"] if self.conversation_history else None
        }

# Example usage and testing
if __name__ == "__main__":
    refiner = PromptRefiner()
    
    # Test with sample processed input
    test_input = {
        "original_input": "আজকের আবহাওয়া কেমন?",
        "cleaned_input": "আজকের আবহাওয়া কেমন",
        "detected_language": "bengali",
        "intent": "weather",
        "processing_type": "weather_query",
        "timestamp": datetime.now().isoformat(),
        "confidence": 0.8
    }
    
    result = refiner.refine_prompt(test_input)
    
    print("=== Prompt Refiner Test ===")
    print(f"Original: {result['original_prompt']}")
    print(f"Refined: {result['refined_prompt'][:200]}...")
    print(f"Model Route: {result['model_route']}")
    print(f"Template: {result['template_used']}")
    print("-" * 50)
