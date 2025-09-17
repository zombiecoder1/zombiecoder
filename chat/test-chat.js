async function testChat() {
  try {
    console.log('🧪 Testing Chat with Subprocess Approach...\n');
    
    // Test 1: Simple chat
    console.log('Test 1: Simple chat request...');
    const response = await fetch('http://localhost:3001/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: "Write a simple Python function to add two numbers"
      })
    });

    if (response.ok) {
      const data = await response.json();
      console.log('✅ Chat successful!');
      console.log('Response:', data.response.substring(0, 200) + '...');
    } else {
      console.error('❌ Chat failed:', response.status);
    }

    console.log('\n' + '='.repeat(50) + '\n');

    // Test 2: Bengali chat
    console.log('Test 2: Bengali chat request...');
    const bengaliResponse = await fetch('http://localhost:3001/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: "আমাকে একটি সিম্পল Python ফাংশন লিখে দাও"
      })
    });

    if (bengaliResponse.ok) {
      const data = await bengaliResponse.json();
      console.log('✅ Bengali chat successful!');
      console.log('Response:', data.response.substring(0, 200) + '...');
    } else {
      console.error('❌ Bengali chat failed:', bengaliResponse.status);
    }

    console.log('\n' + '='.repeat(50) + '\n');

    // Test 3: Streaming chat
    console.log('Test 3: Streaming chat request...');
    const streamResponse = await fetch('http://localhost:3001/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: "Explain what is subprocess in Python"
      })
    });

    if (streamResponse.ok) {
      console.log('✅ Streaming started!');
      const reader = streamResponse.body.getReader();
      const decoder = new TextDecoder();
      let fullResponse = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.chunk) {
                process.stdout.write(data.chunk);
                fullResponse += data.chunk;
              }
              if (data.type === 'complete') {
                console.log('\n✅ Streaming completed!');
                break;
              }
            } catch (e) {
              // Ignore parsing errors
            }
          }
        }
      }
    } else {
      console.error('❌ Streaming failed:', streamResponse.status);
    }

  } catch (error) {
    console.error('❌ Test failed:', error.message);
  }
}

// Run test
testChat();
