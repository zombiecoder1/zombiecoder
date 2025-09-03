export interface ShaonMessage {
    message: string;
    agent: string;
    timestamp: string;
    response?: string;
    status: 'pending' | 'success' | 'error';
    agent_emoji?: string;
    agent_color?: string;
    agent_capabilities?: string[];
    processing_time?: number;
    memory_stats?: any;
}

export interface SystemStatus {
    system: string;
    agents: Record<string, any>;
    system_status: any;
    memory_stats: any;
    ollama_url: string;
    default_model: string;
    timestamp: string;
}

export class ShaonAPI {
    private baseUrl = 'http://localhost:12345';

    async chatWithAgent(message: string, agent: string = 'সাহন ভাই'): Promise<ShaonMessage> {
        try {
            const response = await fetch(`${this.baseUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message,
                    agent
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json() as any;

            return {
                message,
                agent: data.agent || agent,
                timestamp: data.timestamp || new Date().toISOString(),
                response: data.response,
                status: 'success',
                agent_emoji: data.agent_emoji,
                agent_color: data.agent_color,
                agent_capabilities: data.agent_capabilities,
                processing_time: data.processing_time,
                memory_stats: data.memory_stats
            };
        } catch (error) {
            console.error('Chat Error:', error);
            return {
                message,
                agent,
                timestamp: new Date().toISOString(),
                status: 'error'
            };
        }
    }

    async getSystemStatus(): Promise<SystemStatus | null> {
        try {
            const response = await fetch(`${this.baseUrl}/status`);
            if (response.ok) {
                return await response.json() as SystemStatus;
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        } catch (error) {
            console.error('Status Error:', error);
            return null;
        }
    }

    async getSystemInfo(): Promise<any> {
        try {
            const response = await fetch(`${this.baseUrl}/info`);
            if (response.ok) {
                return await response.json();
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        } catch (error) {
            console.error('Info Error:', error);
            return null;
        }
    }

    async testConnection(): Promise<boolean> {
        try {
            const response = await fetch(`${this.baseUrl}/status`);
            return response.ok;
        } catch (error) {
            console.error('Connection Test Error:', error);
            return false;
        }
    }
}
