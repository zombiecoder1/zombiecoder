const {
  spawn
} = require('child_process');
const path = require('path');

console.log('🚀 Starting Chat Interface with AI & TTS Servers...\n');

let aiServer = null;
let ttsServer = null;
let memoryServer = null;
let orchestratorServer = null;
let nextServer = null;

// Function to start AI Server
function startAIServer() {
  console.log('🤖 Starting AI Server...');
  aiServer = spawn('node', ['server/ai-server.js'], {
    stdio: 'inherit',
    cwd: process.cwd()
  });

  aiServer.on('error', (error) => {
    console.error('❌ AI Server error:', error);
  });

  aiServer.on('exit', (code) => {
    if (code !== 0) {
      console.error(`❌ AI Server exited with code ${code}`);
    }
  });

  // Wait for AI server to start
  setTimeout(startMemoryServer, 2000);
}

// Function to start Memory Server
function startMemoryServer() {
  console.log('🧠 Starting Memory Server...');
  memoryServer = spawn('node', ['server/memory-server.js'], {
    stdio: 'inherit',
    cwd: process.cwd()
  });

  memoryServer.on('error', (error) => {
    console.error('❌ Memory Server error:', error);
  });

  memoryServer.on('exit', (code) => {
    if (code !== 0) {
      console.error(`❌ Memory Server exited with code ${code}`);
    }
  });

  // Wait for Memory server to start
  setTimeout(startTTSServer, 2000);
}

// Function to start TTS Server
function startTTSServer() {
  console.log('🎤 Starting TTS Server...');
  ttsServer = spawn('node', ['server/tts-server.js'], {
    stdio: 'inherit',
    cwd: process.cwd()
  });

  ttsServer.on('error', (error) => {
    console.error('❌ TTS Server error:', error);
  });

  ttsServer.on('exit', (code) => {
    if (code !== 0) {
      console.error(`❌ TTS Server exited with code ${code}`);
    }
  });

  // Wait for TTS server to start
  setTimeout(startOrchestratorServer, 2000);
}

// Function to start Orchestrator Server
function startOrchestratorServer() {
  console.log('🎯 Starting Orchestrator Server...');
  orchestratorServer = spawn('python', ['orchestrator/nextjs_integration.py'], {
    stdio: 'inherit',
    cwd: process.cwd()
  });

  orchestratorServer.on('error', (error) => {
    console.error('❌ Orchestrator Server error:', error);
  });

  orchestratorServer.on('exit', (code) => {
    if (code !== 0) {
      console.error(`❌ Orchestrator Server exited with code ${code}`);
    }
  });

  // Wait for Orchestrator server to start
  setTimeout(startNextServer, 3000);
}

// Function to start Next.js Server
function startNextServer() {
  console.log('🌐 Starting Next.js Development Server...');
  nextServer = spawn('npm', ['run', 'dev'], {
    stdio: 'inherit',
    cwd: process.cwd()
  });

  nextServer.on('error', (error) => {
    console.error('❌ Next.js Server error:', error);
  });

  nextServer.on('exit', (code) => {
    if (code !== 0) {
      console.error(`❌ Next.js Server exited with code ${code}`);
    }
  });
}

// Handle process termination
function cleanup() {
  console.log('\n🛑 Shutting down all servers...');

  if (aiServer) {
    aiServer.kill();
    console.log('✅ AI Server stopped');
  }

  if (memoryServer) {
    memoryServer.kill();
    console.log('✅ Memory Server stopped');
  }

  if (ttsServer) {
    ttsServer.kill();
    console.log('✅ TTS Server stopped');
  }

  if (orchestratorServer) {
    orchestratorServer.kill();
    console.log('✅ Orchestrator Server stopped');
  }

  if (nextServer) {
    nextServer.kill();
    console.log('✅ Next.js Server stopped');
  }

  process.exit(0);
}

// Listen for termination signals
process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
process.on('SIGQUIT', cleanup);

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('❌ Uncaught Exception:', error);
  cleanup();
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Unhandled Rejection at:', promise, 'reason:', reason);
  cleanup();
});

// Start the sequence
console.log('📋 Starting services in sequence:');
console.log('1. AI Server (Port 3001)');
console.log('2. Memory Server (Port 3003)');
console.log('3. TTS Server (Port 3002)');
console.log('4. Orchestrator Server (Port 3004)');
console.log('5. Next.js Server (Port 3000)');
console.log('');

startAIServer();

// Show status after all servers start
setTimeout(() => {
  console.log('\n🎉 All servers started successfully!');
  console.log('📱 Chat Interface: http://localhost:3000');
  console.log('🤖 AI Server: http://localhost:3001/health');
  console.log('🧠 Memory Server: http://localhost:3003/health');
  console.log('🎤 TTS Server: http://localhost:3002/health');
  console.log('🎯 Orchestrator Server: http://localhost:3004/api/health');
  console.log('\n💡 Press Ctrl+C to stop all servers');
}, 12000);