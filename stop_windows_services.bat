@echo off
echo 🛑 Stopping ZombieCoder Windows Services...
echo ==========================================

echo 📋 Stopping all Python processes...
taskkill /f /im python.exe 2>nul

echo 📋 Stopping Ollama processes...
taskkill /f /im ollama.exe 2>nul

echo ✅ All ZombieCoder services stopped!
echo.
pause
