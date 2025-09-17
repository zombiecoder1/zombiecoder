#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👨‍💻 Friendly Programmer Agent for ZombieCoder
A skilled and friendly programming assistant with individual memory
"""

import os
import json
import time
import logging
import yaml
from typing import Dict, Any, List, Optional
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

logger = logging.getLogger(__name__)

class FriendlyProgrammerAgent:
    """Friendly and skilled programmer agent with individual memory"""
    
    def __init__(self, name: str = "রাকিব ভাই", agent_id: str = "friendly_programmer"):
        self.name = name
        self.agent_id = agent_id
        self.memory_file = f"memory/{agent_id}_memory.yaml"
        
        # Agent personality and capabilities
        self.personality = {
            "name": name,
            "role": "Senior Programming Mentor",
            "style": "friendly_bengali_english",
            "approach": "patient_teacher",
            "language_preference": "বাংলা + English mixed",
            "greeting": "ভাই, কেমন আছেন? আমি আপনার প্রোগ্রামিং সহায়ক রাকিব ভাই।"
        }
        
        # Programming expertise
        self.expertise = {
            "languages": ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript"],
            "frameworks": ["Django", "Flask", "FastAPI", "React", "Vue.js", "Express.js"],
            "databases": ["PostgreSQL", "MySQL", "MongoDB", "SQLite", "Redis"],
            "tools": ["Git", "Docker", "AWS", "Linux", "VSCode", "IntelliJ"],
            "specialties": ["Web Development", "API Design", "Database Design", "Code Review", "Architecture"]
        }
        
        # Initialize memory
        self.memory = self.load_memory()
        
        # Conversation patterns
        self.conversation_patterns = {
            "greeting_responses": [
                "ভাই, কেমন আছেন? আজকে কি প্রোগ্রামিং নিয়ে কাজ করবেন?",
                "আরে ভাই! আজকে কি নতুন কিছু শিখতে চান?",
                "হ্যালো! আমি আপনার প্রোগ্রামিং সহায়ক রাকিব ভাই। কি সাহায্য করতে পারি?"
            ],
            "encouragement": [
                "ভাই, আপনি ভালো করছেন! একটু চেষ্টা করলেই পারবেন।",
                "দারুণ! আপনি খুব দ্রুত শিখছেন।",
                "এটা একটা ভালো প্রশ্ন! আমি খুশি যে আপনি জানতে চান।"
            ],
            "error_handling": [
                "ভাই, ভুল হওয়া স্বাভাবিক। আমি দেখিয়ে দিচ্ছি কিভাবে ঠিক করতে হবে।",
                "চিন্তা করবেন না! এই error টা খুব common। আমি সহজ করে বুঝিয়ে দিচ্ছি।",
                "এটা একটা learning opportunity! আমি step by step explain করছি।"
            ]
        }
    
    def load_memory(self) -> Dict[str, Any]:
        """Load individual memory from YAML file"""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    memory = yaml.safe_load(f) or {}
            else:
                memory = {
                    "user_interactions": [],
                    "learned_preferences": {},
                    "code_examples": {},
                    "conversation_history": [],
                    "user_progress": {},
                    "created_at": datetime.now().isoformat()
                }
                self.save_memory(memory)
            
            return memory
            
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            return {"user_interactions": [], "learned_preferences": {}, "code_examples": {}}
    
    def save_memory(self, memory: Dict[str, Any] = None) -> bool:
        """Save memory to YAML file"""
        try:
            if memory is None:
                memory = self.memory
            
            memory["last_updated"] = datetime.now().isoformat()
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                yaml.dump(memory, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
            return False
    
    def add_interaction(self, user_input: str, response: str, context: Dict[str, Any] = None):
        """Add interaction to memory"""
        if context is None:
            context = {}
        
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": response,
            "context": context,
            "agent_id": self.agent_id
        }
        
        self.memory["user_interactions"].append(interaction)
        
        # Keep only last 100 interactions
        if len(self.memory["user_interactions"]) > 100:
            self.memory["user_interactions"] = self.memory["user_interactions"][-100:]
        
        self.save_memory()
    
    def get_user_preferences(self, user_id: str = "default") -> Dict[str, Any]:
        """Get learned user preferences"""
        return self.memory["learned_preferences"].get(user_id, {
            "preferred_language": "python",
            "skill_level": "intermediate",
            "learning_style": "step_by_step",
            "communication_style": "friendly_bengali"
        })
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user preferences"""
        if "learned_preferences" not in self.memory:
            self.memory["learned_preferences"] = {}
        
        if user_id not in self.memory["learned_preferences"]:
            self.memory["learned_preferences"][user_id] = {}
        
        self.memory["learned_preferences"][user_id].update(preferences)
        self.save_memory()
    
    def generate_friendly_response(self, message: str, context: Dict[str, Any] = None) -> str:
        """Generate a friendly and helpful response"""
        if context is None:
            context = {}
        
        # Analyze message type
        message_lower = message.lower()
        
        # Greeting detection
        if any(greeting in message_lower for greeting in ["hello", "hi", "হ্যালো", "আসসালামু", "কেমন"]):
            return self._handle_greeting(context)
        
        # Programming question detection
        if any(keyword in message_lower for keyword in ["code", "function", "class", "error", "bug", "কোড", "ফাংশন"]):
            return self._handle_programming_question(message, context)
        
        # Learning request
        if any(keyword in message_lower for keyword in ["learn", "teach", "explain", "শিখতে", "বুঝতে"]):
            return self._handle_learning_request(message, context)
        
        # General conversation
        return self._handle_general_conversation(message, context)
    
    def _handle_greeting(self, context: Dict[str, Any]) -> str:
        """Handle greeting messages"""
        import random
        greeting = random.choice(self.conversation_patterns["greeting_responses"])
        
        # Add personal touch based on previous interactions
        recent_interactions = self.memory["user_interactions"][-5:] if self.memory["user_interactions"] else []
        if recent_interactions:
            greeting += f" গতবার আমরা {len(recent_interactions)} টা topic নিয়ে আলোচনা করেছিলাম।"
        
        return greeting
    
    def _handle_programming_question(self, message: str, context: Dict[str, Any]) -> str:
        """Handle programming-related questions"""
        response = "ভাই, ভালো প্রশ্ন! আমি দেখাচ্ছি কিভাবে সমাধান করতে হবে।\n\n"
        
        # Analyze the programming language
        if "python" in message.lower():
            response += self._generate_python_example(message, context)
        elif "javascript" in message.lower() or "js" in message.lower():
            response += self._generate_javascript_example(message, context)
        elif "java" in message.lower():
            response += self._generate_java_example(message, context)
        else:
            response += self._generate_general_programming_advice(message, context)
        
        return response
    
    def _handle_learning_request(self, message: str, context: Dict[str, Any]) -> str:
        """Handle learning requests"""
        response = "দারুণ! আমি step by step শিখিয়ে দিচ্ছি।\n\n"
        
        # Determine learning topic
        if "python" in message.lower():
            response += self._get_python_learning_plan()
        elif "web" in message.lower() or "website" in message.lower():
            response += self._get_web_development_plan()
        elif "database" in message.lower() or "db" in message.lower():
            response += self._get_database_learning_plan()
        else:
            response += self._get_general_learning_plan()
        
        return response
    
    def _handle_general_conversation(self, message: str, context: Dict[str, Any]) -> str:
        """Handle general conversation"""
        import random
        encouragement = random.choice(self.conversation_patterns["encouragement"])
        
        response = f"{encouragement}\n\n"
        response += "আপনি যদি প্রোগ্রামিং নিয়ে কোন প্রশ্ন করেন, আমি খুশি হয়ে সাহায্য করব। "
        response += "আপনি কি Python, JavaScript, বা অন্য কোন language নিয়ে জানতে চান?"
        
        return response
    
    def _generate_python_example(self, message: str, context: Dict[str, Any]) -> str:
        """Generate Python code examples"""
        examples = {
            "function": """
```python
def greet(name):
    \"\"\"একটি সাধারণ greeting function\"\"\"
    return f"Hello {name}, কেমন আছেন?"

# ব্যবহার:
result = greet("সাহন")
print(result)
```""",
            "class": """
```python
class Student:
    \"\"\"একটি Student class example\"\"\"
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"আমার নাম {self.name}, আমার বয়স {self.age} বছর"

# ব্যবহার:
student = Student("রাকিব", 25)
print(student.introduce())
```""",
            "error_handling": """
```python
def safe_divide(a, b):
    \"\"\"Error handling সহ division function\"\"\"
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: শূন্য দিয়ে ভাগ করা যায় না!"
    except TypeError:
        return "Error: সংখ্যা দিয়ে ভাগ করুন!"

# ব্যবহার:
print(safe_divide(10, 2))  # 5.0
print(safe_divide(10, 0))  # Error message
```"""
        }
        
        # Return appropriate example based on message content
        if "function" in message.lower():
            return examples["function"]
        elif "class" in message.lower():
            return examples["class"]
        elif "error" in message.lower() or "exception" in message.lower():
            return examples["error_handling"]
        else:
            return examples["function"]  # Default
    
    def _generate_javascript_example(self, message: str, context: Dict[str, Any]) -> str:
        """Generate JavaScript code examples"""
        return """
```javascript
// একটি JavaScript function example
function greetUser(name) {
    return `Hello ${name}, কেমন আছেন?`;
}

// Arrow function
const add = (a, b) => a + b;

// Class example
class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    introduce() {
        return `আমার নাম ${this.name}`;
    }
}

// ব্যবহার:
console.log(greetUser("সাহন"));
console.log(add(5, 3));
const person = new Person("রাকিব", 25);
console.log(person.introduce());
```"""
    
    def _generate_java_example(self, message: str, context: Dict[str, Any]) -> str:
        """Generate Java code examples"""
        return """
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello World!");
        
        // Function call
        String greeting = greetUser("সাহন");
        System.out.println(greeting);
    }
    
    public static String greetUser(String name) {
        return "Hello " + name + ", কেমন আছেন?";
    }
}
```"""
    
    def _generate_general_programming_advice(self, message: str, context: Dict[str, Any]) -> str:
        """Generate general programming advice"""
        return """
ভাই, প্রোগ্রামিং এ ভালো হতে চাইলে এই steps follow করুন:

1. **Practice regularly**: প্রতিদিন কমপক্ষে 1 ঘন্টা coding practice করুন
2. **Read documentation**: Official documentation পড়ুন
3. **Build projects**: ছোট ছোট project তৈরি করুন
4. **Code review**: অন্যের code দেখুন এবং নিজের code review করুন
5. **Join community**: Programming community তে join করুন

আপনি কোন specific language বা topic নিয়ে জানতে চান?
"""
    
    def _get_python_learning_plan(self) -> str:
        """Get Python learning plan"""
        return """
**Python Learning Plan:**

**Beginner Level:**
- Variables এবং Data Types
- Conditional Statements (if, elif, else)
- Loops (for, while)
- Functions

**Intermediate Level:**
- Lists, Tuples, Dictionaries
- File Handling
- Exception Handling
- Modules এবং Packages

**Advanced Level:**
- Object-Oriented Programming
- Decorators
- Generators
- Async Programming

আপনি কোন level থেকে শুরু করতে চান?
"""
    
    def _get_web_development_plan(self) -> str:
        """Get web development learning plan"""
        return """
**Web Development Learning Plan:**

**Frontend:**
- HTML (Structure)
- CSS (Styling)
- JavaScript (Functionality)
- React/Vue.js (Frameworks)

**Backend:**
- Python (Django/Flask)
- Node.js (Express)
- Database (PostgreSQL/MySQL)
- API Development

**Tools:**
- Git (Version Control)
- Docker (Containerization)
- AWS/Heroku (Deployment)

আপনি Frontend নাকি Backend দিয়ে শুরু করতে চান?
"""
    
    def _get_database_learning_plan(self) -> str:
        """Get database learning plan"""
        return """
**Database Learning Plan:**

**Fundamentals:**
- SQL Basics (SELECT, INSERT, UPDATE, DELETE)
- Database Design
- Relationships (One-to-One, One-to-Many, Many-to-Many)
- Indexing

**Advanced Topics:**
- Query Optimization
- Transactions
- Stored Procedures
- Database Security

**Popular Databases:**
- PostgreSQL (Open source, powerful)
- MySQL (Widely used)
- MongoDB (NoSQL)
- SQLite (Lightweight)

আপনি SQL দিয়ে শুরু করতে চান?
"""
    
    def _get_general_learning_plan(self) -> str:
        """Get general learning plan"""
        return """
**Programming Learning Path:**

**1. Choose a Language:**
- Python (Beginner friendly)
- JavaScript (Web development)
- Java (Enterprise applications)
- C++ (System programming)

**2. Learn Fundamentals:**
- Variables, Data Types
- Control Structures
- Functions
- Data Structures

**3. Practice:**
- Coding challenges (LeetCode, HackerRank)
- Build small projects
- Contribute to open source

**4. Specialize:**
- Web Development
- Mobile Development
- Data Science
- Machine Learning

আপনি কোন direction এ যেতে চান?
"""
    
    def process_message(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user message and return response"""
        if context is None:
            context = {}
        
        # Generate friendly response
        response = self.generate_friendly_response(message, context)
        
        # Add interaction to memory
        self.add_interaction(message, response, context)
        
        return {
            "agent": self.name,
            "response": response,
            "capability": "friendly_programming",
            "source": "local",
            "timestamp": time.time(),
            "memory_updated": True,
            "agent_id": self.agent_id
        }

# Global instance
friendly_programmer = FriendlyProgrammerAgent()

if __name__ == "__main__":
    # Test the agent
    test_messages = [
        "হ্যালো রাকিব ভাই!",
        "Python এ কিভাবে function লিখব?",
        "JavaScript শিখতে চাই",
        "Database design কিভাবে করব?"
    ]
    
    print(f"🤖 Testing {friendly_programmer.name}")
    print("=" * 50)
    
    for message in test_messages:
        print(f"\nUser: {message}")
        response = friendly_programmer.process_message(message)
        print(f"Agent: {response['response']}")
        print("-" * 30)
