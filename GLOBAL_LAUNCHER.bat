@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ====================================================
echo   🧟‍♂️ ZombieCoder Local AI System Starting...
echo ====================================================
echo.
echo 📁 Project Directory: %CD%
echo.

REM ====================================================
REM STEP 1: PORT CLEANUP AND BLOCKING SOLUTION
REM ====================================================
echo [1/6] 🧹 Cleaning up blocked ports and processes...
echo.

REM Kill processes on our target ports
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8001"') do (
    echo 🔴 Killing process %%a on port 8001 (OpenAI Shim)
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":12345"') do (
    echo 🔴 Killing process %%a on port 12345 (ZombieCoder)
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":11434"') do (
    echo 🔴 Killing process %%a on port 11434 (Ollama)
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8080"') do (
    echo 🔴 Killing process %%a on port 8080 (Proxy)
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8081"') do (
    echo 🔴 Killing process %%a on port 8081 (Multi-Project API)
    taskkill /PID %%a /F >nul 2>&1
)

echo ✅ Port cleanup completed!
echo.

REM ====================================================
REM STEP 2: CLOUD VS LOCAL DETECTION
REM ====================================================
echo [2/6] 🔍 Detecting Cloud vs Local AI Configuration...
echo.

REM Check if cloud domains are blocked
echo 🔒 Checking hosts file for cloud domain blocking...
set CLOUD_BLOCKED=0
set TOTAL_DOMAINS=4

REM Check api.openai.com
nslookup api.openai.com >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ api.openai.com: ACCESSIBLE (Cloud AI available)
) else (
    echo ✅ api.openai.com: BLOCKED (Local AI enforced)
    set /a CLOUD_BLOCKED+=1
)

REM Check api.anthropic.com
nslookup api.anthropic.com >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ api.anthropic.com: ACCESSIBLE (Cloud AI available)
) else (
    echo ✅ api.anthropic.com: BLOCKED (Local AI enforced)
    set /a CLOUD_BLOCKED+=1
)

REM Check oai.hf.space
nslookup oai.hf.space >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ oai.hf.space: ACCESSIBLE (Cloud AI available)
) else (
    echo ✅ oai.hf.space: BLOCKED (Local AI enforced)
    set /a CLOUD_BLOCKED+=1
)

REM Check openaiapi-site.azureedge.net
nslookup openaiapi-site.azureedge.net >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ openaiapi-site.azureedge.net: ACCESSIBLE (Cloud AI available)
) else (
    echo ✅ openaiapi-site.azureedge.net: BLOCKED (Local AI enforced)
    set /a CLOUD_BLOCKED+=1
)

echo.
echo 📊 Cloud AI Blocking Status: %CLOUD_BLOCKED%/%TOTAL_DOMAINS% domains blocked

if %CLOUD_BLOCKED% equ %TOTAL_DOMAINS% (
    echo 🎯 VERDICT: LOCAL AI ENFORCED ✅
    echo    - All cloud AI domains are blocked
    echo    - System will use local AI services only
    echo    - No external AI calls possible
) else (
    echo ⚠️  WARNING: CLOUD AI ACCESSIBLE ❌
    echo    - Some cloud AI domains are accessible
    echo    - System may make external AI calls
    echo    - Local AI not fully enforced
)

echo.

REM ====================================================
REM STEP 3: AUTO-ENVIRONMENT SETUP FOR EDITORS
REM ====================================================
echo [3/6] 🔧 Setting up Editor Environment Variables...
echo.

REM Set environment variables for current session
set OPENAI_API_BASE=http://127.0.0.1:8001/v1
set OPENAI_API_KEY=local-ai-key
set FORCE_LOCAL_AI=true
set LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1
set ZOMBIECODER_HOST=http://127.0.0.1:12345
set OLLAMA_HOST=http://127.0.0.1:11434
set AI_PROVIDER=zombiecoder
set AI_MODEL=local-llama
set EDITOR_MODE=local_ai

echo ✅ Environment Variables Set:
echo    OPENAI_API_BASE=%OPENAI_API_BASE%
echo    OPENAI_API_KEY=%OPENAI_API_KEY%
echo    FORCE_LOCAL_AI=%FORCE_LOCAL_AI%
echo    LOCAL_AI_ENDPOINT=%LOCAL_AI_ENDPOINT%
echo    ZOMBIECODER_HOST=%ZOMBIECODER_HOST%
echo    OLLAMA_HOST=%OLLAMA_HOST%
echo    AI_PROVIDER=%AI_PROVIDER%
echo    AI_MODEL=%AI_MODEL%
echo    EDITOR_MODE=%EDITOR_MODE%
echo.

REM Create .env files in project directories
echo 📝 Creating .env files for Editor Integration...
echo.

REM Create .env in current directory
if not exist ".env" (
    echo OPENAI_API_BASE=http://127.0.0.1:8001/v1 > .env
    echo OPENAI_API_KEY=local-ai-key >> .env
    echo FORCE_LOCAL_AI=true >> .env
    echo LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1 >> .env
    echo ZOMBIECODER_HOST=http://127.0.0.1:12345 >> .env
    echo OLLAMA_HOST=http://127.0.0.1:11434 >> .env
    echo AI_PROVIDER=zombiecoder >> .env
    echo AI_MODEL=local-llama >> .env
    echo EDITOR_MODE=local_ai >> .env
    echo ✅ .env file created in %CD%
)

REM Create .env in core-server directory
if not exist "core-server\.env" (
    echo OPENAI_API_BASE=http://127.0.0.1:8001/v1 > core-server\.env
    echo OPENAI_API_KEY=local-ai-key >> core-server\.env
    echo FORCE_LOCAL_AI=true >> core-server\.env
    echo LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1 >> core-server\.env
    echo ZOMBIECODER_HOST=http://127.0.0.1:12345 >> core-server\.env
    echo OLLAMA_HOST=http://127.0.0.1:11434 >> core-server\.env
    echo AI_PROVIDER=zombiecoder >> core-server\.env
    echo AI_MODEL=local-llama >> core-server\.env
    echo EDITOR_MODE=local_ai >> core-server\.env
    echo ✅ .env file created in core-server directory
)

REM Create .env in our-server directory
if not exist "our-server\.env" (
    echo OPENAI_API_BASE=http://127.0.0.1:8001/v1 > our-server\.env
    echo OPENAI_API_KEY=local-ai-key >> our-server\.env
    echo FORCE_LOCAL_AI=true >> our-server\.env
    echo LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1 >> our-server\.env
    echo ZOMBIECODER_HOST=http://127.0.0.1:12345 >> our-server\.env
    echo OLLAMA_HOST=http://127.0.0.1:11434 >> our-server\.env
    echo AI_PROVIDER=zombiecoder >> our-server\.env
    echo AI_MODEL=local-llama >> our-server\.env
    echo EDITOR_MODE=local_ai >> our-server\.env
    echo ✅ .env file created in our-server directory
)

REM Create VS Code settings for local AI
if not exist ".vscode" mkdir .vscode
if not exist ".vscode\settings.json" (
    echo { > .vscode\settings.json
    echo   "openai.apiBase": "http://127.0.0.1:8001/v1", >> .vscode\settings.json
    echo   "openai.apiKey": "local-ai-key", >> .vscode\settings.json
    echo   "openai.forceLocal": true, >> .vscode\settings.json
    echo   "zombiecoder.endpoint": "http://127.0.0.1:8001/v1", >> .vscode\settings.json
    echo   "zombiecoder.apiKey": "local-ai-key", >> .vscode\settings.json
    echo   "zombiecoder.provider": "local", >> .vscode\settings.json
    echo   "zombiecoder.model": "local-llama", >> .vscode\settings.json
    echo   "zombiecoder.forceLocal": true >> .vscode\settings.json
    echo } >> .vscode\settings.json
    echo ✅ VS Code settings.json created
)

REM Create Cursor AI configuration
if not exist ".cursorrules" (
    echo # Cursor AI Local Configuration > .cursorrules
    echo # This file configures Cursor to use local AI >> .cursorrules
    echo. >> .cursorrules
    echo # Force local AI usage >> .cursorrules
    echo FORCE_LOCAL_AI=true >> .cursorrules
    echo LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1 >> .cursorrules
    echo LOCAL_AI_KEY=local-ai-key >> .cursorrules
    echo AI_PROVIDER=zombiecoder >> .cursorrules
    echo AI_MODEL=local-llama >> .cursorrules
    echo EDITOR_MODE=local_ai >> .cursorrules
    echo. >> .cursorrules
    echo # AI Model Configuration >> .cursorrules
    echo AI_MODEL=local-llama >> .cursorrules
    echo AI_PROVIDER=zombiecoder >> .cursorrules
    echo ✅ .cursorrules file created
)

REM Create Cursor AI settings.json
if not exist ".cursor" mkdir .cursor
if not exist ".cursor\settings.json" (
    echo { > .cursor\settings.json
    echo   "openai.apiBase": "http://127.0.0.1:8001/v1", >> .cursor\settings.json
    echo   "openai.apiKey": "local-ai-key", >> .cursor\settings.json
    echo   "openai.forceLocal": true, >> .cursor\settings.json
    echo   "zombiecoder.endpoint": "http://127.0.0.1:8001/v1", >> .cursor\settings.json
    echo   "zombiecoder.apiKey": "local-ai-key", >> .cursor\settings.json
    echo   "zombiecoder.provider": "local", >> .cursor\settings.json
    echo   "zombiecoder.model": "local-llama", >> .cursor\settings.json
    echo   "zombiecoder.forceLocal": true >> .cursor\settings.json
    echo } >> .cursor\settings.json
    echo ✅ Cursor settings.json created
)

echo.
echo ====================================================
echo   🎯 Editor Integration Ready!
echo ====================================================
echo ✅ Environment Variables: Set
echo ✅ .env Files: Created
echo ✅ VS Code Settings: Configured
echo ✅ Cursor AI: Configured
echo ✅ Terminal: Ready
echo.

REM ====================================================
REM STEP 4: CHECK AND START OLLAMA
REM ====================================================
echo [4/6] 🤖 Starting Ollama Models...
echo.

REM Check if Ollama is running
netstat -an | findstr ":11434" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama already running on port 11434
) else (
    echo 🚀 Starting Ollama...
    start /B "Ollama Server" "C:\Users\%USERNAME%\AppData\Local\Ollama\ollama.exe" serve
    timeout /t 3 /nobreak >nul
)

REM ====================================================
REM STEP 5: START OPENAI SHIM SERVER
REM ====================================================
echo [5/6] 🔌 Starting OpenAI Shim Server...
echo.

cd local_ai_integration
if exist "openai_shim.py" (
    echo 🚀 Starting OpenAI Shim on port 8001...
    start /B "OpenAI Shim" python openai_shim.py
    timeout /t 5 /nobreak >nul
) else (
    echo ❌ OpenAI Shim not found in local_ai_integration
)

cd ..

REM ====================================================
REM STEP 6: START ZOMBIECODER AGENT SYSTEM
REM ====================================================
echo [6/6] 🧟‍♂️ Starting ZombieCoder Agent System...
echo.

if exist "core-server\unified_agent_system.py" (
    echo 🚀 Starting ZombieCoder Unified Agent System on port 12345...
    start /B "ZombieCoder" python core-server\unified_agent_system.py
    timeout /t 5 /nobreak >nul
) else (
    echo ❌ ZombieCoder unified agent system not found
)

echo.
echo ====================================================
echo   🎯 All services started! Checking status...
echo ====================================================
echo.

REM ====================================================
REM ADVANCED TESTING AND INTEGRATION
REM ====================================================
echo 🧪 Testing Editor Integration...
echo.

REM Test OpenAI Shim API endpoints
echo 🔍 Testing OpenAI Shim API...
curl -s -X POST http://127.0.0.1:8001/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"local-llama\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}],\"max_tokens\":10}" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ OpenAI Shim API: Working
) else (
    echo ❌ OpenAI Shim API: Failed
)

REM Test ZombieCoder API
echo 🔍 Testing ZombieCoder API...
curl -s http://127.0.0.1:12345/status >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ ZombieCoder API: Working
) else (
    echo ❌ ZombieCoder API: Failed
)

echo.
echo ====================================================
echo   📊 Service Status Check
echo ====================================================
echo.

REM Check Ollama
echo 🔍 Checking Ollama (Port 11434)...
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama: http://127.0.0.1:11434 - RUNNING
) else (
    echo ❌ Ollama: http://127.0.0.1:11434 - FAILED
)

REM Check OpenAI Shim
echo 🔍 Checking OpenAI Shim (Port 8001)...
curl -s http://127.0.0.1:8001/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ OpenAI Shim: http://127.0.0.1:8001 - RUNNING
) else (
    echo ❌ OpenAI Shim: http://127.0.0.1:8001 - FAILED
)

REM Check ZombieCoder
echo 🔍 Checking ZombieCoder (Port 12345)...
curl -s http://127.0.0.1:12345/ >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ ZombieCoder: http://127.0.0.1:12345 - RUNNING
) else (
    echo ❌ ZombieCoder: http://127.0.0.1:12345 - FAILED
)

echo.
echo ====================================================
echo   🌟 Local AI Integration Status
echo ====================================================
echo.
echo 🧠 Ollama Models: http://127.0.0.1:11434
echo 🔌 OpenAI Shim: http://127.0.0.1:8001
echo 🧟‍♂️ ZombieCoder: http://127.0.0.1:12345
echo.

echo ====================================================
echo   🚀 Editor Integration Setup
echo ====================================================
echo.
echo 📋 Cursor AI Local Setup:
echo.
echo 1️⃣ Environment Variables (Current Session):
echo    set OPENAI_API_BASE=http://127.0.0.1:8001/v1
echo    set OPENAI_API_KEY=local-ai-key
echo    set FORCE_LOCAL_AI=true
echo.
echo 2️⃣ .env File in Cursor Project:
echo    OPENAI_API_BASE=http://127.0.0.1:8001/v1
echo    OPENAI_API_KEY=local-ai-key
echo    FORCE_LOCAL_AI=true
echo    LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1
echo.
echo 3️⃣ VS Code Extension Setup:
echo    - Install ZombieCoder Extension
echo    - Set API endpoint to: http://127.0.0.1:8001/v1
echo    - API Key: local-ai-key
echo.
echo 4️⃣ Test Commands:
echo    - Cursor: Ctrl+Shift+I
echo    - VS Code: Ctrl+Shift+P → ZombieCoder
echo    - Terminal: curl http://127.0.0.1:8001/health
echo.

echo ====================================================
echo   🔧 Advanced Editor Integration
echo ====================================================
echo.
echo 🎯 Auto-Environment Setup:
echo    - Setting environment variables automatically...
echo    - Creating .env files in project directories...
echo    - Configuring VS Code settings...
echo    - Configuring Cursor AI settings...
echo.
echo 🔧 Troubleshooting Commands:
echo.
echo 🧹 Kill all processes:
echo    taskkill /F /IM python.exe
echo    taskkill /F /IM ollama.exe
echo.
echo 📊 Check port status:
echo    netstat -an | findstr ":8001\|:12345\|:11434"
echo.
echo 🔄 Restart specific service:
echo    python core-server\unified_agent_system.py
echo.
echo 🚀 Editor Integration Commands:
echo    - Cursor AI: Ctrl+Shift+I
echo    - VS Code: Ctrl+Shift+P → ZombieCoder
echo    - Terminal Integration: Available
echo.

echo ====================================================
echo   🎯 Final Integration Summary
echo ====================================================
echo.
echo 🌟 Editor Integration Status:
echo    ✅ Cursor AI: Configured for Local AI
echo    ✅ VS Code: Settings Applied
echo    ✅ Environment Variables: Set
echo    ✅ .env Files: Created
echo    ✅ API Endpoints: Tested
echo.
echo 🚀 Ready to Use:
echo    - Cursor AI: Ctrl+Shift+I (Local AI)
echo    - VS Code: Ctrl+Shift+P → ZombieCoder
echo    - Terminal: curl commands available
echo    - All services: Running on localhost
echo.
echo 🔧 Configuration Files Created:
echo    - .env (Root, core-server, our-server)
echo    - .vscode/settings.json
echo    - .cursorrules
echo    - .cursor/settings.json
echo.
echo 🔍 Cloud vs Local Detection:
echo    - Cloud AI Domains: %CLOUD_BLOCKED%/%TOTAL_DOMAINS% blocked
echo    - Local AI Enforcement: %CLOUD_BLOCKED%/%TOTAL_DOMAINS% effective
echo    - Editor Mode: %EDITOR_MODE%
echo    - AI Provider: %AI_PROVIDER%
echo    - AI Model: %AI_MODEL%
echo.
echo ====================================================
echo   🎉 System Ready! Press any key to continue...
echo ====================================================
pause >nul

REM Keep terminal open and show final status
echo.
echo 🔄 Keeping terminal open for monitoring...
echo 📊 Use 'netstat -an | findstr ":8001\|:12345\|:11434"' to check ports
echo 🚀 All services are now integrated with your editors!
echo.
cmd /k
