@echo off
title ZombieCoder Complete Local AI Launcher
color 0A

echo ===================================================
echo    ZOMBIECODER COMPLETE LOCAL AI LAUNCHER
echo ===================================================
echo.

echo [1/7] 🧹 Cleaning up ports...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8001') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :12345') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :11434') do taskkill /f /pid %%a >nul 2>&1
echo Port cleanup completed!
echo.

echo [2/7] 🔒 Verifying Cloud AI Blocking...
echo Checking hosts file for cloud domain blocking...
set CLOUD_BLOCKED=0
set TOTAL_DOMAINS=4

nslookup api.openai.com >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ api.openai.com: ACCESSIBLE
) else (
    echo ✅ api.openai.com: BLOCKED
    set /a CLOUD_BLOCKED+=1
)

nslookup api.anthropic.com >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ api.anthropic.com: ACCESSIBLE
) else (
    echo ✅ api.anthropic.com: BLOCKED
    set /a CLOUD_BLOCKED+=1
)

nslookup oai.hf.space >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ oai.hf.space: ACCESSIBLE
) else (
    echo ✅ oai.hf.space: BLOCKED
    set /a CLOUD_BLOCKED+=1
)

nslookup openaiapi-site.azureedge.net >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ openaiapi-site.azureedge.net: ACCESSIBLE
) else (
    echo ✅ openaiapi-site.azureedge.net: BLOCKED
    set /a CLOUD_BLOCKED+=1
)

echo.
echo Cloud AI Blocking Status: %CLOUD_BLOCKED%/%TOTAL_DOMAINS% domains blocked

if %CLOUD_BLOCKED% equ %TOTAL_DOMAINS% (
    echo 🎯 VERDICT: LOCAL AI ENFORCED ✅
) else (
    echo ⚠️  WARNING: CLOUD AI ACCESSIBLE ❌
    echo Please configure hosts file to block cloud domains
)
echo.

echo [3/7] 🌍 Setting Environment Variables...
set OPENAI_API_BASE=http://127.0.0.1:8001/v1
set OPENAI_API_KEY=local-ai-key
set FORCE_LOCAL_AI=true
set LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1
set ZOMBIECODER_HOST=http://127.0.0.1:12345
set OLLAMA_HOST=http://127.0.0.1:11434
set AI_PROVIDER=zombiecoder
set AI_MODEL=local-llama
set EDITOR_MODE=local_ai
echo Environment variables set!
echo.

echo [4/7] 🚀 Starting OpenAI Shim Server...
start "OpenAI Shim" /min python local_ai_integration\openai_shim.py
timeout /t 3 /nobreak >nul
echo OpenAI Shim started on port 8001
echo.

echo [5/7] 🤖 Starting ZombieCoder Unified Agent System...
start "ZombieCoder" /min python core-server\unified_agent_system.py
timeout /t 3 /nobreak >nul
echo ZombieCoder started on port 12345
echo.

echo [6/7] 🦙 Starting Ollama...
"C:\Users\sahon\AppData\Local\Programs\Ollama\ollama.exe" serve >nul 2>&1
if %errorlevel% equ 0 (
    echo Ollama started on port 11434
) else (
    echo ⚠️  Ollama failed to start
)
echo.

echo [7/7] 🔍 Checking Service Status...
timeout /t 5 /nobreak >nul

echo.
echo Checking OpenAI Shim (Port 8001)...
curl -s http://127.0.0.1:8001/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ OpenAI Shim: RUNNING
) else (
    echo ❌ OpenAI Shim: NOT RESPONDING
)

echo Checking ZombieCoder (Port 12345)...
curl -s http://127.0.0.1:12345/status >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ ZombieCoder: RUNNING
) else (
    echo ❌ ZombieCoder: NOT RESPONDING
)

echo Checking Ollama (Port 11434)...
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama: RUNNING
) else (
    echo ❌ Ollama: NOT RESPONDING
)

echo.
echo ===================================================
echo 🎉 ZOMBIECODER LOCAL AI SYSTEM READY!
echo ===================================================
echo.
echo 📱 Cursor AI: Ctrl+Shift+I
echo 💻 VS Code: Ctrl+Shift+P → ZombieCoder
echo 🌐 OpenAI Shim: http://127.0.0.1:8001
echo 🤖 ZombieCoder: http://127.0.0.1:12345
echo 🦙 Ollama: http://127.0.0.1:11434
echo.
echo Press any key to continue...
pause >nul
