"""
Prompt Orchestration System Configuration
Editor ভাই-এর জন্য Smart Prompt Routing System
"""

import os
from typing import Dict, List, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ModelConfig:
    """Model configuration for different AI services"""
    name: str
    endpoint: str
    api_key: str = None
    max_tokens: int = 1000
    temperature: float = 0.7
    model_type: str = "llm"  # llm, tts, stt

@dataclass
class SystemConfig:
    """Main system configuration"""
    # Language settings
    default_language: str = "bengali"
    supported_languages: List[str] = None
    
    # Model settings
    models: Dict[str, ModelConfig] = None
    
    # Output settings
    output_formats: List[str] = None
    audio_output_dir: str = "audio_outputs"
    log_level: str = "INFO"
    
    # System paths
    base_dir: Path = None
    
    def __post_init__(self):
        if self.supported_languages is None:
            self.supported_languages = [
                "bengali", "english", "hindi", "urdu", "arabic"
            ]
        
        if self.models is None:
            self.models = {
                "llm_local": ModelConfig(
                    name="Local LLM",
                    endpoint="http://localhost:11434/api/generate",
                    model_type="llm"
                ),
                "tts_coqui": ModelConfig(
                    name="Coqui TTS",
                    endpoint="local",
                    model_type="tts"
                ),
                "llm_openai": ModelConfig(
                    name="OpenAI GPT",
                    endpoint="https://api.openai.com/v1/chat/completions",
                    api_key=os.getenv("OPENAI_API_KEY"),
                    model_type="llm"
                )
            }
        
        if self.output_formats is None:
            self.output_formats = ["text", "json", "audio", "html"]
        
        if self.base_dir is None:
            self.base_dir = Path(__file__).parent

# Global configuration instance
config = SystemConfig()

# Prompt templates for different use cases
PROMPT_TEMPLATES = {
    "general_question": """
    আপনি একজন সহায়ক AI। নিম্নলিখিত প্রশ্নের উত্তর দিন:
    
    প্রশ্ন: {user_input}
    
    উত্তর দিন বাংলা এবং ইংরেজি উভয় ভাষায়, সহজ এবং বোধগম্য ভাষায়।
    """,
    
    "coding_help": """
    আপনি একজন প্রোগ্রামিং বিশেষজ্ঞ। নিম্নলিখিত কোডিং সমস্যার সমাধান দিন:
    
    সমস্যা: {user_input}
    
    সমাধান দিন:
    1. সমস্যার বিশ্লেষণ
    2. সমাধানের ধাপ
    3. কোড উদাহরণ
    4. ব্যাখ্যা
    """,
    
    "translation": """
    নিম্নলিখিত টেক্সটটি অনুবাদ করুন:
    
    টেক্সট: {user_input}
    
    অনুবাদ দিন বাংলা থেকে ইংরেজি এবং ইংরেজি থেকে বাংলা।
    """,
    
    "weather": """
    আবহাওয়া সম্পর্কিত প্রশ্নের উত্তর দিন:
    
    প্রশ্ন: {user_input}
    
    উত্তর দিন সহজ ভাষায়, বর্তমান আবহাওয়া এবং পরামর্শ সহ।
    """
}

# Language detection patterns
LANGUAGE_PATTERNS = {
    "bengali": [
        "আমি", "আপনি", "কেমন", "কী", "কোথায়", "কখন", "কেন", "কীভাবে",
        "হয়", "আছে", "নেই", "করতে", "হবে", "হয়েছে", "করবে"
    ],
    "english": [
        "the", "is", "are", "was", "were", "have", "has", "had", "will",
        "would", "could", "should", "can", "may", "might", "do", "does", "did"
    ],
    "hindi": [
        "मैं", "आप", "है", "हैं", "था", "थे", "करना", "होना", "जाना", "आना"
    ]
}

# Output format templates
OUTPUT_TEMPLATES = {
    "json": {
        "response": "{content}",
        "language": "{language}",
        "timestamp": "{timestamp}",
        "model_used": "{model}",
        "audio_file": "{audio_path}"
    },
    "html": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Response</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <h2>AI Response</h2>
        <p><strong>Language:</strong> {language}</p>
        <p><strong>Response:</strong> {content}</p>
        <p><strong>Timestamp:</strong> {timestamp}</p>
        {audio_player}
    </body>
    </html>
    """
}
