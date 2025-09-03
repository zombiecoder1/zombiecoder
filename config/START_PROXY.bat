@echo off
echo.
echo 🚀 ZombieCoder Proxy Server Launcher
echo ======================================
echo.

REM Activate virtual environment
echo 📦 Activating virtual environment...
call .venv\Scripts\Activate.bat

REM Kill existing processes on proxy port
echo 🔄 Checking port 8080...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080') do (
    echo Killing process %%a on port 8080
    taskkill /PID %%a /F >nul 2>&1
)

REM Start proxy server
echo 🤖 Starting Cursor Proxy Server...
start /B python our-server\proxy_server.py

REM Wait for proxy server
echo ⏳ Waiting for proxy server to start...
timeout /t 3 /nobreak >nul

REM Check proxy status
echo 📡 Checking proxy server status...
curl -s http://localhost:8080/proxy/status >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Proxy server is running on http://localhost:8080
) else (
    echo ❌ Proxy server failed to start
    pause
    exit /b 1
)

echo.
echo 🎯 Proxy Server Configuration:
echo ==============================
echo 📡 Server: http://localhost:8080
echo 🤖 Agent: ZombieCoder Agent (সাহন ভাই)
echo 🔧 Capabilities: 10 (coding, debugging, architecture, etc.)
echo 🎭 Personalities: 8 (elder_brother, friend, teacher, etc.)
echo 🔄 Auto-Detect: Enabled
echo ✅ Truth Verification: Enabled
echo 🌐 Real-Time Support: Enabled
echo.

echo 📋 Next Steps:
echo ===============
echo 1. Configure Cursor to use local proxy
echo 2. Test with Cursor AI features
echo 3. Check proxy logs for requests
echo.

echo 🎉 Proxy Server Ready!
echo Press any key to exit...
pause >nul
