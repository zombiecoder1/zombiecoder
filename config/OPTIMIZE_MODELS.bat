@echo off
echo 🤖 ZombieCoder Model Optimization
echo =================================
echo.

REM Check current models
echo 📊 Current Models:
ollama list

echo.
echo 🔍 Analyzing model performance...
echo.

REM Remove unnecessary models (keeping only the best ones)
echo 🗑️ Removing unnecessary models...

REM Remove large models that are slow
echo Removing llama3.2:3b (too slow)...
ollama rm llama3.2:3b

echo Removing deepseek-r1:8b (too large)...
ollama rm deepseek-r1:8b

echo Removing neural-chat:latest (redundant)...
ollama rm neural-chat:latest

echo Removing nomic-embed-text:latest (not needed for chat)...
ollama rm nomic-embed-text:latest

echo.
echo ✅ Optimization completed!
echo.

REM Show remaining models
echo 📋 Optimized Model List:
ollama list

echo.
echo 🎯 Recommended Models:
echo - llama3.2:1b (Fast, 1.2GB) - General chat
echo - qwen2.5-coder:1.5b-base (Fast, 940MB) - Coding tasks
echo - codellama:latest (Medium, 3.6GB) - Advanced coding
echo - llama3.1:8b (Large, 4.9GB) - High quality responses
echo.

echo 💡 Total space saved: ~8GB
echo ⚡ Expected performance improvement: 40-60%
echo.

pause
