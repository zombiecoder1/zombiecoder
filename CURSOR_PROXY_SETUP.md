# 🎯 Cursor Proxy Interceptor Setup Guide

## 🚀 Shadow Proxy Technique

এই setup এর মাধ্যমে Cursor এর UI workflow intact থাকবে, কিন্তু সব requests আমাদের local Ollama এ redirect হবে।

## 📋 Setup Steps

### 1. Start the Proxy Interceptor

```bash
cd /home/sahon/Desktop/zombiecoder
source zombie_env/bin/activate
python3 cursor_proxy_interceptor.py
```

### 2. Configure Cursor to Use Local Proxy

#### Option A: Cursor Settings (Recommended)
1. Open Cursor
2. Go to Settings → Network
3. Set Proxy: `http://localhost:8080`
4. Save settings

#### Option B: Environment Variables
```bash
export HTTP_PROXY=http://localhost:8080
export HTTPS_PROXY=http://localhost:8080
export ALL_PROXY=http://localhost:8080
```

#### Option C: Cursor Config File
Create/edit `~/.cursor/config.json`:
```json
{
  "proxy": {
    "http": "http://localhost:8080",
    "https": "http://localhost:8080"
  }
}
```

### 3. Test the Setup

```bash
# Check interceptor health
curl http://localhost:8080/health

# Test chat completions
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "model": "local-ollama"
  }'
```

## 🔄 How It Works

### Request Flow:
1. **User types in Cursor UI** → Cursor sends request
2. **Proxy Interceptor** → Catches request on port 8080
3. **Local Ollama** → Processes with local model
4. **Response** → Returns to Cursor UI in expected format

### Key Features:
- ✅ **UI Workflow Intact** - Cursor thinks it's using default service
- ✅ **Local Processing** - All requests go to local Ollama
- ✅ **Graceful Fallback** - Falls back to Cursor if local fails
- ✅ **Request Tracking** - Monitors local vs fallback usage
- ✅ **Health Monitoring** - Real-time system status

## 📊 Monitoring

### Health Check:
```bash
curl http://localhost:8080/health | jq .
```

### Response:
```json
{
  "status": "healthy",
  "ollama_connected": true,
  "request_count": 15,
  "local_responses": 12,
  "cursor_responses": 3,
  "timestamp": 1757462585.0405364
}
```

## 🛡️ Safety Features

### 1. No Global Blocking
- ❌ No hosts file modification
- ❌ No iptables rules
- ❌ No network blocking
- ✅ Pure proxy redirection

### 2. Graceful Fallback
- Local model fails → Falls back to Cursor
- Clear error messages
- No hanging or blocking

### 3. Request Tracking
- Monitors local vs fallback usage
- Real-time statistics
- Performance metrics

## 🔧 Troubleshooting

### Issue: Cursor not using proxy
**Solution:** Check Cursor settings and restart Cursor

### Issue: Local model not responding
**Solution:** Check Ollama status:
```bash
curl http://localhost:11434/api/tags
```

### Issue: Proxy not intercepting
**Solution:** Check if port 8080 is free:
```bash
netstat -tlnp | grep :8080
```

## 🚀 Advanced Configuration

### Custom Model Selection:
Edit `cursor_proxy_interceptor.py`:
```python
def select_best_model(self) -> Optional[str]:
    # Customize model selection logic
    for model_name in ["your-preferred-model", "backup-model"]:
        if model_name in available_models:
            return model_name
```

### Custom Response Formatting:
Modify the response formatting in `chat_completions()` method to match Cursor's exact expectations.

## 📈 Performance Tips

1. **Use lightweight models** for faster responses
2. **Monitor system resources** to avoid overload
3. **Enable request caching** for repeated queries
4. **Use streaming responses** for long outputs

## 🔄 Restart Commands

```bash
# Stop interceptor
pkill -f "cursor_proxy_interceptor.py"

# Start interceptor
cd /home/sahon/Desktop/zombiecoder
source zombie_env/bin/activate
python3 cursor_proxy_interceptor.py
```

---

**Status:** 🟢 Ready for Cursor Integration
**Last Updated:** $(date)
**Next Step:** Configure Cursor proxy settings
