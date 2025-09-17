#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 CrewAI Integration for ZombieCoder
Multi-agent system with specialized roles
"""

import os
import json
from typing import Dict, List, Any, Optional
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
import requests

class OllamaTool(BaseTool):
    """Custom tool for Ollama integration"""
    name: str = "Ollama AI Tool"
    description: str = "Use Ollama local AI models for code generation and analysis"
    
    def __init__(self, model: str = "deepseek-coder:latest", base_url: str = "http://localhost:11434"):
        super().__init__()
        self._model = model
        self._base_url = base_url
    
    def _run(self, prompt: str, context: str = "") -> str:
        """Run Ollama model with given prompt"""
        try:
            response = requests.post(
                f"{self._base_url}/api/generate",
                json={
                    "model": self._model,
                    "prompt": f"{context}\n\n{prompt}",
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response from model")
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

class ZombieCoderCrew:
    """ZombieCoder CrewAI integration with specialized agents"""
    
    def __init__(self):
        self.ollama_tool = OllamaTool()
        self.agents = self._create_agents()
        self.crew = None
    
    def _create_agents(self) -> Dict[str, Agent]:
        """Create specialized agents for different roles"""
        
        agents = {}
        
        # Programming Agent (সাহন ভাই)
        agents["programmer"] = Agent(
            role="Senior Programmer",
            goal="Generate high-quality code and solve programming problems",
            backstory="আমি সাহন ভাই, একজন অভিজ্ঞ প্রোগ্রামার। আমি বাংলা এবং ইংরেজি উভয় ভাষায় কোড লিখতে পারি। আমার বিশেষত্ব হলো Python, JavaScript, এবং অন্যান্য প্রোগ্রামিং ভাষায় দক্ষতা।",
            verbose=True,
            allow_delegation=False,
            tools=[self.ollama_tool],
            max_iter=3,
            language="bengali"
        )
        
        # Best Practices Agent (আর্কিটেক্ট)
        agents["architect"] = Agent(
            role="Software Architect",
            goal="Ensure code quality, security, and best practices",
            backstory="আমি একজন সিনিয়র সফটওয়্যার আর্কিটেক্ট। আমি কোডের মান যাচাই করি, নিরাপত্তা সমস্যা চিহ্নিত করি এবং বেস্ট প্র্যাকটিস সুপারিশ করি।",
            verbose=True,
            allow_delegation=False,
            tools=[self.ollama_tool],
            max_iter=3,
            language="bengali"
        )
        
        # Verifier Agent (সত্যতা যাচাইকারী)
        agents["verifier"] = Agent(
            role="Truth Verifier",
            goal="Verify information accuracy and validate assumptions",
            backstory="আমি একজন সত্যতা যাচাইকারী এজেন্ট। আমি তথ্যের নির্ভুলতা নিশ্চিত করি, অনুমান যাচাই করি এবং ঝুঁকি মূল্যায়ন করি।",
            verbose=True,
            allow_delegation=False,
            tools=[self.ollama_tool],
            max_iter=3,
            language="bengali"
        )
        
        # Conversational Agent (মুসকান)
        agents["conversationalist"] = Agent(
            role="Friendly Assistant",
            goal="Provide helpful and friendly assistance to users",
            backstory="আমি মুসকান, একজন বন্ধুত্বপূর্ণ AI সহকারী। আমি ব্যবহারকারীদের সাহায্য করি, প্রশ্নের উত্তর দিই এবং প্রাকৃতিক কথোপকথন করি।",
            verbose=True,
            allow_delegation=False,
            tools=[self.ollama_tool],
            max_iter=3,
            language="bengali"
        )
        
        # Operations Agent (হান্টার)
        agents["operator"] = Agent(
            role="System Operator",
            goal="Handle system operations and automation tasks",
            backstory="আমি হান্টার, একজন দক্ষ সিস্টেম অপারেটর। আমি স্বয়ংক্রিয় কাজ পরিচালনা করি, সিস্টেম মনিটর করি এবং সমস্যা সমাধান করি।",
            verbose=True,
            allow_delegation=False,
            tools=[self.ollama_tool],
            max_iter=3,
            language="bengali"
        )
        
        return agents
    
    def create_programming_task(self, task_description: str, language: str = "Python") -> Task:
        """Create a programming task"""
        return Task(
            description=f"""
            কাজ: {task_description}
            প্রোগ্রামিং ভাষা: {language}
            
            আপনার কাজ:
            1. প্রয়োজনীয় কোড লিখুন
            2. কোড ব্যাখ্যা করুন
            3. ব্যবহারের উদাহরণ দিন
            4. সম্ভাব্য সমস্যা এবং সমাধান উল্লেখ করুন
            
            উত্তর বাংলা ভাষায় দিন।
            """,
            agent=self.agents["programmer"],
            expected_output="কোড ব্লক + বিস্তারিত ব্যাখ্যা + ব্যবহারের উদাহরণ"
        )
    
    def create_review_task(self, code: str, language: str = "Python") -> Task:
        """Create a code review task"""
        return Task(
            description=f"""
            কোড রিভিউ করুন:
            
            কোড:
            ```
            {code}
            ```
            
            প্রোগ্রামিং ভাষা: {language}
            
            আপনার মূল্যায়ন:
            1. কোডের মান যাচাই করুন
            2. নিরাপত্তা সমস্যা চিহ্নিত করুন
            3. পারফরমেন্স উন্নতির সুপারিশ দিন
            4. বেস্ট প্র্যাকটিস অনুসরণ করুন
            5. উন্নতির পরামর্শ দিন
            
            উত্তর বাংলা ভাষায় দিন।
            """,
            agent=self.agents["architect"],
            expected_output="মূল্যায়ন রিপোর্ট + উন্নতির সুপারিশ"
        )
    
    def create_verification_task(self, information: str, context: str = "") -> Task:
        """Create a verification task"""
        return Task(
            description=f"""
            তথ্য যাচাই করুন:
            
            তথ্য: {information}
            প্রসঙ্গ: {context}
            
            আপনার যাচাইকরণ:
            1. তথ্যের সত্যতা নিশ্চিত করুন
            2. সম্ভাব্য সমস্যা চিহ্নিত করুন
            3. ঝুঁকি মূল্যায়ন করুন
            4. বিকল্প সমাধান প্রস্তাব করুন
            
            উত্তর বাংলা ভাষায় দিন।
            """,
            agent=self.agents["verifier"],
            expected_output="যাচাইকরণ রিপোর্ট + ঝুঁকি মূল্যায়ন"
        )
    
    def create_conversation_task(self, question: str, context: str = "") -> Task:
        """Create a conversation task"""
        return Task(
            description=f"""
            ব্যবহারকারীর প্রশ্নের উত্তর দিন:
            
            প্রশ্ন: {question}
            প্রসঙ্গ: {context}
            
            আপনার উত্তর:
            1. প্রশ্নের সরাসরি উত্তর দিন
            2. প্রয়োজন হলে আরও তথ্য দিন
            3. উদাহরণ বা ব্যাখ্যা দিন
            4. অনুসরণ প্রশ্ন প্রস্তাব করুন
            
            বন্ধুত্বপূর্ণ এবং সহায়ক হন। বাংলা ভাষায় উত্তর দিন।
            """,
            agent=self.agents["conversationalist"],
            expected_output="প্রাকৃতিক এবং সহায়ক উত্তর"
        )
    
    def create_operation_task(self, operation: str, system_info: str = "") -> Task:
        """Create an operations task"""
        return Task(
            description=f"""
            সিস্টেম অপারেশন পরিচালনা করুন:
            
            অপারেশন: {operation}
            সিস্টেম তথ্য: {system_info}
            
            আপনার কাজ:
            1. অপারেশনের পরিকল্পনা করুন
            2. প্রয়োজনীয় স্টেপ নির্ধারণ করুন
            3. সম্ভাব্য সমস্যা চিহ্নিত করুন
            4. স্বয়ংক্রিয় সমাধান প্রস্তাব করুন
            
            উত্তর বাংলা ভাষায় দিন।
            """,
            agent=self.agents["operator"],
            expected_output="অপারেশন পরিকল্পনা + স্বয়ংক্রিয় সমাধান"
        )
    
    def execute_task(self, task: Task) -> str:
        """Execute a single task"""
        try:
            crew = Crew(
                agents=[task.agent],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            return str(result)
            
        except Exception as e:
            return f"Error executing task: {str(e)}"
    
    def execute_multi_agent_workflow(self, tasks: List[Task]) -> List[str]:
        """Execute multiple tasks with different agents"""
        try:
            # Get unique agents from tasks
            agents = list(set(task.agent for task in tasks))
            
            crew = Crew(
                agents=agents,
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            return str(result)
            
        except Exception as e:
            return f"Error executing multi-agent workflow: {str(e)}"
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "total_agents": len(self.agents),
            "agents": {
                name: {
                    "role": agent.role,
                    "goal": agent.goal,
                    "language": agent.language,
                    "tools": [tool.name for tool in agent.tools] if hasattr(agent, 'tools') else []
                }
                for name, agent in self.agents.items()
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize ZombieCoder Crew
    zombie_crew = ZombieCoderCrew()
    
    print("🤖 ZombieCoder CrewAI Integration Test")
    print("=" * 50)
    
    # Test 1: Programming Task
    print("\n1. Testing Programming Agent...")
    programming_task = zombie_crew.create_programming_task(
        "একটি REST API তৈরি করুন যা CSV ফাইল আপলোড এবং প্রসেস করতে পারে",
        "Python"
    )
    
    result1 = zombie_crew.execute_task(programming_task)
    print(f"✅ Programming Result: {result1[:200]}...")
    
    # Test 2: Code Review Task
    print("\n2. Testing Code Review Agent...")
    sample_code = """
def process_csv(file_path):
    import pandas as pd
    df = pd.read_csv(file_path)
    return df.head()
    """
    
    review_task = zombie_crew.create_review_task(sample_code, "Python")
    result2 = zombie_crew.execute_task(review_task)
    print(f"✅ Review Result: {result2[:200]}...")
    
    # Test 3: Verification Task
    print("\n3. Testing Verification Agent...")
    verification_task = zombie_crew.create_verification_task(
        "Pandas CSV processing is thread-safe",
        "Multi-threaded application context"
    )
    result3 = zombie_crew.execute_task(verification_task)
    print(f"✅ Verification Result: {result3[:200]}...")
    
    # Test 4: Conversation Task
    print("\n4. Testing Conversational Agent...")
    conversation_task = zombie_crew.create_conversation_task(
        "Python এ কিভাবে async/await ব্যবহার করব?",
        "Web development context"
    )
    result4 = zombie_crew.execute_task(conversation_task)
    print(f"✅ Conversation Result: {result4[:200]}...")
    
    # Test 5: Operation Task
    print("\n5. Testing Operations Agent...")
    operation_task = zombie_crew.create_operation_task(
        "সিস্টেম পারফরমেন্স মনিটরিং সেটআপ করুন",
        "Linux server with Python applications"
    )
    result5 = zombie_crew.execute_task(operation_task)
    print(f"✅ Operation Result: {result5[:200]}...")
    
    # Get agent status
    print("\n6. Agent Status:")
    status = zombie_crew.get_agent_status()
    print(f"Total Agents: {status['total_agents']}")
    for name, info in status['agents'].items():
        print(f"- {name}: {info['role']} ({info['language']})")
    
    print("\n🎉 All tests completed successfully!")
