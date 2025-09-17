"""
Demo Script for Prompt Orchestration System
Editor ভাই-এর জন্য Interactive Demo
"""

import json
import time
from datetime import datetime
from typing import Dict, List

from main_orchestrator import PromptOrchestrator

class PromptOrchestrationDemo:
    """Interactive demo for the Prompt Orchestration System"""
    
    def __init__(self):
        self.orchestrator = PromptOrchestrator()
        self.demo_requests = [
            {
                "input": "আজকের আবহাওয়া কেমন?",
                "format": "json",
                "description": "Bengali weather question"
            },
            {
                "input": "Hello, how are you today?",
                "format": "text", 
                "description": "English greeting"
            },
            {
                "input": "আমার Python কোডে একটা বাগ আছে, কীভাবে ঠিক করব?",
                "format": "code",
                "description": "Bengali coding help request"
            },
            {
                "input": "Translate this to English: 'আমি একজন প্রোগ্রামার'",
                "format": "html",
                "description": "Translation request"
            },
            {
                "input": "What is machine learning?",
                "format": "conversation",
                "description": "Educational question"
            }
        ]
    
    def run_demo(self):
        """Run the complete demo"""
        print("🚀 Prompt Orchestration System Demo")
        print("Editor ভাই-এর জন্য Smart Prompt Routing System")
        print("=" * 60)
        
        # Show system status
        self._show_system_status()
        
        # Run demo requests
        self._run_demo_requests()
        
        # Show conversation history
        self._show_conversation_history()
        
        # Show system statistics
        self._show_system_stats()
        
        # Interactive mode
        self._interactive_mode()
    
    def _show_system_status(self):
        """Display system status"""
        print("\n📊 System Status:")
        print("-" * 30)
        
        try:
            status = self.orchestrator.get_system_status()
            
            print(f"Orchestrator: {status['orchestrator']['status']}")
            print(f"Session ID: {status['orchestrator']['session_id']}")
            print(f"Uptime: {status['orchestrator']['uptime']:.2f} seconds")
            
            print("\nComponents:")
            for component, state in status['components'].items():
                print(f"  {component}: {state}")
            
            print("\nModel Status:")
            for model, info in status['models'].items():
                print(f"  {model}: {info['status']}")
            
            print(f"\nSupported Formats: {', '.join(status['supported_formats'])}")
            
        except Exception as e:
            print(f"Error getting system status: {e}")
    
    def _run_demo_requests(self):
        """Run demo requests"""
        print("\n🎯 Running Demo Requests:")
        print("-" * 40)
        
        for i, request in enumerate(self.demo_requests, 1):
            print(f"\n{i}. {request['description']}")
            print(f"   Input: {request['input']}")
            print(f"   Format: {request['format']}")
            print("   Processing...")
            
            try:
                start_time = time.time()
                response = self.orchestrator.process_request(
                    user_input=request['input'],
                    output_format=request['format']
                )
                end_time = time.time()
                
                print(f"   ✅ Success: {response['success']}")
                print(f"   ⏱️  Processing Time: {response['processing_time']:.2f}s")
                print(f"   🌐 Language: {response['system_info']['language']}")
                print(f"   🎯 Intent: {response['system_info']['intent']}")
                print(f"   🤖 Model: {response['model_response']['model_used']}")
                
                # Show response preview
                if isinstance(response['formatted_response'], dict):
                    content = response['formatted_response'].get('content', '')
                else:
                    content = str(response['formatted_response'])
                
                preview = content[:100] + "..." if len(content) > 100 else content
                print(f"   📝 Response Preview: {preview}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print("   " + "-" * 50)
    
    def _show_conversation_history(self):
        """Display conversation history"""
        print("\n💬 Conversation History:")
        print("-" * 30)
        
        try:
            history = self.orchestrator.get_conversation_history(5)
            
            if not history:
                print("No conversation history available.")
                return
            
            for i, entry in enumerate(history, 1):
                print(f"\n{i}. {entry['timestamp']}")
                print(f"   Input: {entry['user_input'][:50]}...")
                print(f"   Language: {entry['language']}")
                print(f"   Intent: {entry['intent']}")
                print(f"   Processing Time: {entry['processing_time']:.2f}s")
                
        except Exception as e:
            print(f"Error getting conversation history: {e}")
    
    def _show_system_stats(self):
        """Display system statistics"""
        print("\n📈 System Statistics:")
        print("-" * 25)
        
        try:
            stats = self.orchestrator.get_system_stats()
            
            print(f"Total Requests: {stats['total_requests']}")
            print(f"Successful: {stats['successful_requests']}")
            print(f"Failed: {stats['failed_requests']}")
            print(f"Success Rate: {stats['success_rate']:.1f}%")
            print(f"Conversation Exchanges: {stats['conversation_exchanges']}")
            print(f"Uptime: {stats['uptime_seconds']:.2f} seconds")
            
        except Exception as e:
            print(f"Error getting system stats: {e}")
    
    def _interactive_mode(self):
        """Run interactive mode"""
        print("\n🎮 Interactive Mode:")
        print("-" * 20)
        print("Enter your questions (type 'quit' to exit, 'help' for commands)")
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Thanks for using the Prompt Orchestration System!")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if user_input.lower() == 'status':
                    self._show_system_status()
                    continue
                
                if user_input.lower() == 'stats':
                    self._show_system_stats()
                    continue
                
                if user_input.lower() == 'history':
                    self._show_conversation_history()
                    continue
                
                if user_input.lower() == 'reset':
                    self.orchestrator.reset_session()
                    print("🔄 Session reset successfully!")
                    continue
                
                if not user_input:
                    continue
                
                # Process the request
                print("Processing...")
                start_time = time.time()
                
                response = self.orchestrator.process_request(
                    user_input=user_input,
                    output_format="json"
                )
                
                end_time = time.time()
                
                if response['success']:
                    print(f"✅ Response ({response['processing_time']:.2f}s):")
                    
                    if isinstance(response['formatted_response'], dict):
                        content = response['formatted_response'].get('content', '')
                    else:
                        content = str(response['formatted_response'])
                    
                    print(f"🌐 Language: {response['system_info']['language']}")
                    print(f"🎯 Intent: {response['system_info']['intent']}")
                    print(f"🤖 Model: {response['model_response']['model_used']}")
                    print(f"\n📝 Response:\n{content}")
                    
                else:
                    print(f"❌ Error: {response.get('error', 'Unknown error')}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Thanks for using the Prompt Orchestration System!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_help(self):
        """Show help information"""
        print("\n📖 Available Commands:")
        print("  help     - Show this help message")
        print("  status   - Show system status")
        print("  stats    - Show system statistics")
        print("  history  - Show conversation history")
        print("  reset    - Reset current session")
        print("  quit     - Exit the demo")
        print("\n💡 Tips:")
        print("  - Ask questions in Bengali or English")
        print("  - Try coding questions, translations, or general queries")
        print("  - The system will automatically detect language and intent")

def main():
    """Main function to run the demo"""
    demo = PromptOrchestrationDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()
