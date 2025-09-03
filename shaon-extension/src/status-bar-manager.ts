import * as vscode from 'vscode';

export class StatusBarManager {
    private statusBarItem: vscode.StatusBarItem;
    private currentStatus: 'active' | 'inactive' | 'loading' | 'error' = 'inactive';

    constructor() {
        this.statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Left,
            100
        );
    }

    public initialize(): void {
        this.statusBarItem.command = 'shaon.openPanel';
        this.statusBarItem.tooltip = 'Shaon AI Status - Click to open panel';
        this.statusBarItem.show();
        this.setStatus('inactive');
    }

    public setStatus(status: 'active' | 'inactive' | 'loading' | 'error'): void {
        this.currentStatus = status;

        switch (status) {
            case 'active':
                this.statusBarItem.text = '$(light-bulb) Shaon AI Active';
                this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.prominentBackground');
                this.statusBarItem.color = new vscode.ThemeColor('statusBarItem.prominentForeground');
                break;
            case 'inactive':
                this.statusBarItem.text = '$(light-bulb) Shaon AI Inactive';
                this.statusBarItem.backgroundColor = undefined;
                this.statusBarItem.color = undefined;
                break;
            case 'loading':
                this.statusBarItem.text = '$(sync~spin) Shaon AI Loading';
                this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
                this.statusBarItem.color = new vscode.ThemeColor('statusBarItem.warningForeground');
                break;
            case 'error':
                this.statusBarItem.text = '$(error) Shaon AI Error';
                this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
                this.statusBarItem.color = new vscode.ThemeColor('statusBarItem.errorForeground');
                break;
        }
    }

    public getStatus(): string {
        return this.currentStatus;
    }

    public dispose(): void {
        this.statusBarItem.dispose();
    }
}
