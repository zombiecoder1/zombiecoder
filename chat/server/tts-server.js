const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const winston = require('winston');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.TTS_SERVER_PORT || 3002;

// Logger configuration
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/tts-error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/tts-combined.log' }),
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

// Create audio directory
const audioDir = path.join(__dirname, '../public/audio');
if (!fs.existsSync(audioDir)) {
  fs.mkdirSync(audioDir, { recursive: true });
}

// Google TTS Configuration
const GOOGLE_TTS_CONFIG = {
  apiKey: process.env.GOOGLE_TTS_API_KEY,
  baseURL: 'https://texttospeech.googleapis.com/v1/text:synthesize',
  voices: {
    bengali: {
      languageCode: 'bn-IN',
      name: 'bn-IN-Standard-A',
      ssmlGender: 'FEMALE'
    },
    english: {
      languageCode: 'en-US',
      name: 'en-US-Standard-A',
      ssmlGender: 'FEMALE'
    },
    englishMale: {
      languageCode: 'en-US',
      name: 'en-US-Standard-B',
      ssmlGender: 'MALE'
    }
  }
};

// Helper function to detect language
function detectLanguage(text) {
  const bengaliRegex = /[\u0980-\u09FF]/;
  return bengaliRegex.test(text) ? 'bengali' : 'english';
}

// Helper function to generate SSML
function generateSSML(text, language = 'english') {
  const voice = GOOGLE_TTS_CONFIG.voices[language];
  
  // Clean text for SSML
  const cleanText = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');

  return `<speak>${cleanText}</speak>`;
}

// Helper function to call Google TTS API
async function callGoogleTTS(text, language = 'english', voiceName = null) {
  try {
    if (!GOOGLE_TTS_CONFIG.apiKey) {
      throw new Error('Google TTS API key not configured');
    }

    const detectedLang = detectLanguage(text);
    const voice = voiceName ? 
      GOOGLE_TTS_CONFIG.voices[voiceName] : 
      GOOGLE_TTS_CONFIG.voices[detectedLang];

    const requestBody = {
      input: {
        ssml: generateSSML(text, detectedLang)
      },
      voice: {
        languageCode: voice.languageCode,
        name: voice.name,
        ssmlGender: voice.ssmlGender
      },
      audioConfig: {
        audioEncoding: 'MP3',
        speakingRate: 0.9,
        pitch: 0,
        volumeGainDb: 0
      }
    };

    logger.info(`Calling Google TTS for ${detectedLang} text`);

    const response = await axios.post(
      `${GOOGLE_TTS_CONFIG.baseURL}?key=${GOOGLE_TTS_CONFIG.apiKey}`,
      requestBody,
      {
        timeout: 30000,
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    if (response.data && response.data.audioContent) {
      logger.info('Google TTS response received successfully');
      return response.data.audioContent;
    } else {
      throw new Error('Invalid response format from Google TTS');
    }

  } catch (error) {
    logger.error('Error calling Google TTS:', error.message);
    throw error;
  }
}

// Helper function to save audio file
function saveAudioFile(audioContent, filename) {
  try {
    const audioBuffer = Buffer.from(audioContent, 'base64');
    const filePath = path.join(audioDir, filename);
    fs.writeFileSync(filePath, audioBuffer);
    return `/audio/${filename}`;
  } catch (error) {
    logger.error('Error saving audio file:', error);
    throw error;
  }
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    apiKey: !!GOOGLE_TTS_CONFIG.apiKey,
    availableVoices: Object.keys(GOOGLE_TTS_CONFIG.voices)
  });
});

// TTS endpoint
app.post('/api/tts', async (req, res) => {
  try {
    const { text, language, voiceName } = req.body;

    if (!text || !text.trim()) {
      return res.status(400).json({ error: 'Text is required' });
    }

    // Log the request
    logger.info(`TTS request received: ${text.substring(0, 100)}...`);

    // Generate unique filename
    const timestamp = Date.now();
    const filename = `tts_${timestamp}.mp3`;

    // Call Google TTS
    const audioContent = await callGoogleTTS(text, language, voiceName);

    // Save audio file
    const audioUrl = saveAudioFile(audioContent, filename);

    logger.info(`TTS response sent successfully: ${filename}`);

    res.json({ 
      audioUrl: audioUrl,
      filename: filename,
      language: language || detectLanguage(text),
      text: text.substring(0, 100) + (text.length > 100 ? '...' : '')
    });

  } catch (error) {
    logger.error('Error in TTS endpoint:', error);
    
    // Fallback to browser TTS
    res.status(500).json({ 
      error: 'TTS service unavailable',
      message: 'Using browser TTS as fallback',
      fallback: true
    });
  }
});

// Get available voices
app.get('/api/voices', (req, res) => {
  res.json({
    voices: GOOGLE_TTS_CONFIG.voices,
    apiKeyConfigured: !!GOOGLE_TTS_CONFIG.apiKey
  });
});

// Stream audio endpoint
app.get('/audio/:filename', (req, res) => {
  const filename = req.params.filename;
  const filePath = path.join(audioDir, filename);

  if (!fs.existsSync(filePath)) {
    return res.status(404).json({ error: 'Audio file not found' });
  }

  const stat = fs.statSync(filePath);
  const fileSize = stat.size;
  const range = req.headers.range;

  if (range) {
    const parts = range.replace(/bytes=/, "").split("-");
    const start = parseInt(parts[0], 10);
    const end = parts[1] ? parseInt(parts[1], 10) : fileSize - 1;
    const chunksize = (end - start) + 1;
    const file = fs.createReadStream(filePath, { start, end });
    const head = {
      'Content-Range': `bytes ${start}-${end}/${fileSize}`,
      'Accept-Ranges': 'bytes',
      'Content-Length': chunksize,
      'Content-Type': 'audio/mpeg',
    };
    res.writeHead(206, head);
    file.pipe(res);
  } else {
    const head = {
      'Content-Length': fileSize,
      'Content-Type': 'audio/mpeg',
    };
    res.writeHead(200, head);
    fs.createReadStream(filePath).pipe(res);
  }
});

// Clean old audio files (older than 1 hour)
function cleanupOldAudioFiles() {
  try {
    const files = fs.readdirSync(audioDir);
    const now = Date.now();
    const oneHour = 60 * 60 * 1000;

    files.forEach(file => {
      const filePath = path.join(audioDir, file);
      const stats = fs.statSync(filePath);
      
      if (now - stats.mtime.getTime() > oneHour) {
        fs.unlinkSync(filePath);
        logger.info(`Cleaned up old audio file: ${file}`);
      }
    });
  } catch (error) {
    logger.error('Error cleaning up audio files:', error);
  }
}

// Cleanup every 30 minutes
setInterval(cleanupOldAudioFiles, 30 * 60 * 1000);

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
  logger.info(`TTS Server running on port ${PORT}`);
  logger.info(`Google TTS API Key: ${GOOGLE_TTS_CONFIG.apiKey ? 'Configured' : 'Not configured'}`);
  console.log(`🎤 TTS Server started on http://localhost:${PORT}`);
  console.log(`🏥 Health check: http://localhost:${PORT}/health`);
  console.log(`🎵 Audio directory: ${audioDir}`);
});

module.exports = app;
