@echo off
echo 🚀 ZombieCoder Windows Setup
echo ================================

echo 📋 Installing Python dependencies...
pip install -r core-server/requirements.txt

echo 📋 Creating virtual environment...
python -m venv zombie_env
call zombie_env\Scripts\activate.bat

echo 📋 Installing additional Windows dependencies...
pip install flask flask-cors requests psutil

echo 🐳 Installing Ollama for Windows...
echo Please download and install Ollama from: https://ollama.ai/download/windows

echo 📋 Creating Windows startup script...
echo @echo off > start_windows_services.bat
echo call zombie_env\Scripts\activate.bat >> start_windows_services.bat
echo start "Proxy Server" cmd /k "python core-server/proxy_server.py" >> start_windows_services.bat
echo start "Unified Agent" cmd /k "python core-server/unified_agent_system.py" >> start_windows_services.bat
echo start "Multi Project" cmd /k "python core-server/multi_project_manager.py" >> start_windows_services.bat
echo start "Editor Chat" cmd /k "python core-server/editor_chat_server.py" >> start_windows_services.bat
echo echo ✅ All ZombieCoder services started! >> start_windows_services.bat
echo echo 📊 Check status: curl http://localhost:8001/health >> start_windows_services.bat
echo pause >> start_windows_services.bat

echo 📋 Creating Windows stop script...
echo @echo off > stop_windows_services.bat
echo taskkill /f /im python.exe >> stop_windows_services.bat
echo echo ✅ All ZombieCoder services stopped! >> stop_windows_services.bat
echo pause >> stop_windows_services.bat

echo 📋 Creating Windows test script...
echo @echo off > test_windows_services.bat
echo echo 🧪 Testing ZombieCoder Windows Services >> test_windows_services.bat
echo curl http://localhost:8001/health >> test_windows_services.bat
echo curl http://localhost:12345/status >> test_windows_services.bat
echo curl http://localhost:8080/proxy/status >> test_windows_services.bat
echo pause >> test_windows_services.bat

echo ✅ Windows setup completed!
echo 🚀 Run start_windows_services.bat to start all services
echo 🛑 Run stop_windows_services.bat to stop all services
echo 🧪 Run test_windows_services.bat to test services
pause
