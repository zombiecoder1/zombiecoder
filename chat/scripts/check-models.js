const axios = require('axios');

// Common local AI endpoints to check
const AI_ENDPOINTS = [
  {
    name: 'Ollama',
    url: 'http://localhost:11434',
    models: ['llama2', 'llama2:7b', 'llama2:13b', 'mistral', 'codellama', 'phi2', 'gemma2'],
    testEndpoint: '/api/tags'
  },
  {
    name: 'LM Studio',
    url: 'http://localhost:1234',
    models: ['default'],
    testEndpoint: '/v1/models'
  },
  {
    name: 'OpenAI Compatible',
    url: 'http://localhost:8000',
    models: ['default'],
    testEndpoint: '/v1/models'
  },
  {
    name: 'LocalAI',
    url: 'http://localhost:8080',
    models: ['default'],
    testEndpoint: '/models'
  }
];

async function checkEndpoint(endpoint) {
  try {
    console.log(`🔍 Checking ${endpoint.name} at ${endpoint.url}...`);
    
    const response = await axios.get(`${endpoint.url}${endpoint.testEndpoint}`, {
      timeout: 5000
    });
    
    console.log(`✅ ${endpoint.name} is running!`);
    console.log(`📊 Response:`, response.data);
    
    return {
      name: endpoint.name,
      url: endpoint.url,
      available: true,
      models: endpoint.models,
      response: response.data
    };
  } catch (error) {
    console.log(`❌ ${endpoint.name} is not available: ${error.message}`);
    return {
      name: endpoint.name,
      url: endpoint.url,
      available: false,
      error: error.message
    };
  }
}

async function testModelSpeed(endpoint, model) {
  try {
    console.log(`⚡ Testing speed for ${model} on ${endpoint.name}...`);
    
    const startTime = Date.now();
    
    const response = await axios.post(`${endpoint.url}/api/generate`, {
      model: model,
      prompt: "Hello, how are you?",
      stream: false,
      options: {
        temperature: 0.7,
        num_predict: 50
      }
    }, {
      timeout: 30000
    });
    
    const endTime = Date.now();
    const responseTime = endTime - startTime;
    
    console.log(`✅ ${model} responded in ${responseTime}ms`);
    
    return {
      model: model,
      responseTime: responseTime,
      success: true,
      response: response.data.response
    };
  } catch (error) {
    console.log(`❌ ${model} test failed: ${error.message}`);
    return {
      model: model,
      success: false,
      error: error.message
    };
  }
}

async function main() {
  console.log('🚀 Checking available local AI models...\n');
  
  const results = [];
  
  // Check all endpoints
  for (const endpoint of AI_ENDPOINTS) {
    const result = await checkEndpoint(endpoint);
    results.push(result);
  }
  
  // Find available endpoints
  const availableEndpoints = results.filter(r => r.available);
  
  if (availableEndpoints.length === 0) {
    console.log('\n❌ No local AI models found!');
    console.log('Please start one of the following:');
    console.log('- Ollama: ollama serve');
    console.log('- LM Studio: Start LM Studio');
    console.log('- LocalAI: local-ai server');
    return;
  }
  
  console.log(`\n✅ Found ${availableEndpoints.length} available AI service(s)`);
  
  // Test speed for each available endpoint
  const speedResults = [];
  
  for (const endpoint of availableEndpoints) {
    for (const model of endpoint.models) {
      const speedResult = await testModelSpeed(endpoint, model);
      speedResults.push({
        endpoint: endpoint.name,
        ...speedResult
      });
    }
  }
  
  // Sort by response time (fastest first)
  const successfulTests = speedResults.filter(r => r.success);
  successfulTests.sort((a, b) => a.responseTime - b.responseTime);
  
  console.log('\n🏆 Speed Test Results (Fastest to Slowest):');
  console.log('==========================================');
  
  successfulTests.forEach((test, index) => {
    console.log(`${index + 1}. ${test.endpoint} - ${test.model}: ${test.responseTime}ms`);
  });
  
  if (successfulTests.length > 0) {
    const fastest = successfulTests[0];
    console.log(`\n🎯 Recommended: ${fastest.endpoint} with ${fastest.model} (${fastest.responseTime}ms)`);
    
    // Save recommendation to file
    const fs = require('fs');
    const recommendation = {
      endpoint: fastest.endpoint,
      model: fastest.model,
      url: availableEndpoints.find(e => e.name === fastest.endpoint)?.url,
      responseTime: fastest.responseTime,
      timestamp: new Date().toISOString()
    };
    
    fs.writeFileSync('ai-model-recommendation.json', JSON.stringify(recommendation, null, 2));
    console.log('💾 Recommendation saved to ai-model-recommendation.json');
  }
  
  console.log('\n✨ Model check completed!');
}

main().catch(console.error);
