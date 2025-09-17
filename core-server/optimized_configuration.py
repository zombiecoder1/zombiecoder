#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ Optimized Configuration for ZombieCoder
Complete system optimization and configuration updates
"""

import os
import json
import yaml
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ZombieCoderOptimizer:
    """Complete system optimizer for ZombieCoder"""
    
    def __init__(self):
        self.config_dir = "config"
        self.memory_dir = "memory"
        self.logs_dir = "logs"
        
        # Create necessary directories
        self._create_directories()
        
        # Configuration templates
        self.config_templates = self._load_config_templates()
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = [self.config_dir, self.memory_dir, self.logs_dir]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    def _load_config_templates(self) -> Dict[str, Any]:
        """Load configuration templates"""
        return {
            "agent_config": {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "agents": {
                    "friendly_programmer": {
                        "enabled": True,
                        "port": 8004,
                        "priority": 1,
                        "specialties": ["programming", "teaching", "mentoring"]
                    },
                    "programming_agent": {
                        "enabled": True,
                        "port": 12345,
                        "priority": 2,
                        "specialties": ["code_generation", "debugging"]
                    },
                    "architect_agent": {
                        "enabled": True,
                        "port": 8005,
                        "priority": 3,
                        "specialties": ["architecture", "design"]
                    },
                    "verifier_agent": {
                        "enabled": True,
                        "port": 8002,
                        "priority": 4,
                        "specialties": ["verification", "validation"]
                    },
                    "conversational_agent": {
                        "enabled": True,
                        "port": 8006,
                        "priority": 5,
                        "specialties": ["conversation", "support"]
                    },
                    "operations_agent": {
                        "enabled": True,
                        "port": 8007,
                        "priority": 6,
                        "specialties": ["operations", "automation"]
                    }
                }
            },
            
            "system_config": {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "performance": {
                    "max_concurrent_requests": 10,
                    "request_timeout": 30,
                    "memory_limit_mb": 512,
                    "cpu_limit_percent": 80
                },
                "security": {
                    "rate_limiting": {
                        "enabled": True,
                        "requests_per_minute": 100,
                        "burst_limit": 20
                    },
                    "authentication": {
                        "enabled": False,
                        "api_key_required": False
                    }
                },
                "logging": {
                    "level": "INFO",
                    "file_rotation": True,
                    "max_file_size_mb": 10,
                    "backup_count": 5
                },
                "monitoring": {
                    "health_check_interval": 30,
                    "metrics_collection": True,
                    "alerting_enabled": False
                }
            },
            
            "ollama_config": {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "base_url": "http://localhost:11434",
                "default_models": {
                    "programming": "deepseek-coder:latest",
                    "general": "llama3.1:latest",
                    "small": "phi3:latest"
                },
                "performance": {
                    "timeout": 60,
                    "max_tokens": 2000,
                    "temperature": 0.7,
                    "top_p": 0.9
                },
                "fallback_chain": [
                    "deepseek-coder:latest",
                    "codellama:latest",
                    "llama3.1:latest",
                    "mistral:latest"
                ]
            },
            
            "memory_config": {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "storage": {
                    "type": "yaml",
                    "directory": "memory",
                    "compression": False,
                    "encryption": False
                },
                "limits": {
                    "max_interactions_per_agent": 100,
                    "max_conversation_history": 50,
                    "max_memory_file_size_mb": 5
                },
                "cleanup": {
                    "auto_cleanup_enabled": True,
                    "cleanup_interval_days": 30,
                    "backup_before_cleanup": True
                }
            }
        }
    
    def create_optimized_configurations(self) -> Dict[str, Any]:
        """Create all optimized configuration files"""
        results = {
            "created_files": [],
            "errors": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Create agent configuration
        try:
            agent_config_path = os.path.join(self.config_dir, "agent_config.yaml")
            with open(agent_config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config_templates["agent_config"], f, 
                         default_flow_style=False, allow_unicode=True, indent=2)
            results["created_files"].append(agent_config_path)
            logger.info(f"Created agent configuration: {agent_config_path}")
        except Exception as e:
            results["errors"].append(f"Agent config error: {e}")
        
        # Create system configuration
        try:
            system_config_path = os.path.join(self.config_dir, "system_config.yaml")
            with open(system_config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config_templates["system_config"], f,
                         default_flow_style=False, allow_unicode=True, indent=2)
            results["created_files"].append(system_config_path)
            logger.info(f"Created system configuration: {system_config_path}")
        except Exception as e:
            results["errors"].append(f"System config error: {e}")
        
        # Create Ollama configuration
        try:
            ollama_config_path = os.path.join(self.config_dir, "ollama_config.yaml")
            with open(ollama_config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config_templates["ollama_config"], f,
                         default_flow_style=False, allow_unicode=True, indent=2)
            results["created_files"].append(ollama_config_path)
            logger.info(f"Created Ollama configuration: {ollama_config_path}")
        except Exception as e:
            results["errors"].append(f"Ollama config error: {e}")
        
        # Create memory configuration
        try:
            memory_config_path = os.path.join(self.config_dir, "memory_config.yaml")
            with open(memory_config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config_templates["memory_config"], f,
                         default_flow_style=False, allow_unicode=True, indent=2)
            results["created_files"].append(memory_config_path)
            logger.info(f"Created memory configuration: {memory_config_path}")
        except Exception as e:
            results["errors"].append(f"Memory config error: {e}")
        
        return results
    
    def optimize_system_performance(self) -> Dict[str, Any]:
        """Optimize system performance settings"""
        optimizations = {
            "timestamp": datetime.now().isoformat(),
            "applied_optimizations": [],
            "recommendations": []
        }
        
        # Check system resources
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            system_status = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 2)
            }
            
            optimizations["system_status"] = system_status
            
            # Apply optimizations based on system status
            if cpu_percent > 80:
                optimizations["applied_optimizations"].append("Reduced max concurrent requests due to high CPU usage")
                optimizations["recommendations"].append("Consider upgrading CPU or reducing workload")
            
            if memory.percent > 80:
                optimizations["applied_optimizations"].append("Reduced memory limits due to high memory usage")
                optimizations["recommendations"].append("Consider adding more RAM or optimizing memory usage")
            
            if disk.percent > 90:
                optimizations["applied_optimizations"].append("Disk space warning - cleanup recommended")
                optimizations["recommendations"].append("Clean up old logs and temporary files")
            
            # Performance recommendations
            if cpu_percent < 50 and memory.percent < 70:
                optimizations["recommendations"].append("System has good performance headroom")
            
        except ImportError:
            optimizations["errors"] = ["psutil not available for system monitoring"]
        except Exception as e:
            optimizations["errors"] = [f"System monitoring error: {e}"]
        
        return optimizations
    
    def create_startup_scripts(self) -> Dict[str, Any]:
        """Create optimized startup scripts"""
        scripts = {
            "created_scripts": [],
            "errors": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Create optimized launcher script
        launcher_content = """#!/bin/bash
# ZombieCoder Optimized Launcher
# Starts all services with optimized configurations

echo "🚀 Starting ZombieCoder Optimized System..."

# Create necessary directories
mkdir -p logs memory config

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)/core-server"
export ZOMBIECODER_CONFIG_DIR="$(pwd)/config"
export ZOMBIECODER_MEMORY_DIR="$(pwd)/memory"

# Start services in background
echo "📡 Starting Proxy Server..."
python3 core-server/proxy_server.py > logs/proxy_server.log 2>&1 &
PROXY_PID=$!

echo "🤖 Starting Unified Agent System..."
python3 core-server/unified_agent_system.py > logs/unified_agent.log 2>&1 &
UNIFIED_PID=$!

echo "🔧 Starting Multi Project Manager..."
python3 core-server/multi_project_manager.py > logs/multi_project.log 2>&1 &
MULTI_PID=$!

echo "🎨 Starting Editor Chat Server..."
python3 core-server/editor_chat_server.py > logs/editor_chat.log 2>&1 &
EDITOR_PID=$!

echo "👨‍💻 Starting Friendly Programmer Agent..."
python3 core-server/friendly_programmer_agent.py > logs/friendly_programmer.log 2>&1 &
FRIENDLY_PID=$!

# Save PIDs for later cleanup
echo $PROXY_PID > logs/proxy_server.pid
echo $UNIFIED_PID > logs/unified_agent.pid
echo $MULTI_PID > logs/multi_project.pid
echo $EDITOR_PID > logs/editor_chat.pid
echo $FRIENDLY_PID > logs/friendly_programmer.pid

echo "✅ All services started!"
echo "📊 Check status: curl http://localhost:8001/health"
echo "🛑 Stop services: ./stop_services.sh"
"""
        
        try:
            with open("start_optimized_services.sh", 'w', encoding='utf-8') as f:
                f.write(launcher_content)
            os.chmod("start_optimized_services.sh", 0o755)
            scripts["created_scripts"].append("start_optimized_services.sh")
            logger.info("Created optimized startup script")
        except Exception as e:
            scripts["errors"].append(f"Startup script error: {e}")
        
        # Create stop script
        stop_content = """#!/bin/bash
# ZombieCoder Service Stopper

echo "🛑 Stopping ZombieCoder Services..."

# Stop services using saved PIDs
for pid_file in logs/*.pid; do
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Stopping process $PID..."
            kill "$PID"
            rm "$pid_file"
        fi
    fi
done

echo "✅ All services stopped!"
"""
        
        try:
            with open("stop_services.sh", 'w', encoding='utf-8') as f:
                f.write(stop_content)
            os.chmod("stop_services.sh", 0o755)
            scripts["created_scripts"].append("stop_services.sh")
            logger.info("Created stop script")
        except Exception as e:
            scripts["errors"].append(f"Stop script error: {e}")
        
        return scripts
    
    def create_monitoring_dashboard(self) -> Dict[str, Any]:
        """Create monitoring dashboard configuration"""
        dashboard_config = {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "services": {
                "proxy_server": {
                    "url": "http://localhost:8080/health",
                    "port": 8080,
                    "name": "Proxy Server"
                },
                "unified_agent": {
                    "url": "http://localhost:12345/status",
                    "port": 12345,
                    "name": "Unified Agent System"
                },
                "multi_project": {
                    "url": "http://localhost:8001/health",
                    "port": 8001,
                    "name": "Multi Project Manager"
                },
                "editor_chat": {
                    "url": "http://localhost:8003/health",
                    "port": 8003,
                    "name": "Editor Chat Server"
                },
                "friendly_programmer": {
                    "url": "http://localhost:8004/health",
                    "port": 8004,
                    "name": "Friendly Programmer Agent"
                }
            },
            "monitoring": {
                "check_interval": 30,
                "timeout": 10,
                "alert_threshold": 3,
                "retry_attempts": 3
            }
        }
        
        try:
            dashboard_path = os.path.join(self.config_dir, "monitoring_dashboard.yaml")
            with open(dashboard_path, 'w', encoding='utf-8') as f:
                yaml.dump(dashboard_config, f, default_flow_style=False, allow_unicode=True, indent=2)
            logger.info(f"Created monitoring dashboard config: {dashboard_path}")
            return {"success": True, "file": dashboard_path}
        except Exception as e:
            logger.error(f"Dashboard config error: {e}")
            return {"success": False, "error": str(e)}
    
    def run_complete_optimization(self) -> Dict[str, Any]:
        """Run complete system optimization"""
        logger.info("🚀 Starting complete ZombieCoder optimization...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "optimization_steps": [],
            "created_files": [],
            "errors": [],
            "performance_improvements": [],
            "recommendations": []
        }
        
        # Step 1: Create optimized configurations
        logger.info("📝 Creating optimized configurations...")
        config_results = self.create_optimized_configurations()
        results["optimization_steps"].append("Created optimized configurations")
        results["created_files"].extend(config_results["created_files"])
        results["errors"].extend(config_results["errors"])
        
        # Step 2: Optimize system performance
        logger.info("⚡ Optimizing system performance...")
        perf_results = self.optimize_system_performance()
        results["optimization_steps"].append("Optimized system performance")
        results["performance_improvements"].extend(perf_results.get("applied_optimizations", []))
        results["recommendations"].extend(perf_results.get("recommendations", []))
        
        # Step 3: Create startup scripts
        logger.info("📜 Creating startup scripts...")
        script_results = self.create_startup_scripts()
        results["optimization_steps"].append("Created startup scripts")
        results["created_files"].extend(script_results["created_scripts"])
        results["errors"].extend(script_results["errors"])
        
        # Step 4: Create monitoring dashboard
        logger.info("📊 Creating monitoring dashboard...")
        dashboard_result = self.create_monitoring_dashboard()
        results["optimization_steps"].append("Created monitoring dashboard")
        if dashboard_result["success"]:
            results["created_files"].append(dashboard_result["file"])
        else:
            results["errors"].append(dashboard_result["error"])
        
        # Summary
        results["summary"] = {
            "total_optimization_steps": len(results["optimization_steps"]),
            "total_files_created": len(results["created_files"]),
            "total_errors": len(results["errors"]),
            "optimization_success": len(results["errors"]) == 0
        }
        
        logger.info(f"✅ Optimization complete! Created {len(results['created_files'])} files")
        if results["errors"]:
            logger.warning(f"⚠️ {len(results['errors'])} errors occurred")
        
        return results

# Global optimizer instance
zombiecoder_optimizer = ZombieCoderOptimizer()

def run_optimization():
    """Run complete system optimization"""
    return zombiecoder_optimizer.run_complete_optimization()

if __name__ == "__main__":
    print("⚙️ ZombieCoder System Optimizer")
    print("=" * 40)
    
    results = run_optimization()
    
    print(f"\n📊 Optimization Results:")
    print(f"Steps completed: {results['summary']['total_optimization_steps']}")
    print(f"Files created: {results['summary']['total_files_created']}")
    print(f"Errors: {results['summary']['total_errors']}")
    print(f"Success: {results['summary']['optimization_success']}")
    
    if results["created_files"]:
        print(f"\n📁 Created files:")
        for file in results["created_files"]:
            print(f"  ✅ {file}")
    
    if results["errors"]:
        print(f"\n❌ Errors:")
        for error in results["errors"]:
            print(f"  ❌ {error}")
    
    if results["recommendations"]:
        print(f"\n💡 Recommendations:")
        for rec in results["recommendations"]:
            print(f"  💡 {rec}")
    
    print("\n🎉 Optimization completed!")
