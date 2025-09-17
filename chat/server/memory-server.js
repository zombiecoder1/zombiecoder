const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const winston = require('winston');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.MEMORY_SERVER_PORT || 3003;

// Logger configuration
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/memory-error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/memory-combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.NODE_ENV === 'production' 
    ? ['http://localhost:3000'] 
    : ['http://localhost:3000', 'http://127.0.0.1:3000'],
  credentials: true
}));
app.use(express.json({ limit: '10mb' }));

// Create memory directory
const memoryDir = path.join(__dirname, '../data/memory');
if (!fs.existsSync(memoryDir)) {
  fs.mkdirSync(memoryDir, { recursive: true });
}

// Memory storage structure
const memoryStorage = {
  users: new Map(), // userId -> userData
  sessions: new Map(), // sessionId -> sessionData
  conversations: new Map(), // conversationId -> conversationData
  globalContext: new Map() // global context for all users
};

// Memory configuration
const MEMORY_CONFIG = {
  maxConversationLength: 50, // Maximum messages per conversation
  maxHistoryDays: 30, // Keep history for 30 days
  maxUserSessions: 10, // Maximum sessions per user
  contextWindow: 20, // Number of recent messages to include in context
  cleanupInterval: 24 * 60 * 60 * 1000 // Cleanup every 24 hours
};

// Helper function to generate unique IDs
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Helper function to get user ID from session
function getUserId(sessionId) {
  const session = memoryStorage.sessions.get(sessionId);
  return session ? session.userId : null;
}

// Helper function to save memory to file
function saveMemoryToFile() {
  try {
    const memoryData = {
      users: Array.from(memoryStorage.users.entries()),
      sessions: Array.from(memoryStorage.sessions.entries()),
      conversations: Array.from(memoryStorage.conversations.entries()),
      globalContext: Array.from(memoryStorage.globalContext.entries()),
      timestamp: new Date().toISOString()
    };

    const filePath = path.join(memoryDir, `memory_${Date.now()}.json`);
    fs.writeFileSync(filePath, JSON.stringify(memoryData, null, 2));
    
    // Keep only last 5 memory files
    const files = fs.readdirSync(memoryDir).filter(f => f.startsWith('memory_'));
    if (files.length > 5) {
      files.sort().slice(0, files.length - 5).forEach(file => {
        fs.unlinkSync(path.join(memoryDir, file));
      });
    }

    logger.info('Memory saved to file successfully');
  } catch (error) {
    logger.error('Error saving memory to file:', error);
  }
}

// Helper function to load memory from file
function loadMemoryFromFile() {
  try {
    const files = fs.readdirSync(memoryDir).filter(f => f.startsWith('memory_'));
    if (files.length === 0) return;

    const latestFile = files.sort().pop();
    const filePath = path.join(memoryDir, latestFile);
    const memoryData = JSON.parse(fs.readFileSync(filePath, 'utf8'));

    memoryStorage.users = new Map(memoryData.users || []);
    memoryStorage.sessions = new Map(memoryData.sessions || []);
    memoryStorage.conversations = new Map(memoryData.conversations || []);
    memoryStorage.globalContext = new Map(memoryData.globalContext || []);

    logger.info('Memory loaded from file successfully');
  } catch (error) {
    logger.error('Error loading memory from file:', error);
  }
}

// Helper function to cleanup old data
function cleanupOldData() {
  try {
    const now = Date.now();
    const maxAge = MEMORY_CONFIG.maxHistoryDays * 24 * 60 * 60 * 1000;

    // Cleanup old conversations
    for (const [conversationId, conversation] of memoryStorage.conversations.entries()) {
      if (now - conversation.lastUpdated > maxAge) {
        memoryStorage.conversations.delete(conversationId);
        logger.info(`Cleaned up old conversation: ${conversationId}`);
      }
    }

    // Cleanup old sessions
    for (const [sessionId, session] of memoryStorage.sessions.entries()) {
      if (now - session.lastActivity > maxAge) {
        memoryStorage.sessions.delete(sessionId);
        logger.info(`Cleaned up old session: ${sessionId}`);
      }
    }

    // Limit conversation length
    for (const [conversationId, conversation] of memoryStorage.conversations.entries()) {
      if (conversation.messages.length > MEMORY_CONFIG.maxConversationLength) {
        conversation.messages = conversation.messages.slice(-MEMORY_CONFIG.maxConversationLength);
        conversation.lastUpdated = now;
        logger.info(`Truncated conversation: ${conversationId}`);
      }
    }

    // Save after cleanup
    saveMemoryToFile();
  } catch (error) {
    logger.error('Error during cleanup:', error);
  }
}

// Helper function to get conversation context
function getConversationContext(conversationId, limit = MEMORY_CONFIG.contextWindow) {
  try {
    const conversation = memoryStorage.conversations.get(conversationId);
    if (!conversation) return [];

    // Get recent messages
    const recentMessages = conversation.messages.slice(-limit);
    
    // Add user preferences and context
    const userId = conversation.userId;
    const user = memoryStorage.users.get(userId);
    
    let context = [];
    
    if (user && user.preferences) {
      context.push({
        role: 'system',
        content: `User preferences: ${JSON.stringify(user.preferences)}`
      });
    }

    // Add conversation summary if available
    if (conversation.summary) {
      context.push({
        role: 'system',
        content: `Previous conversation summary: ${conversation.summary}`
      });
    }

    // Add recent messages
    context.push(...recentMessages.map(msg => ({
      role: msg.role,
      content: msg.content
    })));

    return context;
  } catch (error) {
    logger.error('Error getting conversation context:', error);
    return [];
  }
}

// Helper function to update conversation summary
function updateConversationSummary(conversationId) {
  try {
    const conversation = memoryStorage.conversations.get(conversationId);
    if (!conversation || conversation.messages.length < 5) return;

    // Simple summary based on recent messages
    const recentMessages = conversation.messages.slice(-10);
    const topics = new Set();
    
    recentMessages.forEach(msg => {
      const words = msg.content.toLowerCase().split(/\s+/);
      words.forEach(word => {
        if (word.length > 3 && !['the', 'and', 'but', 'for', 'are', 'with', 'this', 'that'].includes(word)) {
          topics.add(word);
        }
      });
    });

    conversation.summary = `Topics discussed: ${Array.from(topics).slice(0, 5).join(', ')}`;
    conversation.lastUpdated = Date.now();
  } catch (error) {
    logger.error('Error updating conversation summary:', error);
  }
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    stats: {
      users: memoryStorage.users.size,
      sessions: memoryStorage.sessions.size,
      conversations: memoryStorage.conversations.size,
      globalContext: memoryStorage.globalContext.size
    }
  });
});

// Create or get user
app.post('/api/users', (req, res) => {
  try {
    const { userId, preferences = {} } = req.body;

    if (!userId) {
      return res.status(400).json({ error: 'User ID is required' });
    }

    let user = memoryStorage.users.get(userId);
    
    if (!user) {
      user = {
        id: userId,
        preferences,
        createdAt: new Date().toISOString(),
        lastActivity: Date.now(),
        sessions: []
      };
      memoryStorage.users.set(userId, user);
      logger.info(`Created new user: ${userId}`);
    } else {
      user.preferences = { ...user.preferences, ...preferences };
      user.lastActivity = Date.now();
      logger.info(`Updated user: ${userId}`);
    }

    res.json({ user });
  } catch (error) {
    logger.error('Error creating/updating user:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Create new session
app.post('/api/sessions', (req, res) => {
  try {
    const { userId, sessionId } = req.body;

    if (!userId) {
      return res.status(400).json({ error: 'User ID is required' });
    }

    const newSessionId = sessionId || generateId();
    const session = {
      id: newSessionId,
      userId,
      createdAt: new Date().toISOString(),
      lastActivity: Date.now(),
      conversationId: generateId()
    };

    memoryStorage.sessions.set(newSessionId, session);

    // Create conversation for this session
    const conversation = {
      id: session.conversationId,
      sessionId: newSessionId,
      userId,
      messages: [],
      createdAt: new Date().toISOString(),
      lastUpdated: Date.now(),
      summary: null
    };

    memoryStorage.conversations.set(session.conversationId, conversation);

    // Update user sessions
    const user = memoryStorage.users.get(userId);
    if (user) {
      user.sessions.push(newSessionId);
      if (user.sessions.length > MEMORY_CONFIG.maxUserSessions) {
        user.sessions = user.sessions.slice(-MEMORY_CONFIG.maxUserSessions);
      }
    }

    logger.info(`Created new session: ${newSessionId} for user: ${userId}`);
    res.json({ session, conversation });
  } catch (error) {
    logger.error('Error creating session:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Add message to conversation
app.post('/api/conversations/:conversationId/messages', (req, res) => {
  try {
    const { conversationId } = req.params;
    const { role, content, timestamp } = req.body;

    if (!role || !content) {
      return res.status(400).json({ error: 'Role and content are required' });
    }

    const conversation = memoryStorage.conversations.get(conversationId);
    if (!conversation) {
      return res.status(404).json({ error: 'Conversation not found' });
    }

    const message = {
      id: generateId(),
      role,
      content,
      timestamp: timestamp || new Date().toISOString()
    };

    conversation.messages.push(message);
    conversation.lastUpdated = Date.now();

    // Update session activity
    const session = memoryStorage.sessions.get(conversation.sessionId);
    if (session) {
      session.lastActivity = Date.now();
    }

    // Update conversation summary periodically
    if (conversation.messages.length % 10 === 0) {
      updateConversationSummary(conversationId);
    }

    logger.info(`Added message to conversation: ${conversationId}`);
    res.json({ message, conversation });
  } catch (error) {
    logger.error('Error adding message:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get conversation context
app.get('/api/conversations/:conversationId/context', (req, res) => {
  try {
    const { conversationId } = req.params;
    const { limit } = req.query;

    const context = getConversationContext(conversationId, parseInt(limit) || MEMORY_CONFIG.contextWindow);
    
    res.json({ 
      conversationId,
      context,
      messageCount: context.length
    });
  } catch (error) {
    logger.error('Error getting conversation context:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get user history
app.get('/api/users/:userId/history', (req, res) => {
  try {
    const { userId } = req.params;
    const { limit = 10 } = req.query;

    const user = memoryStorage.users.get(userId);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    const userConversations = Array.from(memoryStorage.conversations.values())
      .filter(conv => conv.userId === userId)
      .sort((a, b) => new Date(b.lastUpdated) - new Date(a.lastUpdated))
      .slice(0, parseInt(limit));

    res.json({
      userId,
      conversations: userConversations,
      totalConversations: userConversations.length
    });
  } catch (error) {
    logger.error('Error getting user history:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Update user preferences
app.put('/api/users/:userId/preferences', (req, res) => {
  try {
    const { userId } = req.params;
    const { preferences } = req.body;

    const user = memoryStorage.users.get(userId);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    user.preferences = { ...user.preferences, ...preferences };
    user.lastActivity = Date.now();

    logger.info(`Updated preferences for user: ${userId}`);
    res.json({ user });
  } catch (error) {
    logger.error('Error updating user preferences:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Delete conversation
app.delete('/api/conversations/:conversationId', (req, res) => {
  try {
    const { conversationId } = req.params;

    const conversation = memoryStorage.conversations.get(conversationId);
    if (!conversation) {
      return res.status(404).json({ error: 'Conversation not found' });
    }

    memoryStorage.conversations.delete(conversationId);
    
    // Update session
    const session = memoryStorage.sessions.get(conversation.sessionId);
    if (session) {
      session.conversationId = generateId();
      
      // Create new conversation
      const newConversation = {
        id: session.conversationId,
        sessionId: conversation.sessionId,
        userId: conversation.userId,
        messages: [],
        createdAt: new Date().toISOString(),
        lastUpdated: Date.now(),
        summary: null
      };
      
      memoryStorage.conversations.set(session.conversationId, newConversation);
    }

    logger.info(`Deleted conversation: ${conversationId}`);
    res.json({ success: true });
  } catch (error) {
    logger.error('Error deleting conversation:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Error handling middleware
app.use((error, req, res, next) => {
  logger.error('Unhandled error:', error);
  res.status(500).json({ 
    error: 'Internal server error',
    message: 'Something went wrong'
  });
});

// Load memory on startup
loadMemoryFromFile();

// Setup periodic tasks
setInterval(cleanupOldData, MEMORY_CONFIG.cleanupInterval);
setInterval(saveMemoryToFile, 5 * 60 * 1000); // Save every 5 minutes

// Start server
app.listen(PORT, () => {
  logger.info(`Memory Server running on port ${PORT}`);
  console.log(`🧠 Memory Server started on http://localhost:${PORT}`);
  console.log(`🏥 Health check: http://localhost:${PORT}/health`);
  console.log(`📁 Memory directory: ${memoryDir}`);
});

module.exports = app;
