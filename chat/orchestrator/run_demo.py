#!/usr/bin/env python3
"""
Quick Demo Runner for Prompt Orchestration System
Editor ভাই-এর জন্য Simple Demo Launcher
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Run the demo with proper setup"""
    print("🚀 Starting Prompt Orchestration System Demo...")
    print("Editor ভাই-এর জন্য Smart Prompt Routing System")
    print("=" * 60)
    
    try:
        # Import and run demo
        from demo import PromptOrchestrationDemo
        
        demo = PromptOrchestrationDemo()
        demo.run_demo()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        print("Please check the system configuration and try again.")

if __name__ == "__main__":
    main()
