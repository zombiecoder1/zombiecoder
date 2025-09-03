@echo off
echo 🚀 Starting ZombieCoder Server...
echo.

REM Activate virtual environment
echo 📦 Activating virtual environment...
call .venv\Scripts\Activate.ps1

REM Check if server is already running
echo 🔍 Checking if server is already running...
netstat -an | findstr :12345 >nul
if %errorlevel% equ 0 (
    echo ⚠️ Server is already running on port 12345
    echo 🛑 Stopping existing server...
    taskkill /f /im python.exe >nul 2>&1
    timeout /t 3 >nul
)

REM Start main server
echo 🚀 Starting main server...
cd our-server
start /B python main_server.py

REM Wait for server to start
echo ⏳ Waiting for server to start...
timeout /t 5 >nul

REM Check server status
echo 🔍 Checking server status...
curl -s http://localhost:12345/api/status >nul
if %errorlevel% equ 0 (
    echo ✅ Server started successfully!
    echo 🌐 API: http://localhost:12345
    echo 📊 Status: http://localhost:12345/api/status
    echo.
    echo 🎉 ZombieCoder is ready to use!
) else (
    echo ❌ Server failed to start
    echo 🔍 Check logs for errors
)

pause
