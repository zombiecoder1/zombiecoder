const {
    spawn
} = require('child_process');

console.log('🧪 Testing Direct Subprocess Approach...\n');

// Test 1: Simple ollama run
function testSimpleOllama() {
    return new Promise((resolve, reject) => {
        console.log('Test 1: Simple ollama run...');

        const ollamaProcess = spawn('ollama', ['run', 'deepseek-coder:latest'], {
            stdio: ['pipe', 'pipe', 'pipe'],
            shell: true
        });

        let output = '';
        let errorOutput = '';

        // Send a simple test prompt
        const testPrompt = "Say 'Hello from subprocess test' and nothing else.";
        ollamaProcess.stdin.write(testPrompt);
        ollamaProcess.stdin.end();

        ollamaProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        ollamaProcess.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        ollamaProcess.on('close', (code) => {
            if (code === 0) {
                console.log('✅ Simple test successful!');
                console.log('Output:', output.trim());
                resolve(output);
            } else {
                console.error('❌ Simple test failed!');
                console.error('Error output:', errorOutput);
                reject(new Error(`Process failed with code ${code}`));
            }
        });

        ollamaProcess.on('error', (error) => {
            console.error('❌ Process error:', error);
            reject(error);
        });

        setTimeout(() => {
            ollamaProcess.kill();
            reject(new Error('Test timeout'));
        }, 30000);
    });
}

// Test 2: Check if ollama is available
function testOllamaAvailability() {
    return new Promise((resolve, reject) => {
        console.log('Test 2: Checking ollama availability...');

        const checkProcess = spawn('ollama', ['--version'], {
            stdio: ['pipe', 'pipe', 'pipe'],
            shell: true
        });

        let output = '';
        let errorOutput = '';

        checkProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        checkProcess.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        checkProcess.on('close', (code) => {
            if (code === 0) {
                console.log('✅ Ollama is available!');
                console.log('Version:', output.trim());
                resolve(output);
            } else {
                console.error('❌ Ollama not found or not working!');
                console.error('Error:', errorOutput);
                reject(new Error('Ollama not available'));
            }
        });

        checkProcess.on('error', (error) => {
            console.error('❌ Ollama check error:', error);
            reject(error);
        });
    });
}

// Test 3: List available models
function testListModels() {
    return new Promise((resolve, reject) => {
        console.log('Test 3: Listing available models...');

        const listProcess = spawn('ollama', ['list'], {
            stdio: ['pipe', 'pipe', 'pipe'],
            shell: true
        });

        let output = '';
        let errorOutput = '';

        listProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        listProcess.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        listProcess.on('close', (code) => {
            if (code === 0) {
                console.log('✅ Models listed successfully!');
                console.log('Available models:');
                console.log(output);
                resolve(output);
            } else {
                console.error('❌ Failed to list models!');
                console.error('Error:', errorOutput);
                reject(new Error('Failed to list models'));
            }
        });

        listProcess.on('error', (error) => {
            console.error('❌ List models error:', error);
            reject(error);
        });
    });
}

// Run all tests
async function runAllTests() {
    try {
        console.log('🚀 Starting subprocess tests...\n');

        // Test 1: Check ollama availability
        await testOllamaAvailability();
        console.log('');

        // Test 2: List models
        await testListModels();
        console.log('');

        // Test 3: Simple ollama run
        await testSimpleOllama();
        console.log('');

        console.log('🎉 All tests passed! Subprocess approach should work.');
        console.log('💡 You can now use this approach in your AI server.');

    } catch (error) {
        console.error('❌ Test failed:', error.message);
        console.log('');
        console.log('🔧 Troubleshooting tips:');
        console.log('1. Make sure ollama is installed and in PATH');
        console.log('2. Make sure you have at least one model downloaded');
        console.log('3. Try running: ollama run deepseek-coder:latest');
        console.log('4. Check if ollama service is running');
    }
}

// Run tests if this file is executed directly
if (require.main === module) {
    runAllTests();
}

module.exports = {
    testSimpleOllama,
    testOllamaAvailability,
    testListModels,
    runAllTests
};