// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = {
    async getPortfolio(): Promise<any> {
        const res = await fetch(`${API_BASE_URL}/portfolio`);
        if (!res.ok) throw new Error('Failed to fetch portfolio');
        return res.json();
    },

    async getStatus(): Promise<any> {
        const res = await fetch(`${API_BASE_URL}/status`);
        if (!res.ok) throw new Error('Failed to fetch status');
        return res.json();
    },

    async startTrading(cycles: number, interval: number): Promise<any> {
        const res = await fetch(`${API_BASE_URL}/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cycles, interval_seconds: interval })
        });
        if (!res.ok) throw new Error('Failed to start trading');
        return res.json();
    },

    async stopTrading(): Promise<any> {
        const res = await fetch(`${API_BASE_URL}/stop`, {
            method: 'POST'
        });
        if (!res.ok) throw new Error('Failed to stop trading');
        return res.json();
    },

    async runCycle(): Promise<any> {
        const res = await fetch(`${API_BASE_URL}/cycle`, {
            method: 'POST'
        });
        if (!res.ok) throw new Error('Failed to run cycle');
        return res.json();
    },

    async getTrades(): Promise<any> {
        const res = await fetch(`${API_BASE_URL}/trades`);
        if (!res.ok) throw new Error('Failed to fetch trades');
        return res.json();
    },

    async getAgents(): Promise<any> {
        const res = await fetch(`${API_BASE_URL}/agents`);
        if (!res.ok) throw new Error('Failed to fetch agents');
        return res.json();
    }
};