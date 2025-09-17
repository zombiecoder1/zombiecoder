"""
User Input Handler
Editor ভাই-এর জন্য Smart Input Processing
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from langdetect import detect, DetectorFactory
from textblob import TextBlob
import logging

from config import LANGUAGE_PATTERNS, config

# Set seed for consistent language detection
DetectorFactory.seed = 0

class InputHandler:
    """Handles user input processing, language detection, and normalization"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def process_input(self, user_input: str) -> Dict:
        """
        Main method to process user input
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Dict containing processed input information
        """
        try:
            # Clean and normalize input
            cleaned_input = self._clean_input(user_input)
            
            # Detect language
            detected_language = self._detect_language(cleaned_input)
            
            # Extract intent
            intent = self._extract_intent(cleaned_input, detected_language)
            
            # Determine processing type
            processing_type = self._determine_processing_type(cleaned_input, intent)
            
            return {
                "original_input": user_input,
                "cleaned_input": cleaned_input,
                "detected_language": detected_language,
                "intent": intent,
                "processing_type": processing_type,
                "timestamp": datetime.now().isoformat(),
                "confidence": self._calculate_confidence(cleaned_input, detected_language)
            }
            
        except Exception as e:
            self.logger.error(f"Error processing input: {e}")
            return {
                "original_input": user_input,
                "cleaned_input": user_input,
                "detected_language": "unknown",
                "intent": "general",
                "processing_type": "text",
                "timestamp": datetime.now().isoformat(),
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _clean_input(self, text: str) -> str:
        """Clean and normalize input text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common Bengali typing issues
        bengali_fixes = {
            '্র': '্র', '্র': '্র',  # Fix ra-kar
            '়': '়', '়': '়',  # Fix hasant
        }
        
        for wrong, correct in bengali_fixes.items():
            text = text.replace(wrong, correct)
        
        # Remove special characters but keep Bengali punctuation
        text = re.sub(r'[^\w\s\u0980-\u09FF.,!?;:()]', '', text)
        
        return text
    
    def _detect_language(self, text: str) -> str:
        """Detect language of the input text"""
        try:
            # First try langdetect
            detected = detect(text)
            
            # Map to our supported languages
            language_map = {
                'bn': 'bengali',
                'en': 'english', 
                'hi': 'hindi',
                'ur': 'urdu',
                'ar': 'arabic'
            }
            
            if detected in language_map:
                return language_map[detected]
            
            # Fallback to pattern matching
            return self._pattern_based_detection(text)
            
        except Exception:
            return self._pattern_based_detection(text)
    
    def _pattern_based_detection(self, text: str) -> str:
        """Fallback language detection using patterns"""
        text_lower = text.lower()
        
        scores = {}
        for lang, patterns in LANGUAGE_PATTERNS.items():
            score = sum(1 for pattern in patterns if pattern in text_lower)
            scores[lang] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return "unknown"
    
    def _extract_intent(self, text: str, language: str) -> str:
        """Extract user intent from the text"""
        text_lower = text.lower()
        
        # Intent patterns
        intent_patterns = {
            "coding": [
                "কোড", "প্রোগ্রাম", "ফাংশন", "বাগ", "error", "code", "program", 
                "function", "bug", "debug", "compile", "syntax"
            ],
            "translation": [
                "অনুবাদ", "translate", "translation", "বাংলা", "ইংরেজি", 
                "english", "bengali"
            ],
            "weather": [
                "আবহাওয়া", "বৃষ্টি", "সূর্য", "weather", "rain", "sun", 
                "temperature", "তাপমাত্রা"
            ],
            "question": [
                "কী", "কেমন", "কোথায়", "কখন", "কেন", "কীভাবে", "what", 
                "how", "where", "when", "why", "which"
            ],
            "greeting": [
                "হ্যালো", "হাই", "নমস্কার", "hello", "hi", "good morning", 
                "good evening", "good night"
            ]
        }
        
        for intent, patterns in intent_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                return intent
        
        return "general"
    
    def _determine_processing_type(self, text: str, intent: str) -> str:
        """Determine what type of processing is needed"""
        if intent == "coding":
            return "code_analysis"
        elif intent == "translation":
            return "translation"
        elif intent == "weather":
            return "weather_query"
        elif intent == "greeting":
            return "conversation"
        else:
            return "text"
    
    def _calculate_confidence(self, text: str, language: str) -> float:
        """Calculate confidence score for language detection"""
        if language == "unknown":
            return 0.0
        
        # Count pattern matches
        patterns = LANGUAGE_PATTERNS.get(language, [])
        if not patterns:
            return 0.5
        
        text_lower = text.lower()
        matches = sum(1 for pattern in patterns if pattern in text_lower)
        
        # Calculate confidence based on pattern matches
        confidence = min(matches / len(patterns) * 2, 1.0)
        return round(confidence, 2)
    
    def get_suggestions(self, processed_input: Dict) -> List[str]:
        """Get suggestions based on processed input"""
        suggestions = []
        
        if processed_input["confidence"] < 0.3:
            suggestions.append("Language detection confidence is low. Please try rephrasing.")
        
        if processed_input["intent"] == "general":
            suggestions.extend([
                "Try asking a specific question",
                "Use keywords like 'code', 'translate', or 'weather' for better results"
            ])
        
        if processed_input["detected_language"] == "bengali":
            suggestions.append("I can help you in Bengali and English")
        
        return suggestions

# Example usage and testing
if __name__ == "__main__":
    handler = InputHandler()
    
    test_inputs = [
        "আজকের আবহাওয়া কেমন?",
        "Hello, how are you?",
        "আমার কোডে একটা বাগ আছে",
        "Translate this to English",
        "কীভাবে Python এ function লিখব?"
    ]
    
    print("=== Input Handler Test ===")
    for test_input in test_inputs:
        result = handler.process_input(test_input)
        print(f"\nInput: {test_input}")
        print(f"Language: {result['detected_language']}")
        print(f"Intent: {result['intent']}")
        print(f"Processing Type: {result['processing_type']}")
        print(f"Confidence: {result['confidence']}")
        print("-" * 50)
