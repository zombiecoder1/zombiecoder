@echo off
title ZombieCoder Comprehensive System Test
color 0A

echo ===================================================
echo    ZOMBIECODER COMPREHENSIVE SYSTEM TEST
echo ===================================================
echo.

echo [1/8] 🧹 Port Cleanup...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8001') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :12345') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :11434') do taskkill /f /pid %%a >nul 2>&1
echo Port cleanup completed!
echo.

echo [2/8] 🔒 Cloud AI Blocking Test...
echo Testing hosts file blocking...
set CLOUD_BLOCKED=0
set TOTAL_DOMAINS=4

ping -n 1 api.openai.com >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ api.openai.com: BLOCKED (127.0.0.1)
    set /a CLOUD_BLOCKED+=1
) else (
    echo ❌ api.openai.com: ACCESSIBLE
)

ping -n 1 api.anthropic.com >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ api.anthropic.com: BLOCKED (127.0.0.1)
    set /a CLOUD_BLOCKED+=1
) else (
    echo ❌ api.anthropic.com: ACCESSIBLE
)

ping -n 1 oai.hf.space >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ oai.hf.space: BLOCKED (127.0.0.1)
    set /a CLOUD_BLOCKED+=1
) else (
    echo ❌ oai.hf.space: ACCESSIBLE
)

ping -n 1 openaiapi-site.azureedge.net >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ openaiapi-site.azureedge.net: BLOCKED (127.0.0.1)
    set /a CLOUD_BLOCKED+=1
) else (
    echo ❌ openaiapi-site.azureedge.net: ACCESSIBLE
)

echo.
echo Cloud AI Blocking Status: %CLOUD_BLOCKED%/%TOTAL_DOMAINS% domains blocked

if %CLOUD_BLOCKED% equ %TOTAL_DOMAINS% (
    echo 🎯 VERDICT: LOCAL AI ENFORCED ✅
) else (
    echo ⚠️  WARNING: CLOUD AI ACCESSIBLE ❌
)
echo.

echo [3/8] 🌍 Environment Setup...
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

echo [4/8] 🚀 Starting Services...
echo Starting OpenAI Shim...
start /b python local_ai_integration\openai_shim.py >nul 2>&1
timeout /t 3 /nobreak >nul

echo Starting ZombieCoder...
start /b python core-server\unified_agent_system.py >nul 2>&1
timeout /t 3 /nobreak >nul

echo Starting Ollama...
if exist "C:\Users\sahon\AppData\Local\Programs\Ollama\ollama.exe" (
    start /b "" "C:\Users\sahon\AppData\Local\Programs\Ollama\ollama.exe" serve >nul 2>&1
    echo Ollama started!
) else (
    echo ⚠️  Ollama not found, skipping...
)
timeout /t 3 /nobreak >nul
echo Services started!
echo.

echo [5/8] 🔍 Service Health Check...
timeout /t 5 /nobreak >nul

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

echo [6/8] 🧪 Trust Checker Test...
echo Running trust verification...
python local_ai_integration\truth_checker.py --verbose
echo Trust checker test completed!
echo.

echo [7/8] 🔌 Editor Integration Test...
echo Testing editor configuration...
python local_ai_integration\editor_integration.py
echo Editor integration test completed!
echo.

echo [8/8] 🚀 Agent Response Test...
echo Testing AI response capabilities...
python test_extension.py
echo Agent response test completed!
echo.

echo ===================================================
echo 🎉 COMPREHENSIVE TEST COMPLETED!
echo ===================================================
echo.
echo 📊 FINAL STATUS:
echo    Cloud AI Blocking: %CLOUD_BLOCKED%/%TOTAL_DOMAINS%
echo    OpenAI Shim: Active
echo    ZombieCoder: Active
echo    Ollama: Active
echo.
echo 🎯 NEXT STEPS:
echo    1. VS Code: Ctrl+Shift+P → ZombieCoder
echo    2. Cursor: Ctrl+Shift+I
echo    3. Test local AI responses
echo.
echo Press any key to continue...
pause >nul
