@echo off
echo 🚀 Starting Ollama Server...
echo.

REM Check if Ollama is already running
netstat -an | findstr ":11434" >nul
if %errorlevel% equ 0 (
    echo ✅ Ollama is already running on port 11434
    goto :check_models
)

REM Try to start Ollama
echo 🔧 Attempting to start Ollama...
ollama serve >nul 2>&1 &
timeout /t 3 /nobreak >nul

REM Check if Ollama started successfully
netstat -an | findstr ":11434" >nul
if %errorlevel% equ 0 (
    echo ✅ Ollama started successfully
) else (
    echo ❌ Failed to start Ollama
    echo Please make sure Ollama is installed and in your PATH
    pause
    exit /b 1
)

:check_models
echo.
echo 📋 Checking available models...
curl -s http://localhost:11434/api/tags
if %errorlevel% neq 0 (
    echo ❌ Cannot connect to Ollama API
    pause
    exit /b 1
)

echo.
echo 🎯 Ollama is ready!
echo 📍 URL: http://localhost:11434
echo.
pause
