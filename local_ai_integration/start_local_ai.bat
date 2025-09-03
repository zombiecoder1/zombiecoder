@echo off
title ZombieCoder Local AI System
echo ====================================================
echo    🚀 ZombieCoder Local AI System Starting...
echo ====================================================
echo.
echo 📁 Project Directory: C:\zombiecoder\local_ai_integration\.
echo.
cd /d "C:\zombiecoder\local_ai_integration\."

echo [1/3] Starting OpenAI Shim Server...
start "OpenAI Shim" cmd /k "cd /d local_ai_integration ^& python openai_shim.py"
timeout /t 3 /nobreak >nul

echo [2/3] Starting ZombieCoder Agent System...
start "ZombieCoder Agents" cmd /k "cd /d core-server ^& python advanced_agent_system.py"
timeout /t 3 /nobreak >nul

echo [3/3] Starting Ollama Models...
start "Ollama Models" cmd /k "ollama serve"

echo ✅ All services started!
echo.
echo 🌐 OpenAI Shim: http://127.0.0.1:8001
echo 🤖 ZombieCoder: http://127.0.0.1:12345
echo 🧠 Ollama: http://127.0.0.1:11434
echo.
pause
