@echo off
echo 🧪 Testing ZombieCoder Windows Services...
echo ========================================

echo 📊 Testing Multi Project Manager...
curl -s http://localhost:8001/health
echo.

echo 📊 Testing Unified Agent System...
curl -s http://localhost:12345/status
echo.

echo 📊 Testing Proxy Server...
curl -s http://localhost:8080/proxy/status
echo.

echo 📊 Testing Editor Chat Server...
curl -s http://localhost:8003/health
echo.

echo 📊 Testing Friendly Programmer Agent...
curl -s http://localhost:8004/status
echo.

echo ✅ Service testing completed!
echo.
pause
