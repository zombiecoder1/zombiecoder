#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 ZombieCoder Complete System Check
====================================

Comprehensive verification of all system components:
- Memory usage monitoring
- Cloud AI blocking verification
- Service health checks
- Configuration validation
- Performance metrics
"""

import os
import sys
import time
import json
import requests
import psutil
import subprocess
from datetime import datetime
from typing import Dict, Any, List

class ZombieCoderSystemCheck:
    """Complete system verification and monitoring"""
    
    def __init__(self):
        self.start_time = time.time()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "system_info": {},
            "services": {},
            "cloud_blocking": {},
            "memory_usage": {},
            "performance": {},
            "recommendations": []
        }
        
    def check_system_info(self):
        """Check basic system information"""
        try:
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent()
            disk = psutil.disk_usage('/')
            
            self.results["system_info"] = {
                "platform": sys.platform,
                "python_version": sys.version,
                "memory_total_gb": round(memory.total / (1024**3), 2),
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "memory_percent": memory.percent,
                "cpu_percent": cpu,
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "disk_percent": disk.percent
            }
            
            print(f"✅ System Info: {memory.total // (1024**3)}GB RAM, {cpu}% CPU")
            return True
        except Exception as e:
            print(f"❌ System Info Error: {e}")
            return False
    
    def check_ollama_memory(self):
        """Check Ollama memory usage and processes"""
        try:
            ollama_processes = []
            total_memory_mb = 0
            
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                if 'ollama' in proc.info['name'].lower():
                    memory_mb = proc.info['memory_info'].rss / (1024**2)
                    ollama_processes.append({
                        "pid": proc.info['pid'],
                        "memory_mb": round(memory_mb, 2)
                    })
                    total_memory_mb += memory_mb
            
            self.results["memory_usage"]["ollama"] = {
                "processes": ollama_processes,
                "total_memory_mb": round(total_memory_mb, 2),
                "process_count": len(ollama_processes),
                "status": "normal" if total_memory_mb < 5000 else "high"
            }
            
            if total_memory_mb > 5000:
                self.results["recommendations"].append("⚠️ Ollama memory usage high - consider restart")
                print(f"⚠️ Ollama Memory: {total_memory_mb:.1f}MB ({len(ollama_processes)} processes)")
            else:
                print(f"✅ Ollama Memory: {total_memory_mb:.1f}MB ({len(ollama_processes)} processes)")
            
            return True
        except Exception as e:
            print(f"❌ Ollama Memory Check Error: {e}")
            return False
    
    def check_cloud_blocking(self):
        """Verify cloud AI domain blocking"""
        cloud_domains = [
            "api.openai.com",
            "api.anthropic.com", 
            "oai.hf.space",
            "openaiapi-site.azureedge.net",
            "openrouter.ai",
            "api.openrouter.ai"
        ]
        
        blocked_count = 0
        domain_results = {}
        
        for domain in cloud_domains:
            try:
                # Use nslookup to check DNS resolution
                result = subprocess.run(
                    ['nslookup', domain], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                
                if '127.0.0.1' in result.stdout:
                    domain_results[domain] = {"status": "blocked", "ip": "127.0.0.1"}
                    blocked_count += 1
                else:
                    domain_results[domain] = {"status": "accessible", "ip": "unknown"}
                    
            except Exception as e:
                domain_results[domain] = {"status": "error", "error": str(e)}
        
        self.results["cloud_blocking"] = {
            "total_domains": len(cloud_domains),
            "blocked_domains": blocked_count,
            "blocking_percentage": round((blocked_count / len(cloud_domains)) * 100, 1),
            "domains": domain_results,
            "status": "secure" if blocked_count == len(cloud_domains) else "vulnerable"
        }
        
        print(f"✅ Cloud Blocking: {blocked_count}/{len(cloud_domains)} domains blocked ({self.results['cloud_blocking']['blocking_percentage']}%)")
        return blocked_count == len(cloud_domains)
    
    def check_service_health(self):
        """Check all local AI services"""
        services = {
            "openai_shim": {
                "url": "http://127.0.0.1:8001/health",
                "name": "OpenAI Shim"
            },
            "zombiecoder": {
                "url": "http://127.0.0.1:12345/status", 
                "name": "ZombieCoder"
            },
            "ollama": {
                "url": "http://127.0.0.1:11434/api/tags",
                "name": "Ollama"
            }
        }
        
        healthy_count = 0
        
        for service_name, config in services.items():
            try:
                response = requests.get(config["url"], timeout=5)
                if response.status_code == 200:
                    self.results["services"][service_name] = {
                        "status": "healthy",
                        "response_time": response.elapsed.total_seconds(),
                        "status_code": response.status_code
                    }
                    healthy_count += 1
                    print(f"✅ {config['name']}: Healthy ({response.elapsed.total_seconds():.2f}s)")
                else:
                    self.results["services"][service_name] = {
                        "status": "unhealthy",
                        "status_code": response.status_code
                    }
                    print(f"❌ {config['name']}: Unhealthy (HTTP {response.status_code})")
                    
            except Exception as e:
                self.results["services"][service_name] = {
                    "status": "offline",
                    "error": str(e)
                }
                print(f"❌ {config['name']}: Offline ({str(e)})")
        
        self.results["services"]["overall"] = {
            "healthy_count": healthy_count,
            "total_count": len(services),
            "health_percentage": round((healthy_count / len(services)) * 100, 1)
        }
        
        return healthy_count == len(services)
    
    def check_configuration(self):
        """Verify configuration files and environment"""
        config_files = [
            ".env",
            ".vscode/settings.json", 
            ".cursor/settings.json",
            ".cursorrules"
        ]
        
        env_vars = [
            "OPENAI_API_BASE",
            "OPENAI_API_KEY", 
            "FORCE_LOCAL_AI",
            "AI_PROVIDER",
            "AI_MODEL"
        ]
        
        config_status = {"files": {}, "environment": {}}
        
        # Check config files
        for file_path in config_files:
            if os.path.exists(file_path):
                config_status["files"][file_path] = "exists"
            else:
                config_status["files"][file_path] = "missing"
        
        # Check environment variables
        for var in env_vars:
            value = os.getenv(var, "")
            if value:
                config_status["environment"][var] = "set"
            else:
                config_status["environment"][var] = "unset"
        
        self.results["configuration"] = config_status
        
        existing_files = sum(1 for status in config_status["files"].values() if status == "exists")
        set_vars = sum(1 for status in config_status["environment"].values() if status == "set")
        
        print(f"✅ Configuration: {existing_files}/{len(config_files)} files, {set_vars}/{len(env_vars)} env vars")
        
        return existing_files == len(config_files) and set_vars == len(env_vars)
    
    def generate_report(self):
        """Generate comprehensive system report"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        self.results["performance"]["check_duration"] = round(duration, 2)
        self.results["performance"]["timestamp_end"] = datetime.now().isoformat()
        
        # Overall system status
        all_services_healthy = all(
            service.get("status") == "healthy" 
            for service in self.results["services"].values() 
            if isinstance(service, dict) and "status" in service
        )
        
        cloud_fully_blocked = self.results["cloud_blocking"]["status"] == "secure"
        memory_normal = self.results["memory_usage"].get("ollama", {}).get("status") == "normal"
        
        if all_services_healthy and cloud_fully_blocked and memory_normal:
            overall_status = "EXCELLENT"
        elif all_services_healthy and cloud_fully_blocked:
            overall_status = "GOOD"
        elif all_services_healthy:
            overall_status = "FAIR"
        else:
            overall_status = "NEEDS_ATTENTION"
        
        self.results["overall_status"] = overall_status
        
        # Save report
        report_file = f"system_check_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return report_file
    
    def run_complete_check(self):
        """Run all system checks"""
        print("🔍 ZombieCoder Complete System Check")
        print("=" * 50)
        
        print("\n[1/5] System Information...")
        self.check_system_info()
        
        print("\n[2/5] Ollama Memory Check...")
        self.check_ollama_memory()
        
        print("\n[3/5] Cloud AI Blocking...")
        self.check_cloud_blocking()
        
        print("\n[4/5] Service Health...")
        self.check_service_health()
        
        print("\n[5/5] Configuration...")
        self.check_configuration()
        
        print("\n" + "=" * 50)
        print("📊 GENERATING REPORT...")
        
        report_file = self.generate_report()
        
        print(f"\n🎯 OVERALL STATUS: {self.results['overall_status']}")
        print(f"📁 Report saved: {report_file}")
        
        if self.results["recommendations"]:
            print("\n💡 RECOMMENDATIONS:")
            for rec in self.results["recommendations"]:
                print(f"   • {rec}")
        
        return self.results

if __name__ == "__main__":
    checker = ZombieCoderSystemCheck()
    results = checker.run_complete_check()
