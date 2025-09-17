@echo off
echo 🚀 Starting ZombieCoder Windows Services...
echo ==========================================

echo 📋 Activating virtual environment...
call zombie_env\Scripts\activate.bat

echo 📋 Starting Proxy Server...
start "Proxy Server" cmd /k "cd /d %cd% && python core-server/proxy_server.py"

echo 📋 Starting Unified Agent System...
start "Unified Agent" cmd /k "cd /d %cd% && python core-server/unified_agent_system.py"

echo 📋 Starting Multi Project Manager...
start "Multi Project" cmd /k "cd /d %cd% && python core-server/multi_project_manager.py"

echo 📋 Starting Editor Chat Server...
start "Editor Chat" cmd /k "cd /d %cd% && python core-server/editor_chat_server.py"

echo 📋 Starting Friendly Programmer Agent...
start "Friendly Programmer" cmd /k "cd /d %cd% && python core-server/friendly_programmer_agent.py"

timeout /t 3 /nobreak >nul

echo ✅ All ZombieCoder services started!
echo 📊 Available endpoints:
echo   - Proxy Server: http://localhost:8080/proxy/chat
echo   - Unified Agent: http://localhost:12345/chat
echo   - Multi Project: http://localhost:8001/chat
echo   - Editor Chat: http://localhost:8003/chat
echo   - Friendly Programmer: http://localhost:8004/chat
echo.
echo 🧪 Test services: test_windows_services.bat
echo 🛑 Stop services: stop_windows_services.bat
echo.
pause
