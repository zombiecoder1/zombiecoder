#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧩 Agent Behavior Implementation
================================

This module implements the agent character configuration guidelines:
- Truthful Mode
- Task-Oriented Behavior
- Friendly Support
- Double Check System
"""

import yaml
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

class AgentBehavior:
    """Agent Behavior Management System"""
    
    def __init__(self, config_path: str = "config/agent_characters.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
        self.logger = logging.getLogger(__name__)
        
    def load_config(self) -> Dict[str, Any]:
        """Load agent character configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Default configuration if file loading fails"""
        return {
            "agents": [
                {
                    "name": "ZombieCoderAgent",
                    "role": "Unified AI Assistant",
                    "traits": ["truthful", "verify_tasks", "friendly", "double_check"],
                    "behavior": ["never_hallucinate", "report_completion", "assist_in_simple_words"]
                }
            ]
        }
    
    def get_agent_config(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for specific agent"""
        for agent in self.config.get("agents", []):
            if agent.get("name") == agent_name:
                return agent
        return None
    
    def verify_truthfulness(self, agent_name: str, response: str) -> Dict[str, Any]:
        """Verify response truthfulness"""
        agent_config = self.get_agent_config(agent_name)
        if not agent_config:
            return {"verified": False, "reason": "Agent not found"}
        
        # Check for common hallucination patterns
        hallucination_indicators = [
            "I'm not sure but I think",
            "This might be",
            "I believe",
            "Probably",
            "I assume"
        ]
        
        is_truthful = True
        warnings = []
        
        for indicator in hallucination_indicators:
            if indicator.lower() in response.lower():
                is_truthful = False
                warnings.append(f"Potential uncertainty: {indicator}")
        
        return {
            "verified": is_truthful,
            "warnings": warnings,
            "agent": agent_name,
            "timestamp": datetime.now().isoformat()
        }
    
    def create_task_report(self, agent_name: str, task_name: str, 
                          completion_status: str, verification_results: Dict[str, Any]) -> str:
        """Create task completion report following checklist template"""
        agent_config = self.get_agent_config(agent_name)
        
        report = f"""
📋 **Task Completion Report - {agent_name}**
==========================================

✅ **সম্পন্ন কাজের নাম**: {task_name}
🔎 **চেক ফলাফল**: {completion_status}

"""
        
        if verification_results.get("verified"):
            report += "✅ **Truthfulness**: Verified\n"
        else:
            report += "⚠️ **Truthfulness**: Issues detected\n"
            for warning in verification_results.get("warnings", []):
                report += f"   - {warning}\n"
        
        report += f"""
🛠️ **পরবর্তী পদক্ষেপ**: 
   - Task completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
   - Agent: {agent_name}
   - Role: {agent_config.get('role', 'Unknown') if agent_config else 'Unknown'}
"""
        
        return report
    
    def enforce_behavior_rules(self, agent_name: str, action: str, 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Enforce behavior rules for agent actions"""
        agent_config = self.get_agent_config(agent_name)
        if not agent_config:
            return {"enforced": False, "reason": "Agent not found"}
        
        # Check behavior compliance
        compliance = {
            "truthful": "truthful" in agent_config.get("traits", []),
            "verify_tasks": "verify_tasks" in agent_config.get("traits", []),
            "friendly": "friendly" in agent_config.get("traits", []),
            "double_check": "double_check" in agent_config.get("traits", [])
        }
        
        # Enforce rules based on action type
        if action == "task_start":
            if compliance["verify_tasks"]:
                context["logic_check_required"] = True
                context["verification_steps"] = []
        
        elif action == "task_complete":
            if compliance["double_check"]:
                context["validation_required"] = True
                context["double_check_results"] = []
        
        elif action == "response_generation":
            if compliance["truthful"]:
                context["truthfulness_check"] = True
                context["uncertainty_handling"] = "admit_unknown"
        
        return {
            "enforced": True,
            "compliance": compliance,
            "context": context,
            "agent": agent_name
        }
    
    def generate_friendly_response(self, agent_name: str, message: str, 
                                 context: Dict[str, Any]) -> str:
        """Generate friendly, supportive response"""
        agent_config = self.get_agent_config(agent_name)
        
        # Add friendly prefix
        friendly_prefixes = [
            "ভাইয়া, ",
            "দোস্ত, ",
            "বন্ধু, ",
            "সাহায্যকারী হিসেবে, "
        ]
        
        prefix = friendly_prefixes[0]  # Default to "ভাইয়া"
        
        # Check if response should be encouraging
        if "error" in context or "failed" in context:
            prefix = "ভাইয়া, চিন্তা করবেন না! "
            message = f"{message}\n\n💪 আমরা একসাথে ঠিক করে ফেলব!"
        
        return f"{prefix}{message}"
    
    def validate_task_completion(self, agent_name: str, task_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate task completion with double check"""
        agent_config = self.get_agent_config(agent_name)
        
        validation = {
            "validated": False,
            "checks_passed": 0,
            "total_checks": 0,
            "issues": [],
            "recommendations": []
        }
        
        # Perform validation checks
        checks = [
            self._check_result_consistency(task_results),
            self._check_error_handling(task_results),
            self._check_user_feedback(task_results),
            self._check_system_integrity(task_results)
        ]
        
        for check in checks:
            validation["total_checks"] += 1
            if check["passed"]:
                validation["checks_passed"] += 1
            else:
                validation["issues"].append(check["issue"])
                validation["recommendations"].append(check["recommendation"])
        
        validation["validated"] = validation["checks_passed"] >= validation["total_checks"] * 0.8
        
        return validation
    
    def _check_result_consistency(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check if results are consistent"""
        return {
            "passed": "status" in results and "data" in results,
            "issue": "Missing required result fields" if "status" not in results or "data" not in results else None,
            "recommendation": "Ensure all required fields are present in results"
        }
    
    def _check_error_handling(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check error handling"""
        has_errors = "errors" in results and results["errors"]
        return {
            "passed": not has_errors,
            "issue": "Errors detected in results" if has_errors else None,
            "recommendation": "Review and fix detected errors"
        }
    
    def _check_user_feedback(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check user feedback integration"""
        return {
            "passed": "user_feedback" in results,
            "issue": "No user feedback mechanism" if "user_feedback" not in results else None,
            "recommendation": "Include user feedback in results"
        }
    
    def _check_system_integrity(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check system integrity"""
        return {
            "passed": "system_status" in results,
            "issue": "No system status information" if "system_status" not in results else None,
            "recommendation": "Include system status in results"
        }

# Global instance
agent_behavior = AgentBehavior()

def get_agent_behavior() -> AgentBehavior:
    """Get global agent behavior instance"""
    return agent_behavior
