# ZombieCoder Ollama Memory Monitor & Auto-Killer
# Prevents memory leaks by monitoring and auto-restarting Ollama

param(
    [int]$MemoryThresholdMB = 5000,  # 5GB threshold
    [int]$CheckIntervalSeconds = 30,  # Check every 30 seconds
    [string]$LogFile = "ollama_monitor.log"
)

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Write-Host $logMessage
    Add-Content -Path $LogFile -Value $logMessage
}

function Get-OllamaMemoryUsage {
    try {
        $process = Get-Process ollama -ErrorAction SilentlyContinue
        if ($process) {
            $memoryMB = [math]::Round($process.WorkingSet / 1MB, 2)
            return @{
                ProcessId = $process.Id
                MemoryMB = $memoryMB
                CPU = $process.CPU
                Status = "Running"
            }
        }
        return @{ Status = "Not Running" }
    }
    catch {
        return @{ Status = "Error: $($_.Exception.Message)" }
    }
}

function Restart-Ollama {
    Write-Log "🔄 Restarting Ollama due to high memory usage..."
    
    try {
        # Kill all Ollama processes
        Get-Process ollama -ErrorAction SilentlyContinue | Stop-Process -Force
        Start-Sleep -Seconds 2
        
        # Kill any remaining processes on port 11434
        $portProcess = Get-NetTCPConnection -LocalPort 11434 -ErrorAction SilentlyContinue
        if ($portProcess) {
            Stop-Process -Id $portProcess.OwningProcess -Force
            Start-Sleep -Seconds 1
        }
        
        # Start fresh Ollama instance
        if (Test-Path "C:\Users\sahon\AppData\Local\Programs\Ollama\ollama.exe") {
            Start-Process -WindowStyle Hidden "C:\Users\sahon\AppData\Local\Programs\Ollama\ollama.exe" -ArgumentList "serve"
            Write-Log "✅ Ollama restarted successfully"
        } else {
            Write-Log "❌ Ollama executable not found"
        }
    }
    catch {
        Write-Log "❌ Error restarting Ollama: $($_.Exception.Message)"
    }
}

function Test-OllamaHealth {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -UseBasicParsing -TimeoutSec 5
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

# Main monitoring loop
Write-Log "🚀 ZombieCoder Ollama Monitor Started"
Write-Log "📊 Memory Threshold: $MemoryThresholdMB MB"
Write-Log "⏰ Check Interval: $CheckIntervalSeconds seconds"
Write-Log "📁 Log File: $LogFile"
Write-Log "=" * 50

while ($true) {
    try {
        $ollamaStatus = Get-OllamaMemoryUsage
        
        if ($ollamaStatus.Status -eq "Running") {
            $memoryMB = $ollamaStatus.MemoryMB
            $processId = $ollamaStatus.ProcessId
            
            Write-Log "📊 Ollama Status: PID $processId, Memory: $memoryMB MB"
            
            # Check memory threshold
            if ($memoryMB -gt $MemoryThresholdMB) {
                Write-Log "🚨 MEMORY LEAK DETECTED! Usage: $memoryMB MB > $MemoryThresholdMB MB"
                Restart-Ollama
                Start-Sleep -Seconds 10  # Wait for restart
            }
            
            # Check health
            if (-not (Test-OllamaHealth)) {
                Write-Log "⚠️ Ollama not responding, restarting..."
                Restart-Ollama
                Start-Sleep -Seconds 10
            }
        } else {
            Write-Log "⚠️ Ollama not running, starting..."
            Restart-Ollama
            Start-Sleep -Seconds 10
        }
        
        # Wait before next check
        Start-Sleep -Seconds $CheckIntervalSeconds
    }
    catch {
        Write-Log "❌ Monitor Error: $($_.Exception.Message)"
        Start-Sleep -Seconds $CheckIntervalSeconds
    }
}
