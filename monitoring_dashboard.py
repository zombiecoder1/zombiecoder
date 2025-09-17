#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 ZombieCoder Monitoring Dashboard
Real-time monitoring of Local vs Cloud usage
"""

import os
import json
import time
import logging
import requests
import threading
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitoringDashboard:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Port configuration
        self.ports = {
            "dashboard": 9000,
            "proxy": 8080,
            "agent_system": 8004,
            "truth_checker": 8002,
            "editor_integration": 8003,
            "multi_project": 8001,
            "main_server": 12345,
            "ollama": 11434
        }
        
        # Monitoring data
        self.monitoring_data = {
            "requests": {
                "total": 0,
                "local": 0,
                "cloud": 0,
                "failed": 0
            },
            "latency": {
                "local_avg": 0,
                "cloud_avg": 0,
                "current": 0
            },
            "servers": {
                "proxy": {"status": "unknown", "last_check": 0},
                "agent_system": {"status": "unknown", "last_check": 0},
                "truth_checker": {"status": "unknown", "last_check": 0},
                "editor_integration": {"status": "unknown", "last_check": 0},
                "multi_project": {"status": "unknown", "last_check": 0},
                "main_server": {"status": "unknown", "last_check": 0},
                "ollama": {"status": "unknown", "last_check": 0}
            },
            "system": {
                "cpu_usage": 0,
                "memory_usage": 0,
                "disk_usage": 0
            },
            "recent_requests": [],
            "uptime": time.time()
        }
        
        # Setup routes
        self.setup_routes()
        
        # Start monitoring
        self.start_monitoring()
        
        logger.info("📊 Monitoring Dashboard initialized")
    
    def setup_routes(self):
        """Setup dashboard routes"""
        
        @self.app.route('/', methods=['GET'])
        def dashboard():
            """Main dashboard page"""
            return render_template_string(DASHBOARD_HTML)
        
        @self.app.route('/api/status', methods=['GET'])
        def get_status():
            """Get comprehensive system status"""
            try:
                # Update server statuses
                self.update_server_statuses()
                
                # Update system metrics
                self.update_system_metrics()
                
                # Calculate uptime
                uptime_seconds = time.time() - self.monitoring_data['uptime']
                uptime_str = str(timedelta(seconds=int(uptime_seconds)))
                
                return jsonify({
                    "status": "healthy",
                    "timestamp": time.time(),
                    "uptime": uptime_str,
                    "requests": self.monitoring_data['requests'],
                    "latency": self.monitoring_data['latency'],
                    "servers": self.monitoring_data['servers'],
                    "system": self.monitoring_data['system'],
                    "recent_requests": self.monitoring_data['recent_requests'][-10:]  # Last 10 requests
                })
                
            except Exception as e:
                logger.error(f"Status error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/requests', methods=['GET'])
        def get_requests():
            """Get request statistics"""
            return jsonify(self.monitoring_data['requests'])
        
        @self.app.route('/api/servers', methods=['GET'])
        def get_servers():
            """Get server statuses"""
            return jsonify(self.monitoring_data['servers'])
        
        @self.app.route('/api/system', methods=['GET'])
        def get_system():
            """Get system metrics"""
            return jsonify(self.monitoring_data['system'])
        
        @self.app.route('/api/proxy-stats', methods=['GET'])
        def get_proxy_stats():
            """Get proxy statistics"""
            try:
                response = requests.get(f"http://localhost:{self.ports['proxy']}/health", timeout=5)
                if response.status_code == 200:
                    return jsonify(response.json())
                else:
                    return jsonify({"error": "Proxy not responding"}), 503
            except Exception as e:
                return jsonify({"error": str(e)}), 503
        
        @self.app.route('/api/agent-stats', methods=['GET'])
        def get_agent_stats():
            """Get agent system statistics"""
            try:
                response = requests.get(f"http://localhost:{self.ports['agent_system']}/status", timeout=5)
                if response.status_code == 200:
                    return jsonify(response.json())
                else:
                    return jsonify({"error": "Agent system not responding"}), 503
            except Exception as e:
                return jsonify({"error": str(e)}), 503
        
        @self.app.route('/api/truth-checker-stats', methods=['GET'])
        def get_truth_checker_stats():
            """Get truth checker statistics"""
            try:
                response = requests.get(f"http://localhost:{self.ports['truth_checker']}/status", timeout=5)
                if response.status_code == 200:
                    return jsonify(response.json())
                else:
                    return jsonify({"error": "Truth checker not responding"}), 503
            except Exception as e:
                return jsonify({"error": str(e)}), 503
        
        @self.app.route('/api/test-request', methods=['POST'])
        def test_request():
            """Test a request to see if it goes local or cloud"""
            try:
                data = request.get_json()
                message = data.get('message', 'Hello, test message')
                
                start_time = time.time()
                
                # Send test request to proxy
                response = requests.post(
                    f"http://localhost:{self.ports['proxy']}/v1/chat/completions",
                    json={
                        "messages": [{"role": "user", "content": message}],
                        "model": "local-ollama"
                    },
                    timeout=30
                )
                
                end_time = time.time()
                latency = (end_time - start_time) * 1000  # Convert to milliseconds
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Determine if response is local or cloud
                    # Local responses typically < 2000ms, cloud responses > 5000ms
                    route = "local" if latency < 2000 else "cloud"
                    
                    # Update monitoring data
                    self.monitoring_data['requests']['total'] += 1
                    if route == "local":
                        self.monitoring_data['requests']['local'] += 1
                    else:
                        self.monitoring_data['requests']['cloud'] += 1
                    
                    # Update latency
                    self.monitoring_data['latency']['current'] = latency
                    
                    # Add to recent requests
                    self.monitoring_data['recent_requests'].append({
                        "timestamp": time.time(),
                        "message": message[:50] + "..." if len(message) > 50 else message,
                        "route": route,
                        "latency": latency,
                        "status": "success"
                    })
                    
                    # Keep only last 100 requests
                    if len(self.monitoring_data['recent_requests']) > 100:
                        self.monitoring_data['recent_requests'] = self.monitoring_data['recent_requests'][-100:]
                    
                    return jsonify({
                        "status": "success",
                        "route": route,
                        "latency": latency,
                        "response": result.get('choices', [{}])[0].get('message', {}).get('content', ''),
                        "timestamp": time.time()
                    })
                else:
                    self.monitoring_data['requests']['failed'] += 1
                    return jsonify({
                        "status": "error",
                        "error": response.text,
                        "latency": latency
                    }), 500
                    
            except Exception as e:
                logger.error(f"Test request error: {e}")
                return jsonify({"error": str(e)}), 500
    
    def update_server_statuses(self):
        """Update status of all servers"""
        for server_name, port in self.ports.items():
            if server_name == "dashboard":
                continue
                
            try:
                if server_name == "ollama":
                    response = requests.get(f"http://localhost:{port}/api/tags", timeout=5)
                else:
                    response = requests.get(f"http://localhost:{port}/health", timeout=5)
                
                if response.status_code == 200:
                    self.monitoring_data['servers'][server_name] = {
                        "status": "healthy",
                        "last_check": time.time()
                    }
                else:
                    self.monitoring_data['servers'][server_name] = {
                        "status": "unhealthy",
                        "last_check": time.time()
                    }
                    
            except Exception as e:
                self.monitoring_data['servers'][server_name] = {
                    "status": "down",
                    "last_check": time.time(),
                    "error": str(e)
                }
    
    def update_system_metrics(self):
        """Update system metrics"""
        try:
            self.monitoring_data['system']['cpu_usage'] = psutil.cpu_percent(interval=0.1)
            self.monitoring_data['system']['memory_usage'] = psutil.virtual_memory().percent
            self.monitoring_data['system']['disk_usage'] = psutil.disk_usage('/').percent
        except Exception as e:
            logger.error(f"System metrics error: {e}")
    
    def start_monitoring(self):
        """Start monitoring thread"""
        def monitor():
            while True:
                try:
                    # Update server statuses every 30 seconds
                    self.update_server_statuses()
                    
                    # Update system metrics every 10 seconds
                    self.update_system_metrics()
                    
                    # Log statistics every 60 seconds
                    logger.info(f"📊 Monitoring: Requests={self.monitoring_data['requests']['total']}, "
                              f"Local={self.monitoring_data['requests']['local']}, "
                              f"Cloud={self.monitoring_data['requests']['cloud']}")
                    
                    time.sleep(30)
                    
                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        logger.info("📊 Monitoring started")

# Dashboard HTML template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧟 ZombieCoder Monitoring Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .card h3 {
            margin: 0 0 15px 0;
            color: #4a5568;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 8px 0;
            border-bottom: 1px solid #f7fafc;
        }
        .metric:last-child {
            border-bottom: none;
        }
        .metric-label {
            font-weight: 500;
            color: #2d3748;
        }
        .metric-value {
            font-weight: bold;
            color: #4a5568;
        }
        .status-healthy {
            color: #38a169;
        }
        .status-unhealthy {
            color: #e53e3e;
        }
        .status-down {
            color: #a0aec0;
        }
        .test-section {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .test-input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 15px;
        }
        .test-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        .test-button:hover {
            transform: scale(1.05);
        }
        .test-result {
            margin-top: 15px;
            padding: 15px;
            border-radius: 8px;
            display: none;
        }
        .test-result.success {
            background: #f0fff4;
            border: 1px solid #9ae6b4;
            color: #22543d;
        }
        .test-result.error {
            background: #fed7d7;
            border: 1px solid #feb2b2;
            color: #742a2a;
        }
        .refresh-button {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            transition: background 0.3s ease;
        }
        .refresh-button:hover {
            background: rgba(255,255,255,0.3);
        }
        .loading {
            text-align: center;
            color: #4a5568;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧟 ZombieCoder Monitoring Dashboard</h1>
            <p>Real-time Local vs Cloud Usage Monitoring</p>
        </div>
        
        <button class="refresh-button" onclick="refreshData()">🔄</button>
        
        <div class="test-section">
            <h3>🧪 Test Request</h3>
            <input type="text" class="test-input" id="testMessage" placeholder="Enter a test message..." value="Hello, how are you?">
            <button class="test-button" onclick="testRequest()">Send Test Request</button>
            <div id="testResult" class="test-result"></div>
        </div>
        
        <div class="dashboard" id="dashboard">
            <div class="loading">Loading dashboard data...</div>
        </div>
    </div>

    <script>
        let refreshInterval;
        
        function refreshData() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    updateDashboard(data);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        }
        
        function updateDashboard(data) {
            const dashboard = document.getElementById('dashboard');
            
            dashboard.innerHTML = `
                <div class="card">
                    <h3>📊 Request Statistics</h3>
                    <div class="metric">
                        <span class="metric-label">Total Requests:</span>
                        <span class="metric-value">${data.requests.total}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Local Responses:</span>
                        <span class="metric-value status-healthy">${data.requests.local}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Cloud Fallbacks:</span>
                        <span class="metric-value status-unhealthy">${data.requests.cloud}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Failed Requests:</span>
                        <span class="metric-value status-down">${data.requests.failed}</span>
                    </div>
                </div>
                
                <div class="card">
                    <h3>⚡ Latency Metrics</h3>
                    <div class="metric">
                        <span class="metric-label">Current Latency:</span>
                        <span class="metric-value">${data.latency.current.toFixed(2)}ms</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Local Average:</span>
                        <span class="metric-value">${data.latency.local_avg.toFixed(2)}ms</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Cloud Average:</span>
                        <span class="metric-value">${data.latency.cloud_avg.toFixed(2)}ms</span>
                    </div>
                </div>
                
                <div class="card">
                    <h3>🖥️ System Resources</h3>
                    <div class="metric">
                        <span class="metric-label">CPU Usage:</span>
                        <span class="metric-value">${data.system.cpu_usage.toFixed(1)}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Memory Usage:</span>
                        <span class="metric-value">${data.system.memory_usage.toFixed(1)}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Disk Usage:</span>
                        <span class="metric-value">${data.system.disk_usage.toFixed(1)}%</span>
                    </div>
                </div>
                
                <div class="card">
                    <h3>🔧 Server Status</h3>
                    ${Object.entries(data.servers).map(([server, status]) => `
                        <div class="metric">
                            <span class="metric-label">${server.replace('_', ' ').toUpperCase()}:</span>
                            <span class="metric-value status-${status.status}">${status.status.toUpperCase()}</span>
                        </div>
                    `).join('')}
                </div>
                
                <div class="card">
                    <h3>📈 Recent Requests</h3>
                    ${data.recent_requests.slice(-5).map(req => `
                        <div class="metric">
                            <span class="metric-label">${req.message}</span>
                            <span class="metric-value status-${req.route === 'local' ? 'healthy' : 'unhealthy'}">${req.route} (${req.latency.toFixed(0)}ms)</span>
                        </div>
                    `).join('')}
                </div>
                
                <div class="card">
                    <h3>⏱️ System Info</h3>
                    <div class="metric">
                        <span class="metric-label">Uptime:</span>
                        <span class="metric-value">${data.uptime}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Last Update:</span>
                        <span class="metric-value">${new Date().toLocaleTimeString()}</span>
                    </div>
                </div>
            `;
        }
        
        function testRequest() {
            const message = document.getElementById('testMessage').value;
            const resultDiv = document.getElementById('testResult');
            
            if (!message.trim()) {
                alert('Please enter a test message');
                return;
            }
            
            resultDiv.style.display = 'block';
            resultDiv.className = 'test-result';
            resultDiv.innerHTML = 'Sending test request...';
            
            fetch('/api/test-request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    resultDiv.className = 'test-result success';
                    resultDiv.innerHTML = `
                        <strong>✅ Test Successful!</strong><br>
                        Route: ${data.route}<br>
                        Latency: ${data.latency.toFixed(2)}ms<br>
                        Response: ${data.response.substring(0, 100)}...
                    `;
                } else {
                    resultDiv.className = 'test-result error';
                    resultDiv.innerHTML = `
                        <strong>❌ Test Failed!</strong><br>
                        Error: ${data.error}
                    `;
                }
                
                // Refresh dashboard after test
                setTimeout(refreshData, 1000);
            })
            .catch(error => {
                resultDiv.className = 'test-result error';
                resultDiv.innerHTML = `
                    <strong>❌ Test Error!</strong><br>
                    Error: ${error.message}
                `;
            });
        }
        
        // Auto-refresh every 5 seconds
        refreshInterval = setInterval(refreshData, 5000);
        
        // Initial load
        refreshData();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    dashboard = MonitoringDashboard()
    
    logger.info("🚀 Starting ZombieCoder Monitoring Dashboard...")
    logger.info(f"🌐 Dashboard running on port {dashboard.ports['dashboard']}")
    logger.info("📊 Open http://localhost:9000 to view the dashboard")
    
    dashboard.app.run(host='0.0.0.0', port=dashboard.ports['dashboard'], debug=False)
