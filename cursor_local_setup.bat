@echo off
chcp 65001 >nul
echo.
echo ====================================================
echo   🚀 Cursor AI Local Setup
echo ====================================================
echo.

echo 📋 Setting up Cursor AI for Local AI...
echo.

REM Set environment variables for current session
echo 🔧 Setting Environment Variables...
set OPENAI_API_BASE=http://127.0.0.1:8001/v1
set OPENAI_API_KEY=local-ai-key
set FORCE_LOCAL_AI=true

echo ✅ Environment Variables Set:
echo    OPENAI_API_BASE=%OPENAI_API_BASE%
echo    OPENAI_API_KEY=%OPENAI_API_KEY%
echo    FORCE_LOCAL_AI=%FORCE_LOCAL_AI%
echo.

echo 📝 Create .env file in your Cursor project:
echo.
echo OPENAI_API_BASE=http://127.0.0.1:8001/v1
echo OPENAI_API_KEY=local-ai-key
echo FORCE_LOCAL_AI=true
echo LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1
echo.

echo 🔄 Next Steps:
echo 1. Copy the .env content above
echo 2. Create .env file in your Cursor project folder
echo 3. Restart Cursor
echo 4. Test with Ctrl+Shift+I
echo.
echo 🎯 Advanced Setup:
echo - VS Code Extension: Install ZombieCoder Extension
echo - Terminal Integration: Available via curl commands
echo - Auto-Configuration: Run GLOBAL_LAUNCHER.bat for full setup
echo.

echo 🧪 Test Local AI Connection:
echo Testing connection to OpenAI Shim...
curl -s http://127.0.0.1:8001/health
if %errorlevel% equ 0 (
    echo ✅ OpenAI Shim is accessible!
    echo.
    echo 🧪 Testing AI Chat Endpoint...
    curl -s -X POST http://127.0.0.1:8001/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"local-llama\",\"messages\":[{\"role\":\"user\",\"content\":\"Test message\"}],\"max_tokens\":10}" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ AI Chat API: Working
    ) else (
        echo ❌ AI Chat API: Failed
    )
) else (
    echo ❌ OpenAI Shim not accessible. Run GLOBAL_LAUNCHER.bat first!
)

echo.
echo ====================================================
echo   🎯 Setup Complete! Press any key to continue...
echo ====================================================
pause >nul
