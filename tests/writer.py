#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 ZombieCoder Memory Writer
Write conversations and stats to memory files
"""

import os
import json
import time
import argparse
from datetime import datetime
from typing import Dict, Any

class MemoryWriter:
    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = memory_dir
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
        
        # Return default structure based on filename
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
    
    def append_conversation(self, actor: str, text: str):
        """Append a conversation message"""
        conversations = self.load_json('conversations.json')
        
        message = {
            'actor': actor,
            'text': text,
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat()
        }
        
        conversations['messages'].append(message)
        
        # Keep only last 100 messages
        if len(conversations['messages']) > 100:
            conversations['messages'] = conversations['messages'][-100:]
        
        self.save_json('conversations.json', conversations)
        print(f"✅ Added {actor} message: {text[:50]}...")
    
    def append_log(self, level: str, message: str):
        """Append a log entry"""
        logs = self.load_json('log.json')
        
        entry = {
            'level': level,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'time': time.time()
        }
        
        logs['entries'].append(entry)
        
        # Keep only last 200 entries
        if len(logs['entries']) > 200:
            logs['entries'] = logs['entries'][-200:]
        
        self.save_json('log.json', logs)
        print(f"✅ Added {level} log: {message[:50]}...")
    
    def update_stats(self, **kwargs):
        """Update statistics"""
        stats = self.load_json('stats.json')
        
        for key, value in kwargs.items():
            if key in stats:
                stats[key] = value
            else:
                print(f"⚠️  Unknown stat key: {key}")
        
        self.save_json('stats.json', stats)
        print(f"✅ Updated stats: {kwargs}")
    
    def update_server_status(self, server_name: str, status: str, **extra):
        """Update server status"""
        servers = self.load_json('servers.json')
        
        servers[server_name] = {
            'status': status,
            'last_check': time.time(),
            'datetime': datetime.now().isoformat(),
            **extra
        }
        
        self.save_json('servers.json', servers)
        print(f"✅ Updated {server_name} status: {status}")
    
    def clear_memory(self):
        """Clear all memory data"""
        files = ['servers.json', 'log.json', 'conversations.json', 'stats.json']
        
        for filename in files:
            filepath = os.path.join(self.memory_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        
        # Recreate with default structures
        self.load_json('servers.json')
        self.load_json('log.json')
        self.load_json('conversations.json')
        self.load_json('stats.json')
        
        print("✅ Memory cleared successfully")
    
    def show_status(self):
        """Show current memory status"""
        print("📊 Memory Status:")
        print("=" * 50)
        
        files = ['servers.json', 'log.json', 'conversations.json', 'stats.json']
        
        for filename in files:
            data = self.load_json(filename)
            print(f"\n📁 {filename}:")
            
            if filename == 'servers.json':
                for server, status in data.items():
                    print(f"  {server}: {status.get('status', 'unknown')}")
            
            elif filename == 'log.json':
                entries = data.get('entries', [])
                print(f"  Total entries: {len(entries)}")
                if entries:
                    latest = entries[-1]
                    print(f"  Latest: [{latest['level']}] {latest['message'][:50]}...")
            
            elif filename == 'conversations.json':
                messages = data.get('messages', [])
                print(f"  Total messages: {len(messages)}")
                if messages:
                    latest = messages[-1]
                    print(f"  Latest: {latest['actor']}: {latest['text'][:50]}...")
            
            elif filename == 'stats.json':
                for key, value in data.items():
                    print(f"  {key}: {value}")

def main():
    parser = argparse.ArgumentParser(description='ZombieCoder Memory Writer')
    parser.add_argument('--memory-dir', default='memory', help='Memory directory path')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Append conversation
    append_parser = subparsers.add_parser('append', help='Append conversation message')
    append_parser.add_argument('--actor', required=True, choices=['user', 'assistant'], help='Message actor')
    append_parser.add_argument('--text', required=True, help='Message text')
    
    # Append log
    log_parser = subparsers.add_parser('log', help='Append log entry')
    log_parser.add_argument('--level', required=True, choices=['info', 'warning', 'error'], help='Log level')
    log_parser.add_argument('--message', required=True, help='Log message')
    
    # Update stats
    stat_parser = subparsers.add_parser('stat', help='Update statistics')
    stat_parser.add_argument('--set', nargs='+', help='Set stat values (key=value format)')
    
    # Update server status
    server_parser = subparsers.add_parser('server', help='Update server status')
    server_parser.add_argument('--name', required=True, help='Server name')
    server_parser.add_argument('--status', required=True, choices=['healthy', 'unhealthy', 'down'], help='Server status')
    
    # Clear memory
    subparsers.add_parser('clear', help='Clear all memory data')
    
    # Show status
    subparsers.add_parser('status', help='Show memory status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    writer = MemoryWriter(args.memory_dir)
    
    if args.command == 'append':
        writer.append_conversation(args.actor, args.text)
    
    elif args.command == 'log':
        writer.append_log(args.level, args.message)
    
    elif args.command == 'stat':
        if args.set:
            stats = {}
            for item in args.set:
                if '=' in item:
                    key, value = item.split('=', 1)
                    # Try to convert to number if possible
                    try:
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                    stats[key] = value
            writer.update_stats(**stats)
        else:
            print("❌ No stats provided. Use --set key=value")
    
    elif args.command == 'server':
        writer.update_server_status(args.name, args.status)
    
    elif args.command == 'clear':
        writer.clear_memory()
    
    elif args.command == 'status':
        writer.show_status()

if __name__ == '__main__':
    main()
