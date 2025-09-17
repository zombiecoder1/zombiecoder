# 🧟 ZombieCoder Memory Dashboard Setup Guide

**Status:** ✅ READY TO USE

## 🚀 **Quick Setup (5 minutes)**

### 1. **Start Memory Dashboard Server**
```bash
cd /home/sahon/Desktop/zombiecoder/tests
python3 -m http.server 9001
```

### 2. **Start Auto Updater (Background)**
```bash
cd /home/sahon/Desktop/zombiecoder/tests
python3 auto_updater.py
```

### 3. **Open Dashboard**
Open browser: **http://localhost:9001/memory_dashboard.html**

## 📊 **What You'll See**

### **Real-time Data:**
- ✅ **Server Status** - All running services
- ✅ **Statistics** - Local vs Cloud responses
- ✅ **Conversations** - Recent chat messages
- ✅ **Logs** - System activity logs

### **Interactive Features:**
- 🔄 **Auto Refresh** - Updates every 3 seconds
- 📥 **Download Conversations** - Export chat history
- ✏️ **Quick Write** - Add messages manually
- 🗑️ **Clear Memory** - Reset all data

## 🛠️ **Manual Commands**

### **Add Conversations:**
```bash
cd /home/sahon/Desktop/zombiecoder/tests

# Add user message
python3 writer.py append --actor user --text "Hello, how are you?"

# Add assistant response
python3 writer.py append --actor assistant --text "I'm working perfectly with local AI!"
```

### **Update Statistics:**
```bash
# Update stats
python3 writer.py stat --set total_requests=10 --set local_responses=8 --set cloud_responses=2

# Update latency
python3 writer.py stat --set avg_latency=120 --set current_route=local
```

### **Add Logs:**
```bash
# Add info log
python3 writer.py log --level info --message "System started successfully"

# Add warning log
python3 writer.py log --level warning --message "High memory usage detected"

# Add error log
python3 writer.py log --level error --message "Connection timeout"
```

### **Check Status:**
```bash
# Show memory status
python3 writer.py status

# Clear all memory
python3 writer.py clear
```

## 🔄 **Automatic Updates**

### **Auto Updater Features:**
- ✅ **Server Status** - Checks all services every 5 seconds
- ✅ **Statistics** - Pulls data from monitoring dashboard
- ✅ **System Logs** - Adds periodic status updates
- ✅ **Error Handling** - Graceful fallback for failed services

### **Start Auto Updater:**
```bash
# Run once
python3 auto_updater.py --once

# Run continuously (background)
python3 auto_updater.py

# Custom interval (10 seconds)
python3 auto_updater.py --interval 10
```

## 📁 **File Structure**

```
/home/sahon/Desktop/zombiecoder/tests/
├── memory_dashboard.html          # Main dashboard
├── writer.py                      # Memory writer script
├── auto_updater.py                # Auto updater script
└── memory/                        # Memory data directory
    ├── servers.json               # Server statuses
    ├── log.json                   # System logs
    ├── conversations.json         # Chat messages
    └── stats.json                 # Statistics
```

## 🎯 **Integration with Running System**

### **Current Status:**
- ✅ **Proxy Interceptor** - Running on port 8080
- ✅ **Monitoring Dashboard** - Running on port 9000
- ✅ **Memory Dashboard** - Running on port 9001
- ✅ **Auto Updater** - Background monitoring

### **Data Flow:**
```
Running Servers → Auto Updater → Memory Files → Dashboard
     ↓                ↓              ↓           ↓
  Status/Stats → JSON Files → Real-time Display
```

## 🚨 **Troubleshooting**

### **Dashboard Not Loading:**
```bash
# Check if server is running
curl http://localhost:9001/memory_dashboard.html

# Restart server
pkill -f "http.server 9001"
cd /home/sahon/Desktop/zombiecoder/tests
python3 -m http.server 9001
```

### **No Data Showing:**
```bash
# Check memory files
ls -la /home/sahon/Desktop/zombiecoder/tests/memory/

# Run auto updater once
cd /home/sahon/Desktop/zombiecoder/tests
python3 auto_updater.py --once

# Check writer status
python3 writer.py status
```

### **Auto Updater Not Working:**
```bash
# Check if running
ps aux | grep auto_updater

# Restart auto updater
pkill -f auto_updater.py
cd /home/sahon/Desktop/zombiecoder/tests
python3 auto_updater.py
```

## 🎉 **Success Indicators**

### ✅ **Dashboard Working:**
- Browser shows dashboard at http://localhost:9001/memory_dashboard.html
- Real-time data updates every 3 seconds
- Server status shows running services
- Statistics show local vs cloud responses

### ✅ **Auto Updates Working:**
- Data refreshes automatically
- Server statuses update in real-time
- Statistics pull from monitoring dashboard
- System logs show periodic updates

### ✅ **Manual Commands Working:**
- `writer.py` commands execute successfully
- Conversations and logs add properly
- Statistics update correctly
- Status command shows current data

## 🚀 **Next Steps**

1. **Open Dashboard:** http://localhost:9001/memory_dashboard.html
2. **Monitor Real-time:** Watch data update automatically
3. **Add Test Data:** Use writer commands to add conversations
4. **Verify Integration:** Confirm data flows from running servers
5. **Enjoy:** Real-time monitoring of your local AI system!

---

**Status:** 🟢 READY FOR USE
**Dashboard:** http://localhost:9001/memory_dashboard.html
**Last Updated:** $(date)
**Auto Updater:** Running in background
