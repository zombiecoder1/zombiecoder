/**
 * Integration Test Script for Enhanced Chat Interface
 * Editor ভাই-এর জন্য System Integration Test
 */

const { spawn } = require('child_process');
const fetch = require('node-fetch');

console.log('🧪 Testing Enhanced Chat Interface Integration');
console.log('Editor ভাই-এর জন্য System Integration Test');
console.log('='.repeat(60));

const services = [
  { name: 'AI Server', port: 3001, url: 'http://localhost:3001/health' },
  { name: 'TTS Server', port: 3002, url: 'http://localhost:3002/health' },
  { name: 'Memory Server', port: 3003, url: 'http://localhost:3003/health' },
  { name: 'Orchestrator Server', port: 3004, url: 'http://localhost:3004/api/health' },
  { name: 'Next.js Server', port: 3000, url: 'http://localhost:3000' }
];

async function testService(service) {
  try {
    console.log(`\n🔍 Testing ${service.name}...`);
    
    const response = await fetch(service.url, { 
      method: 'GET',
      timeout: 5000 
    });
    
    if (response.ok) {
      console.log(`✅ ${service.name} is running on port ${service.port}`);
      return true;
    } else {
      console.log(`❌ ${service.name} returned status ${response.status}`);
      return false;
    }
  } catch (error) {
    console.log(`❌ ${service.name} is not accessible: ${error.message}`);
    return false;
  }
}

async function testOrchestratorIntegration() {
  try {
    console.log('\n🎯 Testing Orchestrator Integration...');
    
    const testMessage = {
      message: "আজকের আবহাওয়া কেমন?",
      history: [],
      conversationId: "test_session",
      userId: "test_user"
    };
    
    const response = await fetch('http://localhost:3004/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(testMessage)
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Orchestrator chat endpoint working');
      console.log(`📝 Response: ${data.response.substring(0, 100)}...`);
      console.log(`🌐 Language: ${data.language}`);
      console.log(`🎯 Intent: ${data.intent}`);
      console.log(`⏱️ Processing Time: ${data.processingTime}s`);
      return true;
    } else {
      console.log(`❌ Orchestrator chat endpoint failed: ${response.status}`);
      return false;
    }
  } catch (error) {
    console.log(`❌ Orchestrator integration test failed: ${error.message}`);
    return false;
  }
}

async function testNextJSIntegration() {
  try {
    console.log('\n🌐 Testing Next.js Integration...');
    
    const testMessage = {
      message: "Hello, how are you?",
      history: [],
      conversationId: "test_session",
      userId: "test_user"
    };
    
    const response = await fetch('http://localhost:3000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(testMessage)
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Next.js chat API working');
      console.log(`📝 Response: ${data.response.substring(0, 100)}...`);
      return true;
    } else {
      console.log(`❌ Next.js chat API failed: ${response.status}`);
      return false;
    }
  } catch (error) {
    console.log(`❌ Next.js integration test failed: ${error.message}`);
    return false;
  }
}

async function runAllTests() {
  console.log('\n🚀 Starting Integration Tests...\n');
  
  let passedTests = 0;
  let totalTests = 0;
  
  // Test individual services
  for (const service of services) {
    totalTests++;
    const result = await testService(service);
    if (result) passedTests++;
  }
  
  // Test orchestrator integration
  totalTests++;
  const orchestratorResult = await testOrchestratorIntegration();
  if (orchestratorResult) passedTests++;
  
  // Test Next.js integration
  totalTests++;
  const nextjsResult = await testNextJSIntegration();
  if (nextjsResult) passedTests++;
  
  // Final results
  console.log('\n' + '='.repeat(60));
  console.log('📊 INTEGRATION TEST RESULTS');
  console.log('='.repeat(60));
  console.log(`✅ Passed: ${passedTests}/${totalTests} tests`);
  console.log(`❌ Failed: ${totalTests - passedTests}/${totalTests} tests`);
  console.log(`📈 Success Rate: ${((passedTests / totalTests) * 100).toFixed(1)}%`);
  
  if (passedTests === totalTests) {
    console.log('\n🎉 ALL TESTS PASSED!');
    console.log('🚀 Enhanced Chat Interface is ready for use!');
    console.log('📱 Open http://localhost:3000 to start chatting');
  } else {
    console.log('\n⚠️  SOME TESTS FAILED');
    console.log('🔧 Please check the failed services and try again');
  }
  
  console.log('\n💡 Tips:');
  console.log('- Make sure all services are running');
  console.log('- Check port conflicts');
  console.log('- Verify environment variables');
  console.log('- Check service logs for errors');
}

// Run tests
runAllTests().catch(console.error);
