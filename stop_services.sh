#!/bin/bash
# ZombieCoder Service Stopper

echo "🛑 Stopping ZombieCoder Services..."

# Stop services using saved PIDs
for pid_file in logs/*.pid; do
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Stopping process $PID..."
            kill "$PID"
            rm "$pid_file"
        fi
    fi
done

echo "✅ All services stopped!"
