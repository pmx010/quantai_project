// lib/types.ts

export interface Position {
    token: string;
    amount: number;
    entryPrice: number;
    currentPrice: number;
    unrealizedPnL: number;
    status: 'up' | 'down' | 'neutral';
}

export interface Trade {
    id: string;
    token: string;
    type: 'buy' | 'sell';
    amount: number;
    entryPrice: number;
    exitPrice?: number;
    pnl?: number;
    status: 'pending' | 'completed' | 'failed';
    timestamp: string;
    txHash?: string;
}

export interface AgentActivity {
    id: string;
    agent: string;
    action: string;
    message: string;
    timestamp: string;
}

export interface PortfolioData {
    totalValue: number;
    totalPnL: number;
    dailyPnL: number;
    dailyLoss: number;
    positions: Position[];
    timestamp: string;
}

export interface SystemStatus {
    isRunning: boolean;
    network: 'devnet' | 'mainnet';
    walletAddress: string;
    cycleCount: number;
    lastRunTime: string;
    uptime: number;
}

export interface TradeFilter {
    status?: 'win' | 'loss' | 'pending';
    token?: string;
    dateRange?: {
        start: string;
        end: string;
    };
}