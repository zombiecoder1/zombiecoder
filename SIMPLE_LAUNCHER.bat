@echo off
echo Starting ZombieCoder Local AI System...
echo.

echo Step 1: Port cleanup...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8001"') do (
    echo Killing process %%a on port 8001
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":12345"') do (
    echo Killing process %%a on port 12345
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":11434"') do (
    echo Killing process %%a on port 11434
    taskkill /PID %%a /F >nul 2>&1
)

echo Port cleanup completed!
echo.

echo Step 2: Setting environment variables...
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

echo Step 3: Starting Ollama...
start /B "Ollama" "C:\Users\%USERNAME%\AppData\Local\Ollama\ollama.exe" serve
timeout /t 3 /nobreak >nul

echo Step 4: Starting OpenAI Shim...
cd local_ai_integration
start /B "OpenAI Shim" python openai_shim.py
timeout /t 5 /nobreak >nul
cd ..

echo Step 5: Starting ZombieCoder...
cd core-server
start /B "ZombieCoder" python unified_agent_system.py
timeout /t 5 /nobreak >nul
cd ..

echo.
echo All services started! Checking status...
echo.

echo Checking Ollama (Port 11434)...
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo Ollama: RUNNING
) else (
    echo Ollama: FAILED
)

echo Checking OpenAI Shim (Port 8001)...
curl -s http://127.0.0.1:8001/health >nul 2>&1
if %errorlevel% equ 0 (
    echo OpenAI Shim: RUNNING
) else (
    echo OpenAI Shim: FAILED
)

echo Checking ZombieCoder (Port 12345)...
curl -s http://127.0.0.1:12345/ >nul 2>&1
if %errorlevel% equ 0 (
    echo ZombieCoder: RUNNING
) else (
    echo ZombieCoder: FAILED
)

echo.
echo System ready! Press any key to continue...
pause >nul
