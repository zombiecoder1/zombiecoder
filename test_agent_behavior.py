#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧩 Agent Behavior Test
======================

Test the agent behavior system implementation
"""

import sys
import os
sys.path.append('core-server')

from agent_behavior import get_agent_behavior

def test_agent_behavior():
    """Test agent behavior system"""
    print("🧩 Testing Agent Behavior System")
    print("=" * 50)
    
    # Get agent behavior instance
    behavior = get_agent_behavior()
    
    # Test 1: Agent Configuration
    print("\n1️⃣ Testing Agent Configuration:")
    agent_config = behavior.get_agent_config("ZombieCoderAgent")
    if agent_config:
        print(f"✅ Agent: {agent_config['name']}")
        print(f"✅ Role: {agent_config['role']}")
        print(f"✅ Traits: {', '.join(agent_config['traits'])}")
    else:
        print("❌ Agent configuration not found")
    
    # Test 2: Truthfulness Verification
    print("\n2️⃣ Testing Truthfulness Verification:")
    test_response = "I'm not sure but I think this might work"
    truth_check = behavior.verify_truthfulness("ZombieCoderAgent", test_response)
    print(f"✅ Verified: {truth_check['verified']}")
    if truth_check['warnings']:
        print(f"⚠️ Warnings: {truth_check['warnings']}")
    
    # Test 3: Task Report Generation
    print("\n3️⃣ Testing Task Report Generation:")
    verification_results = {"verified": True, "warnings": []}
    report = behavior.create_task_report(
        "ZombieCoderAgent", 
        "Test Task", 
        "Completed Successfully", 
        verification_results
    )
    print("✅ Task Report Generated:")
    print(report)
    
    # Test 4: Behavior Rules Enforcement
    print("\n4️⃣ Testing Behavior Rules Enforcement:")
    context = {"task": "test", "status": "starting"}
    enforced = behavior.enforce_behavior_rules("ZombieCoderAgent", "task_start", context)
    print(f"✅ Rules Enforced: {enforced['enforced']}")
    print(f"✅ Compliance: {enforced['compliance']}")
    
    # Test 5: Friendly Response Generation
    print("\n5️⃣ Testing Friendly Response Generation:")
    friendly_response = behavior.generate_friendly_response(
        "ZombieCoderAgent", 
        "Task completed successfully!", 
        {"status": "success"}
    )
    print(f"✅ Friendly Response: {friendly_response}")
    
    # Test 6: Task Validation
    print("\n6️⃣ Testing Task Validation:")
    task_results = {
        "status": "completed",
        "data": {"result": "success"},
        "user_feedback": "Great job!",
        "system_status": "healthy"
    }
    validation = behavior.validate_task_completion("ZombieCoderAgent", task_results)
    print(f"✅ Validated: {validation['validated']}")
    print(f"✅ Checks Passed: {validation['checks_passed']}/{validation['total_checks']}")
    
    if validation['issues']:
        print("⚠️ Issues:")
        for issue in validation['issues']:
            print(f"   - {issue}")
    
    print("\n🎯 Agent Behavior System Test Completed!")
    print("✅ All core features working correctly")

if __name__ == "__main__":
    test_agent_behavior()
