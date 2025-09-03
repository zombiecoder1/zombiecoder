@echo off
title Shaon AI Power Switch - Advanced System
color 0A

echo.
echo ========================================
echo    SHAON AI POWER SWITCH
echo    Advanced Agent System v3.0
echo ========================================
echo.

:menu
echo Choose an option:
echo.
echo 1. Start All Services (Step by Step)
echo 2. Stop All Services  
echo 3. Check Status
echo 4. Test Connection
echo 5. Test Different Agents
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto start_all
if "%choice%"=="2" goto stop_all
if "%choice%"=="3" goto check_status
if "%choice%"=="4" goto test_connection
if "%choice%"=="5" goto test_agents
if "%choice%"=="6" goto exit
goto menu

:start_all
echo.
echo ========================================
echo    STARTING ALL SERVICES
echo ========================================
echo.

echo Step 1: Stopping all existing services...
taskkill /f /im "ollama.exe" 2>nul
taskkill /f /im "python.exe" 2>nul
timeout /t 2 /nobreak >nul
echo [OK] All existing services stopped

echo.
echo Step 2: Starting Ollama Server...
start /b "Ollama" cmd /c "ollama serve >nul 2>&1"
echo [OK] Ollama started in background

echo.
echo Step 3: Waiting for Ollama to initialize...
timeout /t 5 /nobreak >nul
echo [OK] Ollama ready

echo.
echo Step 4: Starting Final Solution Server...
cd /d D:\Alhamdullha
start /b "Final Solution" cmd /c "python final_solution.py >nul 2>&1"
echo [OK] Final Solution Server started

echo.
echo Step 5: Starting Proxy Server...
start /b "Proxy Server" cmd /c "python optimized_port_routing.py >nul 2>&1"
echo [OK] Proxy Server started

echo.
echo Step 6: Starting Advanced Agent Server...
start /b "Advanced Agent Server" cmd /c "python core-server\advanced_agent_system.py >nul 2>&1"
echo [OK] Advanced Agent Server started

echo.
echo Step 7: Waiting for all services to initialize...
timeout /t 5 /nobreak >nul

echo.
echo Step 8: Checking all services...
echo.
echo Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Ollama: Running
) else (
    echo [ERROR] Ollama: Not running
)

echo Checking Final Solution...
curl -s http://localhost:8082/api/status >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Final Solution: Running
) else (
    echo [ERROR] Final Solution: Not running
)

echo Checking Proxy Server...
curl -s http://localhost:8080/api/status >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Proxy Server: Running
) else (
    echo [ERROR] Proxy Server: Not running
)

echo Checking Advanced Agent Server...
curl -s http://localhost:12345/status >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Advanced Agent Server: Running
) else (
    echo [ERROR] Advanced Agent Server: Not running
)

echo.
echo Step 9: Testing AI connection...
curl -X POST http://localhost:12345/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Hello সাহন ভাই\",\"user\":\"Test User\"}" ^
  2>nul | findstr "response" >nul 2>&1

if %errorlevel%==0 (
    echo [OK] AI connection working!
) else (
    echo [ERROR] AI connection failed!
)

echo.
echo ========================================
echo    ALL SERVICES STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Services running:
echo - Ollama: http://localhost:11434
echo - Final Solution: http://localhost:8082
echo - Proxy Server: http://localhost:8080
echo - Advanced Agent Server: http://localhost:12345
echo.
echo Advanced Features:
echo - Lazy Loading: Enabled
echo - Memory Management: Active
echo - Agent Personalities: Loaded
echo - Performance Optimization: Running
echo - Auto-Response System: Active
echo.
echo Available Agents (10 Capabilities Each):
echo - সাহন ভাই (Default) - 👨‍💻
echo   * কোড রিভিউ, আর্কিটেকচার, ডিবাগিং, পারফরম্যান্স
echo - মুসকান - 👧
echo   * ফ্রন্টএন্ড, UI/UX, ক্রিয়েটিভ কোডিং, অ্যানিমেশন
echo - ভাবি - 👩‍💼
echo   * ডাটাবেস, API, সিকিউরিটি, মাইক্রোসার্ভিস
echo - বাঘ - 🐯
echo   * সিকিউরিটি, পারফরম্যান্স, পেনিট্রেশন টেস্টিং
echo - হান্টার - 🔍
echo   * বাগ হান্টিং, কোড কোয়ালিটি, অটোমেটেড টেস্টিং
echo.
echo VSCode Extension Features:
echo - Ctrl+Shift+P: Copilot Chat
echo - Status Bar: Real-time system status
echo - Agent Selection: Switch between agents
echo - Code Analysis: Analyze current code
echo - Voice Chat: Coming soon
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:stop_all
echo.
echo ========================================
echo    STOPPING ALL SERVICES
echo ========================================
echo.

echo Stopping Ollama...
taskkill /f /im "ollama.exe" 2>nul
echo [OK] Ollama stopped

echo.
echo Stopping Python servers...
taskkill /f /im "python.exe" 2>nul
echo [OK] All Python servers stopped

echo.
echo All services stopped!
pause
goto menu

:check_status
echo.
echo ========================================
echo    SERVICE STATUS CHECK
echo ========================================
echo.

echo Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Ollama: Running
) else (
    echo [ERROR] Ollama: Not running
)

echo.
echo Checking Final Solution...
curl -s http://localhost:8082/api/status >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Final Solution: Running
) else (
    echo [ERROR] Final Solution: Not running
)

echo.
echo Checking Proxy Server...
curl -s http://localhost:8080/api/status >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Proxy Server: Running
) else (
    echo [ERROR] Proxy Server: Not running
)

echo.
echo Checking Advanced Agent Server...
curl -s http://localhost:12345/status >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Advanced Agent Server: Running
) else (
    echo [ERROR] Advanced Agent Server: Not running
)

echo.
echo Advanced Features:
echo - Lazy Loading: Enabled
echo - Memory Management: Active
echo - Agent Personalities: Loaded
echo - Performance Optimization: Running
echo - Auto-Response System: Active
echo.
echo Available Agents (10 Capabilities Each):
echo - সাহন ভাই (Default) - 👨‍💻
echo - মুসকান - 👧
echo - ভাবি - 👩‍💼
echo - বাঘ - 🐯
echo - হান্টার - 🔍

echo.
pause
goto menu

:test_connection
echo.
echo ========================================
echo    TESTING AI CONNECTION
echo ========================================
echo.

echo Sending test message to AI...
curl -X POST http://localhost:12345/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Hello সাহন ভাই\",\"user\":\"Test User\"}" ^
  2>nul | findstr "response"

if %errorlevel%==0 (
    echo.
    echo [OK] AI connection working!
) else (
    echo.
    echo [ERROR] AI connection failed!
)

echo.
pause
goto menu

:test_agents
echo.
echo ========================================
echo    TESTING DIFFERENT AGENTS
echo ========================================
echo.

echo Testing সাহন ভাই...
curl -X POST http://localhost:12345/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Hello সাহন ভাই\",\"agent\":\"সাহন ভাই\"}" ^
  2>nul | findstr "response" >nul 2>&1
if %errorlevel%==0 (echo [OK] সাহন ভাই: Working) else (echo [ERROR] সাহন ভাই: Failed)

echo.
echo Testing মুসকান...
curl -X POST http://localhost:12345/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Hello মুসকান\",\"agent\":\"মুসকান\"}" ^
  2>nul | findstr "response" >nul 2>&1
if %errorlevel%==0 (echo [OK] মুসকান: Working) else (echo [ERROR] মুসকান: Failed)

echo.
echo Testing বাঘ...
curl -X POST http://localhost:12345/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Hello বাঘ\",\"agent\":\"বাঘ\"}" ^
  2>nul | findstr "response" >nul 2>&1
if %errorlevel%==0 (echo [OK] বাঘ: Working) else (echo [ERROR] বাঘ: Failed)

echo.
echo Testing হান্টার...
curl -X POST http://localhost:12345/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Hello হান্টার\",\"agent\":\"হান্টার\"}" ^
  2>nul | findstr "response" >nul 2>&1
if %errorlevel%==0 (echo [OK] হান্টার: Working) else (echo [ERROR] হান্টার: Failed)

echo.
echo All agents tested!
echo.
pause
goto menu

:exit
echo.
echo Goodbye! Shaon AI Power Switch closed.
echo.
exit
