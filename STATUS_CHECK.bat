@echo off
chcp 65001 >nul
echo.
echo ====================================================
echo   📊 ZombieCoder System Status Check
echo ====================================================
echo.

echo 🔍 Checking System Status...
echo.

REM Port Status
echo === Port Status ===
netstat -an | findstr ":8001" >nul 2>&1 && echo "✅ Port 8001 (OpenAI Shim) - ACTIVE" || echo "❌ Port 8001 (OpenAI Shim) - INACTIVE"
netstat -an | findstr ":12345" >nul 2>&1 && echo "✅ Port 12345 (ZombieCoder) - ACTIVE" || echo "❌ Port 12345 (ZombieCoder) - INACTIVE"
netstat -an | findstr ":11434" >nul 2>&1 && echo "✅ Port 11434 (Ollama) - ACTIVE" || echo "❌ Port 11434 (Ollama) - INACTIVE"
netstat -an | findstr ":8080" >nul 2>&1 && echo "✅ Port 8080 (Proxy) - ACTIVE" || echo "❌ Port 8080 (Proxy) - INACTIVE"
netstat -an | findstr ":8081" >nul 2>&1 && echo "✅ Port 8081 (Multi-Project API) - ACTIVE" || echo "❌ Port 8081 (Multi-Project API) - INACTIVE"

echo.

REM Process Status
echo === Process Status ===
tasklist | findstr "python.exe" >nul 2>&1 && echo "✅ Python processes - RUNNING" || echo "❌ Python processes - NOT RUNNING"
tasklist | findstr "ollama.exe" >nul 2>&1 && echo "✅ Ollama process - RUNNING" || echo "❌ Ollama process - NOT RUNNING"

echo.

REM API Health
echo === API Health ===
echo "Testing OpenAI Shim..."
curl -s http://127.0.0.1:8001/health >nul 2>&1
if %errorlevel% equ 0 (
    echo "✅ OpenAI Shim API - HEALTHY"
) else (
    echo "❌ OpenAI Shim API - UNHEALTHY"
)

echo "Testing ZombieCoder..."
curl -s http://127.0.0.1:12345/ >nul 2>&1
if %errorlevel% equ 0 (
    echo "✅ ZombieCoder API - HEALTHY"
) else (
    echo "❌ ZombieCoder API - UNHEALTHY"
)

echo "Testing Ollama..."
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo "✅ Ollama API - HEALTHY"
) else (
    echo "❌ Ollama API - UNHEALTHY"
)

echo.

REM Configuration
echo === Configuration ===
if exist ".env" (echo "✅ .env (Root) - EXISTS") else (echo "❌ .env (Root) - MISSING")
if exist "core-server\.env" (echo "✅ .env (core-server) - EXISTS") else (echo "❌ .env (core-server) - MISSING")
if exist "our-server\.env" (echo "✅ .env (our-server) - EXISTS") else (echo "❌ .env (our-server) - MISSING")
if exist ".vscode\settings.json" (echo "✅ VS Code settings - EXISTS") else (echo "❌ VS Code settings - MISSING")
if exist ".cursorrules" (echo "✅ Cursor rules - EXISTS") else (echo "❌ Cursor rules - MISSING")

echo.

REM Environment Variables
echo === Environment Variables ===
if defined OPENAI_API_BASE (
    echo "✅ OPENAI_API_BASE: %OPENAI_API_BASE%"
) else (
    echo "❌ OPENAI_API_BASE: NOT SET"
)

if defined FORCE_LOCAL_AI (
    echo "✅ FORCE_LOCAL_AI: %FORCE_LOCAL_AI%"
) else (
    echo "❌ FORCE_LOCAL_AI: NOT SET"
)

if defined LOCAL_AI_ENDPOINT (
    echo "✅ LOCAL_AI_ENDPOINT: %LOCAL_AI_ENDPOINT%"
) else (
    echo "❌ LOCAL_AI_ENDPOINT: NOT SET"
)

echo.

REM Summary
echo === Summary ===
set /a active_ports=0
set /a healthy_apis=0
set /a config_files=0

netstat -an | findstr ":8001" >nul 2>&1 && set /a active_ports+=1
netstat -an | findstr ":12345" >nul 2>&1 && set /a active_ports+=1
netstat -an | findstr ":11434" >nul 2>&1 && set /a active_ports+=1
netstat -an | findstr ":8080" >nul 2>&1 && set /a active_ports+=1
netstat -an | findstr ":8081" >nul 2>&1 && set /a active_ports+=1

curl -s http://127.0.0.1:8001/health >nul 2>&1 && set /a healthy_apis+=1
curl -s http://127.0.0.1:12345/ >nul 2>&1 && set /a healthy_apis+=1
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1 && set /a healthy_apis+=1

if exist ".env" set /a config_files+=1
if exist ".vscode\settings.json" set /a config_files+=1
if exist ".cursorrules" set /a config_files+=1

echo "📊 System Health: %active_ports%/5 ports active, %healthy_apis%/3 APIs healthy, %config_files%/3 config files present"

if %active_ports% equ 5 (
    if %healthy_apis% equ 3 (
        echo "🎉 System Status: EXCELLENT - All services running perfectly!"
    ) else (
        echo "⚠️  System Status: GOOD - Services running but some APIs need attention"
    )
) else (
    if %active_ports% geq 3 (
        echo "⚠️  System Status: FAIR - Some services down, consider restarting"
    ) else (
        echo "🚨 System Status: POOR - Multiple services down, run GLOBAL_LAUNCHER.bat"
    )
)

echo.
echo ====================================================
echo   🎯 Status Check Complete
echo ====================================================
echo.

echo 💡 Quick Actions:
echo "   🚀 Start System: GLOBAL_LAUNCHER.bat"
echo "   🔄 Restart: Run GLOBAL_LAUNCHER.bat again"
echo "   🧹 Cleanup: taskkill /F /IM python.exe"
echo "   📊 Recheck: Run this file again"
echo.

pause
