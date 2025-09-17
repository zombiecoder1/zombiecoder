const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const winston = require('winston');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const {
  spawn
} = require('child_process');

const app = express();
const PORT = process.env.AI_SERVER_PORT || 3001;

// Logger configuration
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error'
    }),
    new winston.transports.File({
      filename: 'logs/combined.log'
    }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.NODE_ENV === 'production' ? ['http://localhost:3000'] : ['http://localhost:3000', 'http://127.0.0.1:3000'],
  credentials: true
}));
app.use(express.json({
  limit: '10mb'
}));

// Load AI model recommendation
function loadModelRecommendation() {
  try {
    if (fs.existsSync('ai-model-recommendation.json')) {
      const data = fs.readFileSync('ai-model-recommendation.json', 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    logger.error('Error loading model recommendation:', error);
  }

  // Default fallback
  return {
    endpoint: 'Ollama',
    model: 'llama3.1:8b',
    url: 'http://localhost:11434',
    fallbackModels: ['deepseek-coder:latest', 'codellama:latest', 'qwen2.5-coder:1.5b-base', 'llama3.2:1b']
  };
}

// AI model configuration
const AI_CONFIG = loadModelRecommendation();

// Memory server configuration
const MEMORY_SERVER_URL = process.env.MEMORY_SERVER_URL || 'http://localhost:3003';

// Cache for responses
const responseCache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

// Helper function to detect language
function detectLanguage(text) {
  const bengaliRegex = /[\u0980-\u09FF]/;
  const isBengali = bengaliRegex.test(text);
  console.log('Language detection:', {
    text: text.substring(0, 50),
    isBengali
  });
  return isBengali ? 'bengali' : 'english';
}

// Helper function to generate system prompt based on language
function generateSystemPrompt(language) {
  if (language === 'bengali') {
    return `আপনি একজন সহায়ক AI। আপনি বাংলা এবং ইংরেজি উভয় ভাষায় কথা বলতে পারেন। 
    আপনার উত্তরগুলি সঠিক, সহায়ক এবং বন্ধুত্বপূর্ণ হওয়া উচিত। 
    আপনি যদি কোন প্রশ্নের উত্তর না জানেন, তাহলে সৎভাবে বলুন।
    
    গুরুত্বপূর্ণ নিয়ম:
    1. বাংলায় প্রশ্ন করলে বাংলায় উত্তর দিন
    2. ইংরেজিতে প্রশ্ন করলে ইংরেজিতে উত্তর দিন
    3. উত্তরগুলি সংক্ষিপ্ত এবং স্পষ্ট করুন
    4. কখনো মিথ্যা বলবেন না`;
  } else {
    return `You are a helpful AI assistant. You can communicate in both Bengali and English. 
    Your responses should be accurate, helpful, and friendly. 
    If you don't know the answer to a question, be honest about it.
    
    Important rules:
    1. Answer in Bengali if asked in Bengali
    2. Answer in English if asked in English
    3. Keep responses concise and clear
    4. Never provide false information`;
  }
}

// Helper function to get conversation context from memory
async function getConversationContext(conversationId, userId) {
  try {
    // Get context from memory server
    const response = await axios.get(`${MEMORY_SERVER_URL}/api/conversations/${conversationId}/context`);

    if (response.data && response.data.context) {
      logger.info(`Retrieved context for conversation: ${conversationId}`);
      return response.data.context;
    }

    return [];
  } catch (error) {
    logger.error('Error getting conversation context:', error.message);
    return [];
  }
}

// Helper function to save message to memory
async function saveMessageToMemory(conversationId, role, content) {
  try {
    await axios.post(`${MEMORY_SERVER_URL}/api/conversations/${conversationId}/messages`, {
      role,
      content,
      timestamp: new Date().toISOString()
    });

    logger.info(`Saved message to memory: ${conversationId}`);
  } catch (error) {
    logger.error('Error saving message to memory:', error.message, error.stack);
  }
}

// Helper function to call local AI model using direct subprocess
async function callLocalAIModel(message, history = [], language = 'english', conversationId = null, userId = null) {
  const systemPrompt = generateSystemPrompt(language);

  // Get conversation context from memory if available
  let conversationContext = [];
  if (conversationId) {
    conversationContext = await getConversationContext(conversationId, userId);
  }

  // Build full conversation context
  const fullPrompt = `${systemPrompt}\n\n${conversationContext.map(msg => `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`).join('\n')}\n\nUser: ${message}\nAssistant:`;

  // Try primary model first
  const modelsToTry = [AI_CONFIG.model, ...(AI_CONFIG.fallbackModels || [])];

  for (const model of modelsToTry) {
    try {
      logger.info(`Trying direct subprocess call with model ${model}`);
      console.log(`Trying model: ${model}`);

      // Use direct subprocess call like terminal
      const result = await runOllamaSubprocess(model, fullPrompt);

      if (result && result.trim()) {
        logger.info(`AI response received successfully from ${model}`);
        return result.trim();
      } else {
        throw new Error('Empty response from AI model');
      }

    } catch (error) {
      console.error(`Error with model ${model}:`, error.message);
      logger.error(`Error calling model ${model}:`, error.message);

      // Continue to next model if this one fails
      continue;
    }
  }

  // If all models fail, return fallback response
  console.error('All AI models failed');
  logger.error('All AI models failed, using fallback response');

  if (language === 'bengali') {
    return `দুঃখিত, আমি এখন আপনার প্রশ্নের উত্তর দিতে পারছি না। অনুগ্রহ করে কিছুক্ষণ পর আবার চেষ্টা করুন।`;
  } else {
    return `Sorry, I'm unable to answer your question right now. Please try again in a moment.`;
  }
}

// New function to run ollama as subprocess (like terminal)
function runOllamaSubprocess(model, prompt) {
  return new Promise((resolve, reject) => {
    console.log(`Running: ollama run ${model}`);

    const ollamaProcess = spawn('ollama', ['run', model], {
      stdio: ['pipe', 'pipe', 'pipe'],
      shell: true
    });

    let output = '';
    let errorOutput = '';

    // Send prompt to stdin
    ollamaProcess.stdin.write(prompt);
    ollamaProcess.stdin.end();

    // Collect stdout
    ollamaProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    // Collect stderr
    ollamaProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    // Handle process completion
    ollamaProcess.on('close', (code) => {
      if (code === 0) {
        console.log(`Ollama process completed successfully`);
        resolve(output);
      } else {
        console.error(`Ollama process failed with code ${code}`);
        console.error('Error output:', errorOutput);
        reject(new Error(`Ollama process failed: ${errorOutput}`));
      }
    });

    // Handle process errors
    ollamaProcess.on('error', (error) => {
      console.error('Ollama process error:', error);
      reject(error);
    });

    // Set timeout
    setTimeout(() => {
      ollamaProcess.kill();
      reject(new Error('Ollama process timeout'));
    }, 30000); // 30 seconds timeout
  });
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    model: AI_CONFIG.model,
    endpoint: AI_CONFIG.endpoint,
    url: AI_CONFIG.url
  });
});

// Model info endpoint
app.get('/api/model-info', (req, res) => {
  res.json({
    endpoint: AI_CONFIG.endpoint,
    model: AI_CONFIG.model,
    url: AI_CONFIG.url,
    responseTime: AI_CONFIG.responseTime
  });
});

// Main chat endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const {
      message,
      history = [],
      conversationId = null,
      userId = null
    } = req.body;

    if (!message || !message.trim()) {
      return res.status(400).json({
        error: 'Message is required'
      });
    }

    // Log the request
    logger.info(`Chat request received: ${message.substring(0, 100)}...`);

    // Detect language
    const language = detectLanguage(message);

    // Check cache first
    const cacheKey = `${message}_${language}_${JSON.stringify(history)}_${conversationId || 'no-context'}`;
    const cachedResponse = responseCache.get(cacheKey);

    if (cachedResponse && (Date.now() - cachedResponse.timestamp) < CACHE_DURATION) {
      logger.info('Serving response from cache');
      return res.json({
        response: cachedResponse.response,
        cached: true,
        language: language,
        model: AI_CONFIG.model
      });
    }

    // Call local AI model with memory context
    const aiResponse = await callLocalAIModel(message, history, language, conversationId, userId);

    // Save messages to memory if conversationId is provided
    if (conversationId) {
      await saveMessageToMemory(conversationId, 'user', message);
      await saveMessageToMemory(conversationId, 'assistant', aiResponse);
    }

    // Cache the response
    responseCache.set(cacheKey, {
      response: aiResponse,
      timestamp: Date.now()
    });

    // Clean old cache entries
    const now = Date.now();
    for (const [key, value] of responseCache.entries()) {
      if (now - value.timestamp > CACHE_DURATION) {
        responseCache.delete(key);
      }
    }

    logger.info(`Chat response sent successfully`);

    res.json({
      response: aiResponse,
      cached: false,
      language: language,
      model: AI_CONFIG.model,
      conversationId: conversationId
    });

  } catch (error) {
    logger.error('Error in chat endpoint:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: error.message
    });
  }
});

// Test endpoint to verify subprocess works
app.get('/api/test-model', async (req, res) => {
  try {
    console.log('Testing direct subprocess call...');

    const testPrompt = "Hello, can you respond with 'Test successful'?";
    const result = await runOllamaSubprocess('deepseek-coder:latest', testPrompt);

    res.json({
      success: true,
      response: result,
      message: 'Direct subprocess call successful'
    });
  } catch (error) {
    console.error('Test failed:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      message: 'Direct subprocess call failed'
    });
  }
});

// Streaming chat endpoint for real-time output
app.post('/api/chat/stream', async (req, res) => {
  try {
    const {
      message,
      history = [],
      conversationId = null,
      userId = null
    } = req.body;

    if (!message || !message.trim()) {
      return res.status(400).json({
        error: 'Message is required'
      });
    }

    // Set headers for streaming
    res.writeHead(200, {
      'Content-Type': 'text/plain',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type'
    });

    // Detect language
    const language = detectLanguage(message);
    const systemPrompt = generateSystemPrompt(language);

    // Get conversation context
    let conversationContext = [];
    if (conversationId) {
      conversationContext = await getConversationContext(conversationId, userId);
    }

    // Build full prompt
    const fullPrompt = `${systemPrompt}\n\n${conversationContext.map(msg => `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`).join('\n')}\n\nUser: ${message}\nAssistant:`;

    // Use streaming subprocess
    await streamOllamaResponse('deepseek-coder:latest', fullPrompt, res, conversationId, message);

  } catch (error) {
    logger.error('Error in streaming chat:', error);
    res.write(`data: ${JSON.stringify({ error: error.message })}\n\n`);
    res.end();
  }
});

// Function to stream ollama response in real-time
function streamOllamaResponse(model, prompt, res, conversationId, originalMessage) {
  return new Promise((resolve, reject) => {
    console.log(`Starting streaming with model: ${model}`);

    const ollamaProcess = spawn('ollama', ['run', model], {
      stdio: ['pipe', 'pipe', 'pipe'],
      shell: true
    });

    let fullResponse = '';

    // Send prompt to stdin
    ollamaProcess.stdin.write(prompt);
    ollamaProcess.stdin.end();

    // Stream stdout in real-time
    ollamaProcess.stdout.on('data', (data) => {
      const chunk = data.toString();
      fullResponse += chunk;

      // Send chunk to client
      res.write(`data: ${JSON.stringify({ chunk, type: 'content' })}\n\n`);
    });

    // Handle stderr
    ollamaProcess.stderr.on('data', (data) => {
      console.error('Ollama stderr:', data.toString());
    });

    // Handle completion
    ollamaProcess.on('close', async (code) => {
      if (code === 0) {
        console.log('Streaming completed successfully');

        // Save to memory if conversationId provided
        if (conversationId) {
          try {
            await saveMessageToMemory(conversationId, 'user', originalMessage);
            await saveMessageToMemory(conversationId, 'assistant', fullResponse);
          } catch (error) {
            console.error('Error saving to memory:', error);
          }
        }

        res.write(`data: ${JSON.stringify({ type: 'complete', fullResponse })}\n\n`);
        res.end();
        resolve(fullResponse);
      } else {
        console.error(`Streaming failed with code ${code}`);
        res.write(`data: ${JSON.stringify({ error: 'Process failed', code })}\n\n`);
        res.end();
        reject(new Error(`Process failed with code ${code}`));
      }
    });

    // Handle errors
    ollamaProcess.on('error', (error) => {
      console.error('Streaming process error:', error);
      res.write(`data: ${JSON.stringify({ error: error.message })}\n\n`);
      res.end();
      reject(error);
    });

    // Set timeout
    setTimeout(() => {
      ollamaProcess.kill();
      res.write(`data: ${JSON.stringify({ error: 'Timeout' })}\n\n`);
      res.end();
      reject(new Error('Streaming timeout'));
    }, 60000); // 60 seconds timeout
  });
}

// Error handling middleware
app.use((error, req, res, next) => {
  logger.error('Unhandled error:', error);
  res.status(500).json({
    error: 'Internal server error',
    message: 'Something went wrong'
  });
});

// Start server
app.listen(PORT, () => {
  logger.info(`AI Server running on port ${PORT}`);
  logger.info(`Using ${AI_CONFIG.endpoint} with model ${AI_CONFIG.model}`);
  logger.info(`AI URL: ${AI_CONFIG.url}`);
  console.log(`🚀 AI Server started on http://localhost:${PORT}`);
  console.log(`🏥 Health check: http://localhost:${PORT}/health`);
  console.log(`🤖 Model info: http://localhost:${PORT}/api/model-info`);
});

module.exports = app;