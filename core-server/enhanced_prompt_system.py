#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Enhanced Prompt Scoping System
Industry best practices for structured prompt management
"""

import os
import json
import yaml
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AgentType(Enum):
    PROGRAMMING = "programming"
    BEST_PRACTICES = "best_practices"
    VERIFIER = "verifier"
    CONVERSATIONAL = "conversational"
    OPS = "ops"

@dataclass
class PromptTemplate:
    """Structured prompt template"""
    name: str
    agent_type: AgentType
    description: str
    system_prompt: str
    user_prompt_template: str
    expected_output_format: str
    context_requirements: List[str]
    validation_rules: List[str]

class PromptScopingSystem:
    """Enhanced prompt scoping system following industry best practices"""
    
    def __init__(self, config_path: str = "config/prompt_templates.yaml"):
        self.config_path = config_path
        self.templates: Dict[str, PromptTemplate] = {}
        self.load_templates()
    
    def load_templates(self):
        """Load prompt templates from configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                for template_data in config.get('templates', []):
                    template = PromptTemplate(
                        name=template_data['name'],
                        agent_type=AgentType(template_data['agent_type']),
                        description=template_data['description'],
                        system_prompt=template_data['system_prompt'],
                        user_prompt_template=template_data['user_prompt_template'],
                        expected_output_format=template_data['expected_output_format'],
                        context_requirements=template_data['context_requirements'],
                        validation_rules=template_data['validation_rules']
                    )
                    self.templates[template.name] = template
    
    def get_prompt(self, template_name: str, context: Dict[str, Any]) -> Dict[str, str]:
        """Get structured prompt for specific template and context"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.templates[template_name]
        
        # Validate context requirements
        self._validate_context(template, context)
        
        # Format prompts
        system_prompt = template.system_prompt
        user_prompt = template.user_prompt_template.format(**context)
        
        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "expected_output_format": template.expected_output_format,
            "validation_rules": template.validation_rules
        }
    
    def _validate_context(self, template: PromptTemplate, context: Dict[str, Any]):
        """Validate that context meets requirements"""
        for requirement in template.context_requirements:
            if requirement not in context:
                raise ValueError(f"Missing required context: {requirement}")
    
    def create_dynamic_prompt(self, agent_type: AgentType, task: str, context: Dict[str, Any]) -> str:
        """Create dynamic prompt based on agent type and task"""
        
        base_prompts = {
            AgentType.PROGRAMMING: """
আপনি একজন অভিজ্ঞ প্রোগ্রামার এবং কোডিং বিশেষজ্ঞ। আপনার কাজ:

1. **সত্য কথা বলুন**: শুধুমাত্র আপনার জ্ঞানের ভিত্তিতে উত্তর দিন
2. **স্পষ্ট হন**: কোডের প্রতিটি অংশ ব্যাখ্যা করুন
3. **বেস্ট প্র্যাকটিস**: ইন্ডাস্ট্রি স্ট্যান্ডার্ড অনুসরণ করুন
4. **বাংলা ভাষা**: ব্যবহারকারীর সাথে বাংলায় কথা বলুন

**টাস্ক**: {task}
**প্রসঙ্গ**: {context}

আপনার উত্তর:
""",
            AgentType.BEST_PRACTICES: """
আপনি একজন সিনিয়র সফটওয়্যার আর্কিটেক্ট। আপনার কাজ:

1. **গুণমান নিশ্চিত করুন**: কোডের মান যাচাই করুন
2. **নিরাপত্তা**: সিকিউরিটি সমস্যা চিহ্নিত করুন
3. **পারফরমেন্স**: অপটিমাইজেশন সুপারিশ করুন
4. **স্কেলেবিলিটি**: ভবিষ্যতের জন্য প্রস্তুত করুন

**টাস্ক**: {task}
**প্রসঙ্গ**: {context}

আপনার মূল্যায়ন:
""",
            AgentType.VERIFIER: """
আপনি একজন সত্যতা যাচাইকারী এজেন্ট। আপনার কাজ:

1. **প্রমাণ যাচাই**: তথ্যের সত্যতা নিশ্চিত করুন
2. **অনুমান পরীক্ষা**: ধারণাগুলো যাচাই করুন
3. **ঝুঁকি মূল্যায়ন**: সম্ভাব্য সমস্যা চিহ্নিত করুন
4. **সুপারিশ**: উন্নতির পরামর্শ দিন

**টাস্ক**: {task}
**প্রসঙ্গ**: {context}

আপনার যাচাইকরণ:
""",
            AgentType.CONVERSATIONAL: """
আপনি একজন বন্ধুত্বপূর্ণ AI সহকারী। আপনার কাজ:

1. **বন্ধুত্বপূর্ণ**: আন্তরিক এবং সাহায্যকারী হন
2. **স্পষ্ট**: জটিল বিষয় সহজ করে ব্যাখ্যা করুন
3. **প্রশ্ন করুন**: প্রয়োজন হলে আরও তথ্য চাইুন
4. **বাংলা ভাষা**: প্রাকৃতিক বাংলায় কথা বলুন

**টাস্ক**: {task}
**প্রসঙ্গ**: {context}

আপনার উত্তর:
""",
            AgentType.OPS: """
আপনি একজন সিস্টেম অপারেশন বিশেষজ্ঞ। আপনার কাজ:

1. **স্বয়ংক্রিয়করণ**: কাজগুলো স্বয়ংক্রিয় করুন
2. **মনিটরিং**: সিস্টেমের অবস্থা পর্যবেক্ষণ করুন
3. **সমস্যা সমাধান**: এরর এবং সমস্যা ঠিক করুন
4. **দক্ষতা**: প্রসেস অপটিমাইজ করুন

**টাস্ক**: {task}
**প্রসঙ্গ**: {context}

আপনার সমাধান:
"""
        }
        
        base_prompt = base_prompts.get(agent_type, base_prompts[AgentType.CONVERSATIONAL])
        
        return base_prompt.format(
            task=task,
            context=json.dumps(context, ensure_ascii=False, indent=2)
        )
    
    def validate_response(self, template_name: str, response: str) -> Dict[str, Any]:
        """Validate response against template rules"""
        if template_name not in self.templates:
            return {"valid": False, "error": "Template not found"}
        
        template = self.templates[template_name]
        validation_results = []
        
        for rule in template.validation_rules:
            if rule == "contains_code" and "```" not in response:
                validation_results.append({"rule": rule, "passed": False, "message": "Response should contain code blocks"})
            elif rule == "structured_format" and not self._is_structured(response):
                validation_results.append({"rule": rule, "passed": False, "message": "Response should be well-structured"})
            elif rule == "bengali_language" and not self._contains_bengali(response):
                validation_results.append({"rule": rule, "passed": False, "message": "Response should contain Bengali text"})
            else:
                validation_results.append({"rule": rule, "passed": True, "message": "Rule passed"})
        
        all_passed = all(result["passed"] for result in validation_results)
        
        return {
            "valid": all_passed,
            "validation_results": validation_results,
            "template": template_name
        }
    
    def _is_structured(self, text: str) -> bool:
        """Check if text is well-structured"""
        structure_indicators = ["1.", "2.", "**", "###", "-", "*"]
        return any(indicator in text for indicator in structure_indicators)
    
    def _contains_bengali(self, text: str) -> bool:
        """Check if text contains Bengali characters"""
        bengali_chars = set("অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহািীুূৃেৈোৌ্ৎংঃ")
        return any(char in bengali_chars for char in text)
    
    def get_available_templates(self) -> List[Dict[str, Any]]:
        """Get list of available templates"""
        return [
            {
                "name": template.name,
                "agent_type": template.agent_type.value,
                "description": template.description,
                "context_requirements": template.context_requirements
            }
            for template in self.templates.values()
        ]

def create_default_config():
    """Create default prompt templates configuration"""
    config = {
        "templates": [
            {
                "name": "code_generation",
                "agent_type": "programming",
                "description": "Generate code snippets and functions",
                "system_prompt": "আপনি একজন অভিজ্ঞ প্রোগ্রামার। কোড জেনারেট করুন এবং ব্যাখ্যা করুন।",
                "user_prompt_template": "এই কাজের জন্য কোড লিখুন: {task}\nপ্রোগ্রামিং ভাষা: {language}\nপ্রয়োজনীয় লাইব্রেরি: {libraries}",
                "expected_output_format": "কোড ব্লক + ব্যাখ্যা",
                "context_requirements": ["task", "language"],
                "validation_rules": ["contains_code", "structured_format", "bengali_language"]
            },
            {
                "name": "code_review",
                "agent_type": "best_practices",
                "description": "Review code for best practices and security",
                "system_prompt": "আপনি একজন সিনিয়র কোড রিভিউয়ার। কোডের মান যাচাই করুন।",
                "user_prompt_template": "এই কোড রিভিউ করুন: {code}\nপ্রোগ্রামিং ভাষা: {language}\nফোকাস: {focus_areas}",
                "expected_output_format": "মূল্যায়ন + সুপারিশ",
                "context_requirements": ["code", "language"],
                "validation_rules": ["structured_format", "bengali_language"]
            },
            {
                "name": "truth_verification",
                "agent_type": "verifier",
                "description": "Verify information and assumptions",
                "system_prompt": "আপনি একজন সত্যতা যাচাইকারী। তথ্যের নির্ভুলতা নিশ্চিত করুন।",
                "user_prompt_template": "এই তথ্য যাচাই করুন: {information}\nপ্রসঙ্গ: {context}\nযাচাইয়ের ক্ষেত্র: {verification_areas}",
                "expected_output_format": "যাচাইকরণ + মূল্যায়ন",
                "context_requirements": ["information", "context"],
                "validation_rules": ["structured_format", "bengali_language"]
            },
            {
                "name": "conversation",
                "agent_type": "conversational",
                "description": "Natural conversation and Q&A",
                "system_prompt": "আপনি একজন বন্ধুত্বপূর্ণ AI সহকারী। সহায়তা করুন।",
                "user_prompt_template": "ব্যবহারকারী প্রশ্ন: {question}\nপ্রসঙ্গ: {context}\nভাষা: {language}",
                "expected_output_format": "প্রাকৃতিক উত্তর",
                "context_requirements": ["question"],
                "validation_rules": ["bengali_language"]
            },
            {
                "name": "system_operations",
                "agent_type": "ops",
                "description": "Handle system operations and automation",
                "system_prompt": "আপনি একজন সিস্টেম অপারেশন বিশেষজ্ঞ। কাজ স্বয়ংক্রিয় করুন।",
                "user_prompt_template": "অপারেশন: {operation}\nসিস্টেম: {system}\nপরিবেশ: {environment}",
                "expected_output_format": "সমাধান + স্ট্যাটাস",
                "context_requirements": ["operation", "system"],
                "validation_rules": ["structured_format", "bengali_language"]
            }
        ]
    }
    
    os.makedirs("config", exist_ok=True)
    with open("config/prompt_templates.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
    
    return config

if __name__ == "__main__":
    # Create default configuration
    create_default_config()
    
    # Test the system
    prompt_system = PromptScopingSystem()
    
    # Test code generation prompt
    context = {
        "task": "CSV ফাইল পড়া এবং ডেটা ক্লিন করা",
        "language": "Python",
        "libraries": "pandas, numpy"
    }
    
    try:
        prompt = prompt_system.get_prompt("code_generation", context)
        print("✅ Code Generation Prompt:")
        print(prompt["user_prompt"])
        print("\n" + "="*50 + "\n")
        
        # Test dynamic prompt
        dynamic_prompt = prompt_system.create_dynamic_prompt(
            AgentType.PROGRAMMING,
            "একটি REST API তৈরি করুন",
            {"framework": "FastAPI", "database": "SQLite"}
        )
        print("✅ Dynamic Programming Prompt:")
        print(dynamic_prompt)
        print("\n" + "="*50 + "\n")
        
        # Test response validation
        test_response = """
        ## Python কোড
        
        ```python
        import pandas as pd
        import numpy as np
        
        def clean_csv_data(file_path):
            # CSV ফাইল পড়া
            df = pd.read_csv(file_path)
            
            # ডেটা ক্লিন করা
            df = df.dropna()
            df = df.drop_duplicates()
            
            return df
        ```
        
        এই কোডটি CSV ফাইল পড়ে এবং ডেটা ক্লিন করে।
        """
        
        validation = prompt_system.validate_response("code_generation", test_response)
        print("✅ Response Validation:")
        print(f"Valid: {validation['valid']}")
        for result in validation['validation_results']:
            print(f"- {result['rule']}: {'✅' if result['passed'] else '❌'} {result['message']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
