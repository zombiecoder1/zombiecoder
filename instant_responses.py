#!/usr/bin/env python3
"""
⚡ Instant ZombieCoder Responses - Fast Fallback System
"""

import json
import time
from typing import Dict, Any

class InstantZombieCoder:
    """Instant response system for ZombieCoder"""
    
    def __init__(self):
        self.name = "ZombieCoder Agent (সাহন ভাই)"
        self.responses = {
            "csv": {
                "bengali": """
ভাই, Python এ CSV ফাইল পড়ার সহজ উপায়:

```python
import pandas as pd

# CSV ফাইল পড়া
df = pd.read_csv('your_file.csv')

# প্রথম কয়েকটি সারি দেখুন
print(df.head())

# CSV থেকে নির্দিষ্ট কলাম পড়া
df = pd.read_csv('file.csv', usecols=['name', 'age'])

# CSV পড়ার সময় encoding specify করুন
df = pd.read_csv('file.csv', encoding='utf-8')
```

**ব্যাখ্যা:**
- `pandas` library সবচেয়ে সহজ
- `read_csv()` function ব্যবহার করুন
- `encoding` specify করুন Bengali text এর জন্য
- `usecols` দিয়ে নির্দিষ্ট কলাম পড়ুন

**উদাহরণ:**
```python
# Student data পড়া
students = pd.read_csv('students.csv')
print(students.columns)  # কলামের নাম দেখুন
print(students.shape)    # সারি এবং কলাম সংখ্যা
```

এইভাবে আপনি সহজেই CSV ফাইল handle করতে পারবেন!
""",
                "keywords": ["csv", "ফাইল", "পড়া", "data", "pandas"]
            },
            "async": {
                "bengali": """
ভাই, JavaScript এ async/await এর ব্যবহার:

```javascript
// Basic async/await
async function fetchData() {
    try {
        const response = await fetch('https://api.example.com/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

// Multiple async calls
async function loadMultipleData() {
    const [users, posts, comments] = await Promise.all([
        fetch('/api/users').then(r => r.json()),
        fetch('/api/posts').then(r => r.json()),
        fetch('/api/comments').then(r => r.json())
    ]);
    
    return { users, posts, comments };
}

// Real example
async function getUserProfile(userId) {
    try {
        const user = await fetch(`/api/users/${userId}`).then(r => r.json());
        const posts = await fetch(`/api/users/${userId}/posts`).then(r => r.json());
        
        return {
            ...user,
            posts: posts
        };
    } catch (error) {
        console.error('Failed to load profile:', error);
        throw error;
    }
}
```

**মূল নিয়ম:**
1. `async` function এর আগে লিখুন
2. `await` দিয়ে promise wait করুন
3. `try/catch` দিয়ে error handle করুন
4. `Promise.all()` দিয়ে multiple calls করুন

**ব্যবহার:**
```javascript
// Function call
fetchData().then(data => console.log(data));

// বা
(async () => {
    const data = await fetchData();
    console.log(data);
})();
```

এইভাবে async/await দিয়ে clean code লিখতে পারবেন!
""",
                "keywords": ["async", "await", "javascript", "promise", "fetch"]
            },
            "monitoring": {
                "bengali": """
ভাই, সিস্টেম পারফরমেন্স মনিটর করার উপায়:

**1. System Resources:**
```python
import psutil
import time

def monitor_system():
    # CPU Usage
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_percent}%")
    
    # Memory Usage
    memory = psutil.virtual_memory()
    print(f"Memory: {memory.percent}% used")
    print(f"Available: {memory.available / (1024**3):.2f} GB")
    
    # Disk Usage
    disk = psutil.disk_usage('/')
    print(f"Disk: {disk.percent}% used")
    print(f"Free: {disk.free / (1024**3):.2f} GB")
    
    # Network
    network = psutil.net_io_counters()
    print(f"Bytes Sent: {network.bytes_sent}")
    print(f"Bytes Received: {network.bytes_recv}")

# Continuous monitoring
while True:
    monitor_system()
    time.sleep(5)
```

**2. Application Monitoring:**
```python
import logging
from datetime import datetime

# Performance logging
def log_performance(func_name, execution_time, memory_used):
    logging.info(f"{func_name}: {execution_time:.2f}s, {memory_used}MB")

# Memory tracking
import tracemalloc

def track_memory():
    tracemalloc.start()
    # Your code here
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")
```

**3. Real-time Dashboard:**
```python
from flask import Flask, render_template
import psutil
import json

app = Flask(__name__)

@app.route('/system-status')
def system_status():
    status = {
        'cpu': psutil.cpu_percent(),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'timestamp': time.time()
    }
    return json.dumps(status)
```

**Tools:**
- `htop` - Real-time system monitor
- `iostat` - I/O statistics
- `netstat` - Network connections
- `top` - Process monitoring

এইভাবে আপনি সিস্টেমের সব কিছু monitor করতে পারবেন!
""",
                "keywords": ["monitor", "performance", "সিস্টেম", "resources", "cpu"]
            }
        }
    
    def get_instant_response(self, message: str) -> Dict[str, Any]:
        """Get instant response based on keywords"""
        
        message_lower = message.lower()
        
        # Check for CSV related questions
        if any(keyword in message_lower for keyword in ["csv", "ফাইল", "পড়া", "data", "pandas"]):
            return {
                "response": self.responses["csv"]["bengali"],
                "agent": self.name,
                "capability": "coding",
                "source": "instant_fallback",
                "timestamp": time.time()
            }
        
        # Check for async/await questions
        elif any(keyword in message_lower for keyword in ["async", "await", "javascript", "promise", "fetch"]):
            return {
                "response": self.responses["async"]["bengali"],
                "agent": self.name,
                "capability": "coding",
                "source": "instant_fallback",
                "timestamp": time.time()
            }
        
        # Check for monitoring questions
        elif any(keyword in message_lower for keyword in ["monitor", "performance", "সিস্টেম", "resources", "cpu"]):
            return {
                "response": self.responses["monitoring"]["bengali"],
                "agent": self.name,
                "capability": "system_ops",
                "source": "instant_fallback",
                "timestamp": time.time()
            }
        
        # Default response
        else:
            return {
                "response": f"""ভাই, আমি এখনই আপনার প্রশ্নের উত্তর দিচ্ছি:

**আপনার প্রশ্ন:** {message}

**সাধারণ উত্তর:**
আমি ZombieCoder AI Agent (সাহন ভাই)। আমি আপনাকে সাহায্য করতে পারি:

🔧 **কোডিং**: Python, JavaScript, Java, C++, Go
🐛 **ডিবাগিং**: Error fixing, code review
🏗️ **আর্কিটেকচার**: System design, best practices
🔒 **সিকিউরিটি**: Security implementation
⚡ **পারফরমেন্স**: Optimization, monitoring
🌐 **API**: REST API, GraphQL
📊 **ডেটাবেজ**: SQL, NoSQL, data processing

**আরও নির্দিষ্ট প্রশ্ন করুন:**
- "Python এ CSV ফাইল কিভাবে পড়া যায়?"
- "JavaScript এ async/await কিভাবে ব্যবহার করব?"
- "সিস্টেম পারফরমেন্স কিভাবে monitor করব?"

আমি আপনার সব প্রশ্নের উত্তর দেব! 🚀""",
                "agent": self.name,
                "capability": "general",
                "source": "instant_fallback",
                "timestamp": time.time()
            }

# Global instance
instant_zombiecoder = InstantZombieCoder()

def get_fast_response(message: str) -> Dict[str, Any]:
    """Get fast response from instant system"""
    return instant_zombiecoder.get_instant_response(message)

if __name__ == "__main__":
    # Test the instant response system
    test_questions = [
        "Python এ CSV ফাইল কিভাবে পড়া যায়?",
        "JavaScript এ async/await কিভাবে ব্যবহার করব?",
        "সিস্টেম পারফরমেন্স কিভাবে monitor করব?",
        "আপনি কি করতে পারেন?"
    ]
    
    print("⚡ Testing Instant ZombieCoder Responses")
    print("=" * 50)
    
    for question in test_questions:
        print(f"\n📝 Question: {question}")
        start_time = time.time()
        response = get_fast_response(question)
        end_time = time.time()
        
        print(f"⚡ Response Time: {(end_time - start_time)*1000:.2f}ms")
        print(f"🤖 Agent: {response['agent']}")
        print(f"🔧 Capability: {response['capability']}")
        print(f"📄 Response: {response['response'][:100]}...")
        print("-" * 30)
