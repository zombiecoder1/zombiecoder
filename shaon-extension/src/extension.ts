import * as vscode from 'vscode';
import { ShaonAPI } from './shaon-api';
import { StatusBarManager } from './status-bar-manager';

export function activate(context: vscode.ExtensionContext) {
    console.log('Shaon AI Extension is now active!');

    const shaonAPI = new ShaonAPI();
    const statusBar = new StatusBarManager();

    // Initialize status bar
    statusBar.initialize();

    // Register commands
    let startChat = vscode.commands.registerCommand('shaon.startChat', async () => {
        const message = await vscode.window.showInputBox({
            prompt: 'Enter your message for Shaon AI',
            placeHolder: 'Ask me anything...'
        });

        if (message) {
            try {
                statusBar.setStatus('loading');
                const response = await shaonAPI.chatWithAgent(message);
                vscode.window.showInformationMessage(`Shaon: ${response.response}`);
                statusBar.setStatus('active');
            } catch (error) {
                vscode.window.showErrorMessage(`Error: ${error}`);
                statusBar.setStatus('error');
            }
        }
    });

    let openPanel = vscode.commands.registerCommand('shaon.openPanel', () => {
        const panel = vscode.window.createWebviewPanel(
            'shaonPanel',
            'Shaon AI Panel',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        panel.webview.html = getWebviewContent();
    });

    let voiceChat = vscode.commands.registerCommand('shaon.voiceChat', async () => {
        vscode.window.showInformationMessage('Voice chat feature coming soon!');
    });

    let switchAgent = vscode.commands.registerCommand('shaon.switchAgent', async () => {
        const agents = ['সাহন ভাই', 'মুসকান', 'ভাবি', 'বাঘ', 'হান্টার'];
        const selected = await vscode.window.showQuickPick(agents, {
            placeHolder: 'Select AI Agent'
        });

        if (selected) {
            context.globalState.update('selectedAgent', selected);
            vscode.window.showInformationMessage(`Switched to ${selected}`);
        }
    });

    let analyzeCode = vscode.commands.registerCommand('shaon.analyzeCode', async () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const code = editor.document.getText();
            const selectedAgent = context.globalState.get('selectedAgent', 'সাহন ভাই');
            
            try {
                statusBar.setStatus('loading');
                const response = await shaonAPI.chatWithAgent(`Analyze this code: ${code}`, selectedAgent);
                vscode.window.showInformationMessage(`Analysis: ${response.response}`);
                statusBar.setStatus('active');
            } catch (error) {
                vscode.window.showErrorMessage(`Error: ${error}`);
                statusBar.setStatus('error');
            }
        }
    });

    let copilotChat = vscode.commands.registerCommand('shaon.copilotChat', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        // Get cursor position
        const position = editor.selection.active;
        const line = editor.document.lineAt(position.line);
        const selectedText = editor.document.getText(editor.selection);

        // Create input box for copilot-style chat
        const message = await vscode.window.showInputBox({
            prompt: 'Shaon Copilot Chat',
            placeHolder: 'Ask about the code, request changes, or get help...',
            value: selectedText ? `Selected code: ${selectedText}\n\n` : ''
        });

        if (message) {
            try {
                statusBar.setStatus('loading');
                const selectedAgent = context.globalState.get('selectedAgent', 'সাহন ভাই');
                const response = await shaonAPI.chatWithAgent(message, selectedAgent);
                
                // Show response in a new document
                const doc = await vscode.workspace.openTextDocument({
                    content: `Shaon AI Response (${selectedAgent}):\n\n${response.response}\n\n---\nOriginal Query: ${message}`,
                    language: 'markdown'
                });
                
                await vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
                statusBar.setStatus('active');
            } catch (error) {
                vscode.window.showErrorMessage(`Error: ${error}`);
                statusBar.setStatus('error');
            }
        }
    });

    // Register all commands
    context.subscriptions.push(
        startChat, 
        openPanel, 
        voiceChat, 
        switchAgent, 
        analyzeCode, 
        copilotChat
    );

    // Check server status on activation
    checkServerStatus(shaonAPI, statusBar);

    // Set up periodic status checks
    setInterval(() => {
        checkServerStatus(shaonAPI, statusBar);
    }, 30000); // Check every 30 seconds
}

async function checkServerStatus(shaonAPI: ShaonAPI, statusBar: StatusBarManager) {
    try {
        const status = await shaonAPI.getSystemStatus();
        if (status) {
            statusBar.setStatus('active');
        } else {
            statusBar.setStatus('inactive');
        }
    } catch (error) {
        statusBar.setStatus('error');
    }
}

function getWebviewContent() {
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shaon AI Panel</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                padding: 20px;
                background: #1e1e1e;
                color: #ffffff;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .agent-selector {
                margin-bottom: 20px;
                text-align: center;
            }
            .agent-selector select {
                padding: 8px 12px;
                background: #252526;
                color: #ffffff;
                border: 1px solid #333;
                border-radius: 4px;
                font-size: 14px;
            }
            .chat-area {
                height: 400px;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 20px;
                overflow-y: auto;
                background: #252526;
            }
            .input-area {
                display: flex;
                gap: 10px;
            }
            input {
                flex: 1;
                padding: 10px;
                border: 1px solid #333;
                border-radius: 4px;
                background: #252526;
                color: #ffffff;
            }
            button {
                padding: 10px 20px;
                background: #007acc;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background: #005a9e;
            }
            .message {
                margin-bottom: 10px;
                padding: 8px;
                border-radius: 4px;
            }
            .user-message {
                background: #2d2d30;
                text-align: right;
            }
            .ai-message {
                background: #1e1e1e;
                border-left: 3px solid #007acc;
            }
            .status-indicator {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                margin-right: 8px;
            }
            .status-active {
                background: #4caf50;
            }
            .status-inactive {
                background: #f44336;
            }
            .status-loading {
                background: #ff9800;
                animation: pulse 1s infinite;
            }
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Shaon AI Panel</h1>
                <p>ZombieCoder AI Extension with Advanced Features</p>
                <div class="status-indicator status-active"></div>
                <span>System Active</span>
            </div>
            
            <div class="agent-selector">
                <label for="agentSelect">Select Agent: </label>
                <select id="agentSelect">
                    <option value="সাহন ভাই">সাহন ভাই 👨‍💻</option>
                    <option value="মুসকান">মুসকান 👧</option>
                    <option value="ভাবি">ভাবি 👩‍💼</option>
                    <option value="বাঘ">বাঘ 🐯</option>
                    <option value="হান্টার">হান্টার 🔍</option>
                </select>
            </div>
            
            <div class="chat-area" id="chatArea">
                <div class="message ai-message">
                    Hello! I'm Shaon AI. How can I help you today?
                </div>
            </div>
            
            <div class="input-area">
                <input type="text" id="messageInput" placeholder="Type your message...">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
        
        <script>
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (message) {
                    addMessage(message, 'user');
                    input.value = '';
                    // Here you would call the API
                    setTimeout(() => {
                        addMessage('I received your message: ' + message, 'ai');
                    }, 1000);
                }
            }
            
            function addMessage(text, sender) {
                const chatArea = document.getElementById('chatArea');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message ' + sender + '-message';
                messageDiv.textContent = text;
                chatArea.appendChild(messageDiv);
                chatArea.scrollTop = chatArea.scrollHeight;
            }
            
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>`;
}

export function deactivate() {
    console.log('Shaon AI Extension is now deactivated!');
}
