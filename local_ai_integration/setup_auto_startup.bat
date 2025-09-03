@echo off
title ZombieCoder Local AI - Auto Startup Setup
echo ====================================================
echo    🚀 ZombieCoder Local AI - Auto Startup Setup
echo ====================================================
echo.

REM ---- Check Administrator Rights ----
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERROR: This script requires Administrator privileges
    echo.
    echo Please right-click on this file and select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

echo ✅ Administrator privileges confirmed
echo.

REM ---- Set Project Path ----
set PROJECT_DIR=%~dp0..
set PROJECT_DIR=%PROJECT_DIR:~0,-1%
echo 📁 Project Directory: %PROJECT_DIR%

REM ---- Create Startup Script ----
echo [1/4] Creating startup script...
set STARTUP_SCRIPT=%PROJECT_DIR%\start_local_ai.bat

(
echo @echo off
echo title ZombieCoder Local AI System
echo echo ====================================================
echo echo    🚀 ZombieCoder Local AI System Starting...
echo echo ====================================================
echo echo.
echo echo 📁 Project Directory: %PROJECT_DIR%
echo echo.
echo cd /d "%PROJECT_DIR%"
echo.
echo echo [1/3] Starting OpenAI Shim Server...
echo start "OpenAI Shim" cmd /k "cd /d local_ai_integration ^& python openai_shim.py"
echo timeout /t 3 /nobreak ^>nul
echo.
echo echo [2/3] Starting ZombieCoder Agent System...
echo start "ZombieCoder Agents" cmd /k "cd /d core-server ^& python advanced_agent_system.py"
echo timeout /t 3 /nobreak ^>nul
echo.
echo echo [3/3] Starting Ollama Models...
echo start "Ollama Models" cmd /k "ollama serve"
echo.
echo echo ✅ All services started!
echo echo.
echo echo 🌐 OpenAI Shim: http://127.0.0.1:8001
echo echo 🤖 ZombieCoder: http://127.0.0.1:12345
echo echo 🧠 Ollama: http://127.0.0.1:11434
echo echo.
echo pause
) > "%STARTUP_SCRIPT%"

if exist "%STARTUP_SCRIPT%" (
    echo ✅ Startup script created: %STARTUP_SCRIPT%
) else (
    echo ❌ Failed to create startup script
    pause
    exit /b 1
)

REM ---- Create Task Scheduler Entry ----
echo [2/4] Creating Windows Task Scheduler entry...
set TASK_NAME="ZombieCoder Local AI Startup"
set TASK_COMMAND=schtasks /create /tn %TASK_NAME% /tr "%STARTUP_SCRIPT%" /sc onlogon /ru "SYSTEM" /f

echo Creating scheduled task...
%TASK_COMMAND% >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ Scheduled task created successfully
) else (
    echo ⚠️ Could not create scheduled task (may already exist)
    echo   You can manually run: %STARTUP_SCRIPT%
)

REM ---- Create Desktop Shortcut ----
echo [3/4] Creating desktop shortcut...
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT=%DESKTOP%\ZombieCoder Local AI.lnk

echo Creating desktop shortcut...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%STARTUP_SCRIPT%'; $Shortcut.WorkingDirectory = '%PROJECT_DIR%'; $Shortcut.Description = 'Start ZombieCoder Local AI System'; $Shortcut.IconLocation = '%PROJECT_DIR%\core-server\agents\editor_agent.py,0'; $Shortcut.Save()}"

if exist "%SHORTCUT%" (
    echo ✅ Desktop shortcut created
) else (
    echo ⚠️ Could not create desktop shortcut
)

REM ---- Configure Environment Variables ----
echo [4/4] Configuring environment variables...
echo Setting OpenAI environment variables...

setx OPENAI_API_KEY "local-only" >nul 2>&1
setx OPENAI_API_BASE "http://127.0.0.1:8001/v1" >nul 2>&1
setx OPENAI_BASE_URL "http://127.0.0.1:8001/v1" >nul 2>&1

echo ✅ Environment variables configured
echo.

REM ---- Final Instructions ----
echo ====================================================
echo    🎉 Auto Startup Setup Complete!
echo ====================================================
echo.
echo 📋 What was configured:
echo    ✅ Startup script: %STARTUP_SCRIPT%
echo    ✅ Scheduled task: %TASK_NAME%
echo    ✅ Desktop shortcut: ZombieCoder Local AI
echo    ✅ Environment variables: OPENAI_API_*
echo.
echo 🚀 How to use:
echo    1. Double-click desktop shortcut to start manually
echo    2. System will auto-start on login
echo    3. Run: python local_ai_integration\test_local_setup.py
echo.
echo 🔧 Manual start command:
echo    %STARTUP_SCRIPT%
echo.
echo 📁 Files created:
echo    - %STARTUP_SCRIPT%
echo    - %SHORTCUT%
echo.
echo ====================================================
echo.

REM ---- Test Configuration ----
echo 🧪 Testing configuration...
echo Testing OpenAI Shim endpoint...
powershell -Command "& {try { $response = Invoke-WebRequest -Uri 'http://127.0.0.1:8001/health' -UseBasicParsing -Timeout 5; if($response.StatusCode -eq 200) { Write-Host '✅ OpenAI Shim: ONLINE' } else { Write-Host '❌ OpenAI Shim: OFFLINE' } } catch { Write-Host '❌ OpenAI Shim: OFFLINE' }}"

echo.
echo 💡 Next steps:
echo    1. Restart Cursor IDE to apply environment variables
echo    2. Run the startup script to test all services
echo    3. Use Ctrl+Shift+Z in Cursor to activate local AI
echo.

pause
