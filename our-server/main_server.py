#!/usr/bin/env python3
"""
🤖 ZombieCoder Agent Personal - Main Server
"যেখানে কোড ও কথা বলে"

Main AI server that handles all agent requests, provides unified interface,
and manages local AI models with cloud fallback support.
"""

import os
import sys
import json
import logging
import threading
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    import requests
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Run: pip install flask flask-cors requests")
    sys.exit(1)

# Import our modules
try:
    from memory_manager import MemoryManager
    from unified_agent_system import UnifiedAgent
    from ai_providers import AIProviders
    from database_manager import DatabaseManager
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('our-server/logs/main_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ZombieCoderMainServer:
    """Main server for ZombieCoder Agent Personal"""
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize components
        self.memory_manager = MemoryManager()
        self.unified_agent = UnifiedAgent()
        self.ai_providers = AIProviders()
        self.db_manager = DatabaseManager()
        
        # Server status
        self.server_status = "starting"
        self.start_time = datetime.now()
        self.request_count = 0
        
        # Setup routes
        self.setup_routes()
        
        logger.info("🚀 Starting আমাদের সার্ভার...")
        logger.info(f"🌐 Smart Router URL: http://localhost:9000")
        logger.info(f"🤖 Ollama URL: http://localhost:11434")
        logger.info(f"📊 Server Port: {self.config.get('server', {}).get('port', 12345)}")
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open('our-server/config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("❌ Config file not found: our-server/config.json")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON in config: {e}")
            return {}
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/api/status', methods=['GET'])
        def get_status():
            """Get server status"""
            try:
                return jsonify({
                    'status': 'active',
                    'server': 'ZombieCoder Agent Personal',
                    'version': '1.0.0',
                    'uptime': str(datetime.now() - self.start_time),
                    'requests': self.request_count,
                    'memory': self.memory_manager.get_status(),
                    'agent': self.unified_agent.get_status(),
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Status error: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            """Main chat endpoint"""
            try:
                self.request_count += 1
                data = request.get_json()
                
                if not data or 'message' not in data:
                    return jsonify({'error': 'Message required'}), 400
                
                message = data['message']
                context = data.get('context', {})
                agent_type = context.get('agent', 'unified')
                
                logger.info(f"💬 Chat request: {agent_type} - {message[:50]}...")
                
                # Process with unified agent
                response = self.unified_agent.process_message(message, context)
                
                # Log to memory
                self.memory_manager.log_chat(message, response, agent_type)
                
                return jsonify({
                    'response': response,
                    'agent': agent_type,
                    'timestamp': datetime.now().isoformat(),
                    'request_id': self.request_count
                })
                
            except Exception as e:
                logger.error(f"Chat error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/agents/<agent_type>', methods=['GET'])
        def get_agent_status(agent_type):
            """Get specific agent status"""
            try:
                if agent_type == 'unified':
                    status = self.unified_agent.get_status()
                else:
                    status = {'error': f'Agent {agent_type} not found'}
                
                return jsonify(status)
            except Exception as e:
                logger.error(f"Agent status error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/memory', methods=['GET'])
        def get_memory():
            """Get memory status"""
            try:
                return jsonify(self.memory_manager.get_status())
            except Exception as e:
                logger.error(f"Memory error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            try:
                # Check Ollama
                ollama_status = "unknown"
                try:
                    response = requests.get("http://localhost:11434/api/tags", timeout=5)
                    ollama_status = "active" if response.status_code == 200 else "inactive"
                except:
                    ollama_status = "inactive"
                
                return jsonify({
                    'status': 'healthy',
                    'server': 'active',
                    'ollama': ollama_status,
                    'memory': 'active',
                    'agent': 'active',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Health check error: {e}")
                return jsonify({'status': 'unhealthy', 'error': str(e)}), 500
    
    def start(self):
        """Start the server"""
        try:
            port = self.config.get('server', {}).get('port', 12345)
            host = self.config.get('server', {}).get('host', '0.0.0.0')
            
            self.server_status = "running"
            logger.info(f"✅ Server started on {host}:{port}")
            
            self.app.run(
                host=host,
                port=port,
                debug=False,
                threaded=True
            )
        except Exception as e:
            logger.error(f"❌ Server start error: {e}")
            self.server_status = "error"

def main():
    """Main entry point"""
    try:
        server = ZombieCoderMainServer()
        server.start()
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
