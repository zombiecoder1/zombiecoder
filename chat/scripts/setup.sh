#!/bin/bash

echo "🚀 Setting up Chat Interface with AI & TTS Servers..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p server
mkdir -p public/audio
mkdir -p data/memory

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
  echo "📝 Creating .env file from env.example..."
  cp env.example .env
  echo "✅ Created .env file - please update with your configuration"
else
  echo "✅ .env file already exists"
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/setup.sh
chmod +x scripts/start-all.js
chmod +x scripts/check-models.js

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Update .env file with your configuration"
echo "2. Start your local AI model (Ollama, LM Studio, etc.)"
echo "3. Run: npm run check-models (to test available models)"
echo "4. Run: npm run start-all (to start all services)"
echo ""
echo "🔗 URLs:"
echo "- Chat Interface: http://localhost:3000"
echo "- AI Server: http://localhost:3001/health"
echo "- Memory Server: http://localhost:3003/health"
echo "- TTS Server: http://localhost:3002/health"
echo ""
