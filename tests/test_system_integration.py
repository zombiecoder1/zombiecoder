#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ZombieCoder System Integration Tests
Comprehensive testing of all system components
"""

import unittest
import requests
import json
import time
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestZombieCoderSystem(unittest.TestCase):
    """Test suite for ZombieCoder system integration."""
    
    def setUp(self):
        """Set up test environment."""
        self.main_server_url = "http://localhost:12345"
        self.proxy_server_url = "http://localhost:8080"
        self.multi_project_url = "http://localhost:8081"
        self.timeout = 10
        
    def test_main_server_status(self):
        """Test main server is running and responding."""
        try:
            response = requests.get(f"{self.main_server_url}/api/status", timeout=self.timeout)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn("status", data)
            self.assertEqual(data["status"], "active")
            
            logger.info("✅ Main server status test passed")
        except requests.exceptions.RequestException as e:
            self.fail(f"Main server not responding: {e}")
    
    def test_proxy_server_status(self):
        """Test proxy server is running and responding."""
        try:
            response = requests.get(f"{self.proxy_server_url}/proxy/status", timeout=self.timeout)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn("status", data)
            self.assertEqual(data["status"], "active")
            
            logger.info("✅ Proxy server status test passed")
        except requests.exceptions.RequestException as e:
            self.fail(f"Proxy server not responding: {e}")
    
    def test_multi_project_api_status(self):
        """Test multi-project API is running and responding."""
        try:
            response = requests.get(f"{self.multi_project_url}/api/projects/status", timeout=self.timeout)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn("status", data)
            self.assertEqual(data["status"], "active")
            
            logger.info("✅ Multi-project API status test passed")
        except requests.exceptions.RequestException as e:
            self.fail(f"Multi-project API not responding: {e}")
    
    def test_proxy_chat_functionality(self):
        """Test proxy chat functionality with local agent."""
        try:
            chat_data = {
                "messages": [
                    {"role": "user", "content": "Hello, test message"}
                ],
                "model": "zombiecoder-local"
            }
            
            response = requests.post(
                f"{self.proxy_server_url}/proxy/chat",
                json=chat_data,
                timeout=30
            )
            
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn("choices", data)
            self.assertGreater(len(data["choices"]), 0)
            
            choice = data["choices"][0]
            self.assertIn("message", choice)
            self.assertIn("content", choice["message"])
            
            logger.info("✅ Proxy chat functionality test passed")
        except requests.exceptions.RequestException as e:
            self.fail(f"Proxy chat test failed: {e}")
    
    def test_agent_switching(self):
        """Test agent switching functionality."""
        try:
            # Test switching to different agents
            agents = [
                "ZombieCoder Agent (সাহন ভাই)",
                "DocMaster",
                "BugHunter",
                "CloudFallback"
            ]
            
            for agent in agents:
                chat_data = {
                    "messages": [
                        {"role": "user", "content": f"Switch to {agent}"}
                    ],
                    "model": "zombiecoder-local"
                }
                
                response = requests.post(
                    f"{self.proxy_server_url}/proxy/chat",
                    json=chat_data,
                    timeout=30
                )
                
                self.assertEqual(response.status_code, 200)
                
                data = response.json()
                self.assertIn("choices", data)
                
                logger.info(f"✅ Agent switching test passed for {agent}")
                
        except requests.exceptions.RequestException as e:
            self.fail(f"Agent switching test failed: {e}")
    
    def test_cloud_fallback(self):
        """Test cloud fallback functionality."""
        try:
            # Test with a complex request that might trigger fallback
            chat_data = {
                "messages": [
                    {"role": "user", "content": "Explain quantum computing in detail"}
                ],
                "model": "zombiecoder-local"
            }
            
            response = requests.post(
                f"{self.proxy_server_url}/proxy/chat",
                json=chat_data,
                timeout=60
            )
            
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn("choices", data)
            self.assertGreater(len(data["choices"]), 0)
            
            # Check if fallback was used
            if "source" in data:
                logger.info(f"✅ Cloud fallback test passed (source: {data['source']})")
            else:
                logger.info("✅ Cloud fallback test passed (local processing)")
                
        except requests.exceptions.RequestException as e:
            self.fail(f"Cloud fallback test failed: {e}")
    
    def test_multi_project_functionality(self):
        """Test multi-project management functionality."""
        try:
            # Test project listing
            response = requests.get(f"{self.multi_project_url}/api/projects", timeout=self.timeout)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn("projects", data)
            self.assertIn("total_projects", data)
            
            logger.info("✅ Multi-project functionality test passed")
            
        except requests.exceptions.RequestException as e:
            self.fail(f"Multi-project functionality test failed: {e}")
    
    def test_performance_metrics(self):
        """Test system performance metrics."""
        try:
            start_time = time.time()
            
            chat_data = {
                "messages": [
                    {"role": "user", "content": "Quick test"}
                ],
                "model": "zombiecoder-local"
            }
            
            response = requests.post(
                f"{self.proxy_server_url}/proxy/chat",
                json=chat_data,
                timeout=30
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            self.assertEqual(response.status_code, 200)
            
            # Performance check (should be under 10 seconds)
            self.assertLess(response_time, 10.0)
            
            logger.info(f"✅ Performance test passed (response time: {response_time:.2f}s)")
            
        except requests.exceptions.RequestException as e:
            self.fail(f"Performance test failed: {e}")
    
    def test_error_handling(self):
        """Test error handling and edge cases."""
        try:
            # Test with invalid data
            invalid_data = {
                "invalid": "data"
            }
            
            response = requests.post(
                f"{self.proxy_server_url}/proxy/chat",
                json=invalid_data,
                timeout=self.timeout
            )
            
            # Should handle gracefully (either 400 or 200 with error in response)
            self.assertIn(response.status_code, [200, 400])
            
            logger.info("✅ Error handling test passed")
            
        except requests.exceptions.RequestException as e:
            self.fail(f"Error handling test failed: {e}")

def run_integration_tests():
    """Run all integration tests."""
    logger.info("🧪 Starting ZombieCoder System Integration Tests...")
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestZombieCoderSystem)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    logger.info(f"\n📊 Test Summary:")
    logger.info(f"Tests run: {result.testsRun}")
    logger.info(f"Failures: {len(result.failures)}")
    logger.info(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        logger.info("🎉 All integration tests passed!")
        return True
    else:
        logger.error("❌ Some integration tests failed!")
        return False

if __name__ == "__main__":
    run_integration_tests()
