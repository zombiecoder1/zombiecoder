@echo off
echo 🚀 Starting Enhanced Chat Interface with Prompt Orchestration System
echo Editor ভাই-এর জন্য Real-time Chat System
echo ================================================================

echo.
echo 📋 Starting services in sequence:
echo 1. AI Server (Port 3001)
echo 2. Memory Server (Port 3003)  
echo 3. TTS Server (Port 3002)
echo 4. Orchestrator Server (Port 3004)
echo 5. Next.js Server (Port 3000)
echo.

echo 🤖 Starting AI Server...
start "AI Server" cmd /k "npm run server"

timeout /t 3 /nobreak >nul

echo 🧠 Starting Memory Server...
start "Memory Server" cmd /k "npm run memory"

timeout /t 3 /nobreak >nul

echo 🎤 Starting TTS Server...
start "TTS Server" cmd /k "npm run tts"

timeout /t 3 /nobreak >nul

echo 🎯 Starting Orchestrator Server...
start "Orchestrator Server" cmd /k "npm run orchestrator"

timeout /t 5 /nobreak >nul

echo 🌐 Starting Next.js Development Server...
start "Next.js Server" cmd /k "npm run dev"

timeout /t 5 /nobreak >nul

echo.
echo 🎉 All servers started successfully!
echo.
echo 📱 Chat Interface: http://localhost:3000
echo 🤖 AI Server: http://localhost:3001/health
echo 🧠 Memory Server: http://localhost:3003/health
echo 🎤 TTS Server: http://localhost:3002/health
echo 🎯 Orchestrator Server: http://localhost:3004/api/health
echo.
echo 💡 Close this window to stop all servers
echo 💡 Or close individual server windows to stop specific services
echo.
echo Press any key to open the chat interface...
pause >nul

start http://localhost:3000

echo.
echo 🚀 Enhanced Chat Interface is now running!
echo Editor ভাই-এর জন্য Smart Prompt Orchestration System is ready!
echo.
pause
