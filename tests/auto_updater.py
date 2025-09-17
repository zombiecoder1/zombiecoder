#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 ZombieCoder Auto Updater
Automatically updates memory files from running servers
"""

import os
import json
import time
import requests
import threading
from datetime import datetime
from typing import Dict, Any, Optional

class AutoUpdater:
    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = memory_dir
        self.running = False
        self.update_interval = 5  # seconds
        
        # Server endpoints
        self.endpoints = {
            'proxy': 'http://localhost:8080/health',
            'monitoring': 'http://localhost:9000/api/status',
            'agent_system': 'http://localhost:8004/status',
            'truth_checker': 'http://localhost:8002/status',
            'editor_integration': 'http://localhost:8003/status',
            'multi_project': 'http://localhost:8001/status',
            'main_server': 'http://localhost:12345/status',
            'ollama': 'http://localhost:11434/api/tags'
        }
        
        self.ensure_memory_dir()
    
    def ensure_memory_dir(self):
        """Ensure memory directory exists"""
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)
    
    def load_json(self, filename: str) -> Dict[Any, Any]:
        """Load JSON file or return default structure"""
        filepath = os.path.join(self.memory_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Return default structure
        defaults = {
            'servers.json': {},
            'log.json': {'entries': []},
            'conversations.json': {'messages': []},
            'stats.json': {
                'total_requests': 0,
                'local_responses': 0,
                'cloud_responses': 0,
                'avg_latency': 0,
                'current_route': 'unknown'
            }
        }
        return defaults.get(filename, {})
    
    def save_json(self, filename: str, data: Dict[Any, Any]):
        """Save data to JSON file"""
        filepath = os.path.join(self.memory_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def check_server_status(self, name: str, url: str) -> Dict[str, Any]:
        """Check individual server status"""
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'healthy',
                    'last_check': time.time(),
                    'datetime': datetime.now().isoformat(),
                    'data': data
                }
            else:
                return {
                    'status': 'unhealthy',
                    'last_check': time.time(),
                    'datetime': datetime.now().isoformat(),
                    'error': f'HTTP {response.status_code}'
                }
        except requests.exceptions.Timeout:
            return {
                'status': 'down',
                'last_check': time.time(),
                'datetime': datetime.now().isoformat(),
                'error': 'Timeout'
            }
        except requests.exceptions.ConnectionError:
            return {
                'status': 'down',
                'last_check': time.time(),
                'datetime': datetime.now().isoformat(),
                'error': 'Connection refused'
            }
        except Exception as e:
            return {
                'status': 'down',
                'last_check': time.time(),
                'datetime': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def update_servers(self):
        """Update server statuses"""
        servers = self.load_json('servers.json')
        
        for name, url in self.endpoints.items():
            status = self.check_server_status(name, url)
            servers[name] = status
        
        self.save_json('servers.json', servers)
        print(f"🔄 Updated server statuses at {datetime.now().strftime('%H:%M:%S')}")
    
    def update_stats_from_monitoring(self):
        """Update stats from monitoring dashboard"""
        try:
            response = requests.get('http://localhost:9000/api/status', timeout=3)
            if response.status_code == 200:
                data = response.json()
                
                stats = self.load_json('stats.json')
                # Better route detection logic
                local_count = data.get('requests', {}).get('local', 0)
                cloud_count = data.get('requests', {}).get('cloud', 0)
                current_latency = data.get('latency', {}).get('current', 0)
                
                # Determine route based on multiple factors
                if local_count > cloud_count:
                    current_route = 'local'
                elif cloud_count > local_count:
                    current_route = 'cloud'
                else:
                    # If equal, use latency as tiebreaker
                    current_route = 'local' if current_latency < 5000 else 'cloud'
                
                stats.update({
                    'total_requests': data.get('requests', {}).get('total', 0),
                    'local_responses': local_count,
                    'cloud_responses': cloud_count,
                    'avg_latency': current_latency,
                    'current_route': current_route
                })
                
                self.save_json('stats.json', stats)
                print(f"📊 Updated stats from monitoring dashboard")
        except Exception as e:
            print(f"⚠️  Failed to update stats: {e}")
    
    def add_system_log(self, level: str, message: str):
        """Add system log entry"""
        logs = self.load_json('log.json')
        
        entry = {
            'level': level,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'time': time.time(),
            'source': 'auto_updater'
        }
        
        logs['entries'].append(entry)
        
        # Keep only last 200 entries
        if len(logs['entries']) > 200:
            logs['entries'] = logs['entries'][-200:]
        
        self.save_json('log.json', logs)
    
    def update_cycle(self):
        """Single update cycle"""
        try:
            self.update_servers()
            self.update_stats_from_monitoring()
            
            # Add periodic log entry
            if int(time.time()) % 60 == 0:  # Every minute
                self.add_system_log('info', 'Auto-updater running - all systems monitored')
                
        except Exception as e:
            self.add_system_log('error', f'Auto-updater error: {e}')
            print(f"❌ Update cycle error: {e}")
    
    def start(self):
        """Start auto-updater"""
        self.running = True
        self.add_system_log('info', 'Auto-updater started')
        print("🚀 Auto-updater started")
        
        while self.running:
            self.update_cycle()
            time.sleep(self.update_interval)
    
    def stop(self):
        """Stop auto-updater"""
        self.running = False
        self.add_system_log('info', 'Auto-updater stopped')
        print("🛑 Auto-updater stopped")
    
    def run_once(self):
        """Run update cycle once"""
        print("🔄 Running single update cycle...")
        self.update_cycle()
        print("✅ Update cycle completed")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='ZombieCoder Auto Updater')
    parser.add_argument('--memory-dir', default='memory', help='Memory directory path')
    parser.add_argument('--interval', type=int, default=5, help='Update interval in seconds')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    
    args = parser.parse_args()
    
    updater = AutoUpdater(args.memory_dir)
    updater.update_interval = args.interval
    
    if args.once:
        updater.run_once()
    else:
        try:
            updater.start()
        except KeyboardInterrupt:
            updater.stop()

if __name__ == '__main__':
    main()
