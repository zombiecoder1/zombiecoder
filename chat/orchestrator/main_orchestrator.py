"""
Main Orchestration System
Editor ভাই-এর জন্য Complete Prompt Orchestration System
"""

import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path
import asyncio
from dataclasses import asdict

from config import config
from input_handler import InputHandler
from prompt_refiner import PromptRefiner
from model_interface import ModelInterface
from output_formatter import OutputFormatter

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('orchestration.log'),
        logging.StreamHandler()
    ]
)

class PromptOrchestrator:
    """
    Main orchestration system that coordinates all components
    Editor ভাই-এর জন্য Smart Prompt Routing System
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.input_handler = InputHandler()
        self.prompt_refiner = PromptRefiner()
        self.model_interface = ModelInterface()
        self.output_formatter = OutputFormatter()
        
        # System state
        self.session_id = None
        self.conversation_history = []
        self.system_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "start_time": datetime.now().isoformat()
        }
        
        self.logger.info("Prompt Orchestrator initialized successfully")
    
    def process_request(self, user_input: str, output_format: str = "json", session_id: str = None) -> Dict:
        """
        Main method to process user request through the entire pipeline
        
        Args:
            user_input: Raw user input
            output_format: Desired output format (json, html, text, audio, code, conversation)
            session_id: Optional session identifier
            
        Returns:
            Dict containing the complete response
        """
        start_time = datetime.now()
        self.session_id = session_id or f"session_{int(start_time.timestamp())}"
        
        try:
            self.logger.info(f"Processing request for session {self.session_id}")
            self.system_stats["total_requests"] += 1
            
            # Step 1: Process input
            self.logger.debug("Step 1: Processing user input")
            processed_input = self.input_handler.process_input(user_input)
            
            # Step 2: Refine prompt
            self.logger.debug("Step 2: Refining prompt")
            refined_prompt = self.prompt_refiner.refine_prompt(processed_input)
            
            # Step 3: Query model
            self.logger.debug("Step 3: Querying AI model")
            model_response = self.model_interface.query_model(refined_prompt)
            
            # Step 4: Format output
            self.logger.debug("Step 4: Formatting output")
            formatted_response = self.output_formatter.format_response(model_response, output_format)
            
            # Step 5: Create final response
            final_response = self._create_final_response(
                user_input, processed_input, refined_prompt, 
                model_response, formatted_response, start_time
            )
            
            # Update conversation history
            self._update_conversation_history(final_response)
            
            # Update stats
            self.system_stats["successful_requests"] += 1
            
            self.logger.info(f"Request processed successfully in {final_response['processing_time']:.2f}s")
            return final_response
            
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            self.system_stats["failed_requests"] += 1
            
            return self._create_error_response(user_input, str(e), start_time)
    
    def _create_final_response(self, user_input: str, processed_input: Dict, 
                             refined_prompt: Dict, model_response: Dict, 
                             formatted_response: Union[Dict, str], start_time: datetime) -> Dict:
        """Create the final response structure"""
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        return {
            "session_id": self.session_id,
            "timestamp": end_time.isoformat(),
            "processing_time": processing_time,
            "user_input": user_input,
            "processed_input": processed_input,
            "refined_prompt": {
                "template_used": refined_prompt["template_used"],
                "model_route": refined_prompt["model_route"],
                "parameters": refined_prompt["parameters"]
            },
            "model_response": {
                "content": model_response.get("content", ""),
                "model_used": model_response.get("model_used", "unknown"),
                "success": model_response.get("success", False),
                "metadata": model_response.get("metadata", {})
            },
            "formatted_response": formatted_response,
            "system_info": {
                "agent": "ZombieCoder Agent (সাহন ভাই)",
                "version": "1.0.0",
                "language": processed_input.get("detected_language", "unknown"),
                "intent": processed_input.get("intent", "general"),
                "confidence": processed_input.get("confidence", 0.0)
            },
            "success": True
        }
    
    def _create_error_response(self, user_input: str, error_message: str, start_time: datetime) -> Dict:
        """Create error response"""
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        return {
            "session_id": self.session_id,
            "timestamp": end_time.isoformat(),
            "processing_time": processing_time,
            "user_input": user_input,
            "error": {
                "message": error_message,
                "type": "processing_error"
            },
            "formatted_response": {
                "content": "দুঃখিত, একটি ত্রুটি হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।\n\nSorry, an error occurred. Please try again.",
                "error": True
            },
            "system_info": {
                "agent": "ZombieCoder Agent (সাহন ভাই)",
                "version": "1.0.0"
            },
            "success": False
        }
    
    def _update_conversation_history(self, response: Dict):
        """Update conversation history"""
        self.conversation_history.append({
            "timestamp": response["timestamp"],
            "user_input": response["user_input"],
            "response_content": response["formatted_response"].get("content", "") if isinstance(response["formatted_response"], dict) else str(response["formatted_response"]),
            "language": response["system_info"]["language"],
            "intent": response["system_info"]["intent"],
            "processing_time": response["processing_time"]
        })
        
        # Keep only last 20 exchanges
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history[-limit:] if limit else self.conversation_history
    
    def get_system_stats(self) -> Dict:
        """Get system statistics"""
        uptime = datetime.now() - datetime.fromisoformat(self.system_stats["start_time"])
        
        return {
            **self.system_stats,
            "uptime_seconds": uptime.total_seconds(),
            "success_rate": (
                self.system_stats["successful_requests"] / self.system_stats["total_requests"] * 100
                if self.system_stats["total_requests"] > 0 else 0
            ),
            "conversation_exchanges": len(self.conversation_history)
        }
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        return {
            "orchestrator": {
                "status": "running",
                "session_id": self.session_id,
                "uptime": self.get_system_stats()["uptime_seconds"]
            },
            "components": {
                "input_handler": "active",
                "prompt_refiner": "active", 
                "model_interface": "active",
                "output_formatter": "active"
            },
            "models": self.model_interface.get_model_status(),
            "supported_formats": self.output_formatter.get_supported_formats(),
            "conversation_summary": self.prompt_refiner.get_conversation_summary()
        }
    
    def reset_session(self):
        """Reset current session"""
        self.session_id = None
        self.conversation_history = []
        self.prompt_refiner.conversation_history = []
        self.logger.info("Session reset successfully")
    
    def health_check(self) -> Dict:
        """Perform system health check"""
        health_status = {
            "overall": "healthy",
            "components": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Check each component
        try:
            # Test input handler
            test_input = self.input_handler.process_input("test")
            health_status["components"]["input_handler"] = "healthy"
        except Exception as e:
            health_status["components"]["input_handler"] = f"unhealthy: {e}"
            health_status["overall"] = "degraded"
        
        try:
            # Test model interface
            model_status = self.model_interface.get_model_status()
            health_status["components"]["model_interface"] = "healthy"
            health_status["model_status"] = model_status
        except Exception as e:
            health_status["components"]["model_interface"] = f"unhealthy: {e}"
            health_status["overall"] = "degraded"
        
        try:
            # Test output formatter
            supported_formats = self.output_formatter.get_supported_formats()
            health_status["components"]["output_formatter"] = "healthy"
            health_status["supported_formats"] = supported_formats
        except Exception as e:
            health_status["components"]["output_formatter"] = f"unhealthy: {e}"
            health_status["overall"] = "degraded"
        
        return health_status

# Example usage and testing
if __name__ == "__main__":
    # Initialize orchestrator
    orchestrator = PromptOrchestrator()
    
    print("=== Prompt Orchestration System ===")
    print("Editor ভাই-এর জন্য Smart Prompt Routing System")
    print("=" * 50)
    
    # Test system status
    print("\n1. System Status:")
    status = orchestrator.get_system_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    # Test health check
    print("\n2. Health Check:")
    health = orchestrator.health_check()
    print(json.dumps(health, indent=2, ensure_ascii=False))
    
    # Test sample requests
    test_requests = [
        ("আজকের আবহাওয়া কেমন?", "json"),
        ("Hello, how are you?", "text"),
        ("আমার কোডে একটা বাগ আছে", "code"),
        ("Translate this to English", "html")
    ]
    
    print("\n3. Sample Requests:")
    for user_input, output_format in test_requests:
        print(f"\nInput: {user_input}")
        print(f"Format: {output_format}")
        print("-" * 30)
        
        try:
            response = orchestrator.process_request(user_input, output_format)
            print(f"Success: {response['success']}")
            print(f"Processing Time: {response['processing_time']:.2f}s")
            print(f"Language: {response['system_info']['language']}")
            print(f"Intent: {response['system_info']['intent']}")
            
            if isinstance(response['formatted_response'], dict):
                content = response['formatted_response'].get('content', '')
            else:
                content = str(response['formatted_response'])
            
            print(f"Response: {content[:100]}...")
            
        except Exception as e:
            print(f"Error: {e}")
    
    # Show final stats
    print("\n4. System Statistics:")
    stats = orchestrator.get_system_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    print("\n=== System Ready for Production Use ===")
