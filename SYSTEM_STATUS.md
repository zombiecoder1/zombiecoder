# 📊 System Status Monitoring

> **Real-time monitoring and status checking for ZombieCoder Local AI System**

## 🎯 Quick Status Check

### One-Line Status
```bash
# Check all services at once
netstat -an | findstr ":8001\|:12345\|:11434\|:8080\|:8081"
```

### Health Check
```bash
# Quick health verification
curl http://127.0.0.1:8001/health && echo "✅ OpenAI Shim" || echo "❌ OpenAI Shim"
curl http://127.0.0.1:12345/ && echo "✅ ZombieCoder" || echo "❌ ZombieCoder"
curl http://127.0.0.1:11434/api/tags && echo "✅ Ollama" || echo "❌ Ollama"
```

## 🔍 Detailed Status Monitoring

### Port Status Check
```bash
# Check specific ports
echo "=== Port Status ==="
netstat -an | findstr ":8001" && echo "✅ Port 8001 (OpenAI Shim) - ACTIVE" || echo "❌ Port 8001 (OpenAI Shim) - INACTIVE"
netstat -an | findstr ":12345" && echo "✅ Port 12345 (ZombieCoder) - ACTIVE" || echo "❌ Port 12345 (ZombieCoder) - INACTIVE"
netstat -an | findstr ":11434" && echo "✅ Port 11434 (Ollama) - ACTIVE" || echo "❌ Port 11434 (Ollama) - INACTIVE"
netstat -an | findstr ":8080" && echo "✅ Port 8080 (Proxy) - ACTIVE" || echo "❌ Port 8080 (Proxy) - INACTIVE"
netstat -an | findstr ":8081" && echo "✅ Port 8081 (Multi-Project API) - ACTIVE" || echo "❌ Port 8081 (Multi-Project API) - INACTIVE"
```

### Process Status Check
```bash
# Check running processes
echo "=== Process Status ==="
tasklist | findstr "python.exe" && echo "✅ Python processes - RUNNING" || echo "❌ Python processes - NOT RUNNING"
tasklist | findstr "ollama.exe" && echo "✅ Ollama process - RUNNING" || echo "❌ Ollama process - NOT RUNNING"
```

### Service Health Check
```bash
# Test all API endpoints
echo "=== API Health Check ==="

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
```

## 🚨 Troubleshooting Commands

### Kill Blocked Ports
```bash
# Kill processes on specific ports
echo "=== Killing Blocked Ports ==="

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8001"') do (
    echo "🔴 Killing process %%a on port 8001"
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":12345"') do (
    echo "🔴 Killing process %%a on port 12345"
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":11434"') do (
    echo "🔴 Killing process %%a on port 11434"
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8080"') do (
    echo "🔴 Killing process %%a on port 8080"
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8081"') do (
    echo "🔴 Killing process %%a on port 8081"
    taskkill /PID %%a /F >nul 2>&1
)
```

### Restart Services
```bash
# Restart specific services
echo "=== Restarting Services ==="

echo "Restarting OpenAI Shim..."
cd local_ai_integration
start /B python openai_shim.py
cd ..
timeout /t 3 /nobreak >nul

echo "Restarting ZombieCoder..."
start /B python core-server\main_server.py
timeout /t 5 /nobreak >nul

echo "Restarting Proxy Server..."
start /B python our-server\proxy_server.py
timeout /t 3 /nobreak >nul

echo "Restarting Multi-Project API..."
start /B python our-server\multi_project_api.py
timeout /t 3 /nobreak >nul
```

## 📋 Configuration Verification

### Environment Variables
```bash
# Check environment variables
echo "=== Environment Variables ==="
echo "OPENAI_API_BASE: %OPENAI_API_BASE%"
echo "OPENAI_API_KEY: %OPENAI_API_KEY%"
echo "FORCE_LOCAL_AI: %FORCE_LOCAL_AI%"
echo "LOCAL_AI_ENDPOINT: %LOCAL_AI_ENDPOINT%"
echo "ZOMBIECODER_HOST: %ZOMBIECODER_HOST%"
echo "OLLAMA_HOST: %OLLAMA_HOST%"
```

### Configuration Files
```bash
# Check configuration files
echo "=== Configuration Files ==="
if exist ".env" (
    echo "✅ .env (Root) - EXISTS"
) else (
    echo "❌ .env (Root) - MISSING"
)

if exist "core-server\.env" (
    echo "✅ .env (core-server) - EXISTS"
) else (
    echo "❌ .env (core-server) - MISSING"
)

if exist "our-server\.env" (
    echo "✅ .env (our-server) - EXISTS"
) else (
    echo "❌ .env (our-server) - MISSING"
)

if exist ".vscode\settings.json" (
    echo "✅ VS Code settings - EXISTS"
) else (
    echo "❌ VS Code settings - MISSING"
)

if exist ".cursorrules" (
    echo "✅ Cursor rules - EXISTS"
) else (
    echo "❌ Cursor rules - MISSING"
)
```

## 🔄 Auto-Monitoring Script

### STATUS_CHECK.bat
Create a `STATUS_CHECK.bat` file for quick monitoring:

```batch
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
echo "=== Port Status ==="
netstat -an | findstr ":8001" && echo "✅ Port 8001 (OpenAI Shim) - ACTIVE" || echo "❌ Port 8001 (OpenAI Shim) - INACTIVE"
netstat -an | findstr ":12345" && echo "✅ Port 12345 (ZombieCoder) - ACTIVE" || echo "❌ Port 12345 (ZombieCoder) - INACTIVE"
netstat -an | findstr ":11434" && echo "✅ Port 11434 (Ollama) - ACTIVE" || echo "❌ Port 11434 (Ollama) - INACTIVE"
netstat -an | findstr ":8080" && echo "✅ Port 8080 (Proxy) - ACTIVE" || echo "❌ Port 8080 (Proxy) - INACTIVE"
netstat -an | findstr ":8081" && echo "✅ Port 8081 (Multi-Project API) - ACTIVE" || echo "❌ Port 8081 (Multi-Project API) - INACTIVE"

echo.

REM API Health
echo "=== API Health ==="
curl -s http://127.0.0.1:8001/health >nul 2>&1 && echo "✅ OpenAI Shim API - HEALTHY" || echo "❌ OpenAI Shim API - UNHEALTHY"
curl -s http://127.0.0.1:12345/ >nul 2>&1 && echo "✅ ZombieCoder API - HEALTHY" || echo "❌ ZombieCoder API - UNHEALTHY"
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1 && echo "✅ Ollama API - HEALTHY" || echo "❌ Ollama API - UNHEALTHY"

echo.

REM Configuration
echo "=== Configuration ==="
if exist ".env" (echo "✅ .env (Root) - EXISTS") else (echo "❌ .env (Root) - MISSING")
if exist ".vscode\settings.json" (echo "✅ VS Code settings - EXISTS") else (echo "❌ VS Code settings - MISSING")
if exist ".cursorrules" (echo "✅ Cursor rules - EXISTS") else (echo "❌ Cursor rules - MISSING")

echo.
echo ====================================================
echo   🎯 Status Check Complete
echo ====================================================
echo.
pause
```

## 📊 Status Dashboard

### Green Status (All Good) 🟢
```
✅ Port 8001 (OpenAI Shim) - ACTIVE
✅ Port 12345 (ZombieCoder) - ACTIVE  
✅ Port 11434 (Ollama) - ACTIVE
✅ Port 8080 (Proxy) - ACTIVE
✅ Port 8081 (Multi-Project API) - ACTIVE
✅ OpenAI Shim API - HEALTHY
✅ ZombieCoder API - HEALTHY
✅ Ollama API - HEALTHY
```

### Yellow Status (Partial Issues) 🟡
```
✅ Port 8001 (OpenAI Shim) - ACTIVE
❌ Port 12345 (ZombieCoder) - INACTIVE
✅ Port 11434 (Ollama) - ACTIVE
✅ Port 8080 (Proxy) - ACTIVE
✅ Port 8081 (Multi-Project API) - ACTIVE
```

### Red Status (Major Issues) 🔴
```
❌ Port 8001 (OpenAI Shim) - INACTIVE
❌ Port 12345 (ZombieCoder) - INACTIVE
❌ Port 11434 (Ollama) - INACTIVE
❌ Port 8080 (Proxy) - INACTIVE
❌ Port 8081 (Multi-Project API) - INACTIVE
```

## 🚀 Quick Fix Commands

### Fix All Issues
```bash
# 1. Kill all processes
taskkill /F /IM python.exe
taskkill /F /IM ollama.exe

# 2. Restart system
GLOBAL_LAUNCHER.bat
```

### Fix Specific Service
```bash
# Fix OpenAI Shim
cd local_ai_integration && start /B python openai_shim.py

# Fix ZombieCoder
start /B python core-server\main_server.py

# Fix Ollama
start "Ollama" "C:\Users\%USERNAME%\AppData\Local\Ollama\ollama.exe" serve
```

---

**📊 Use these commands to monitor your system health!**

- **Quick Check**: `netstat -an | findstr ":8001\|:12345\|:11434"`
- **Health Check**: `curl http://127.0.0.1:8001/health`
- **Full Status**: Run `STATUS_CHECK.bat`
- **Auto-Fix**: Run `GLOBAL_LAUNCHER.bat`
