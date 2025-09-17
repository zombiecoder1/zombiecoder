#!/usr/bin/env python3
"""
Simple Test for Orchestrator System
Editor ভাই-এর জন্য Basic Test
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from config import config
        print("✅ Config imported successfully")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from input_handler import InputHandler
        print("✅ InputHandler imported successfully")
    except Exception as e:
        print(f"❌ InputHandler import failed: {e}")
        return False
    
    try:
        from prompt_refiner import PromptRefiner
        print("✅ PromptRefiner imported successfully")
    except Exception as e:
        print(f"❌ PromptRefiner import failed: {e}")
        return False
    
    try:
        from model_interface import ModelInterface
        print("✅ ModelInterface imported successfully")
    except Exception as e:
        print(f"❌ ModelInterface import failed: {e}")
        return False
    
    try:
        from output_formatter import OutputFormatter
        print("✅ OutputFormatter imported successfully")
    except Exception as e:
        print(f"❌ OutputFormatter import failed: {e}")
        return False
    
    try:
        from main_orchestrator import PromptOrchestrator
        print("✅ PromptOrchestrator imported successfully")
    except Exception as e:
        print(f"❌ PromptOrchestrator import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        from input_handler import InputHandler
        handler = InputHandler()
        
        # Test input processing
        result = handler.process_input("আজকের আবহাওয়া কেমন?")
        print(f"✅ Input processing: {result['detected_language']} - {result['intent']}")
        
    except Exception as e:
        print(f"❌ Input processing failed: {e}")
        return False
    
    try:
        from prompt_refiner import PromptRefiner
        refiner = PromptRefiner()
        
        # Test prompt refinement
        processed_input = {
            "cleaned_input": "আজকের আবহাওয়া কেমন?",
            "detected_language": "bengali",
            "intent": "weather",
            "processing_type": "weather_query",
            "timestamp": "2025-01-01T00:00:00",
            "confidence": 0.8
        }
        
        refined = refiner.refine_prompt(processed_input)
        print(f"✅ Prompt refinement: {refined['template_used']}")
        
    except Exception as e:
        print(f"❌ Prompt refinement failed: {e}")
        return False
    
    return True

def test_orchestrator():
    """Test main orchestrator"""
    print("\n🧪 Testing main orchestrator...")
    
    try:
        from main_orchestrator import PromptOrchestrator
        orchestrator = PromptOrchestrator()
        
        # Test system status
        status = orchestrator.get_system_status()
        print(f"✅ System status: {status['orchestrator']['status']}")
        
        # Test health check
        health = orchestrator.health_check()
        print(f"✅ Health check: {health['overall']}")
        
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 Simple Orchestrator Test")
    print("Editor ভাই-এর জন্য Basic System Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return False
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Basic functionality tests failed!")
        return False
    
    # Test orchestrator
    if not test_orchestrator():
        print("\n❌ Orchestrator tests failed!")
        return False
    
    print("\n🎉 ALL TESTS PASSED!")
    print("✅ Orchestrator system is working correctly!")
    print("🚀 Ready to start the server!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

