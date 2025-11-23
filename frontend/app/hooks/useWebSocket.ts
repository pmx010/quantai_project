// hooks/useWebSocket.ts
import { useEffect } from 'react';
import { getSocket } from '../lib/socket';
import { usePortfolioStore } from '../lib/stores/portfolio';
import { useSystemStore } from '../lib/stores/system';
import { useAgentStore } from '../lib/stores/agents';
import { useTradeStore } from '../lib/stores/trades';
import { PortfolioData, SystemStatus, AgentActivity, Trade } from '../lib/types';

export const useWebSocket = () => {
    const updatePortfolio = usePortfolioStore((state) => state.updatePortfolio);
    const updateStatus = useSystemStore((state) => state.updateStatus);
    const addActivity = useAgentStore((state) => state.addActivity);
    const addTrade = useTradeStore((state) => state.addTrade);

    useEffect(() => {
        const socket = getSocket();

        socket.on('portfolio:update', (data: PortfolioData) => {
            updatePortfolio(data);
        });

        socket.on('agent:activity', (data: AgentActivity) => {
            addActivity(data);
        });

        socket.on('trade:completed', (data: Trade) => {
            addTrade(data);
        });

        socket.on('system:status', (data: SystemStatus) => {
            updateStatus(data);
        });

        // Connect if not connected
        if (!socket.connected) {
            socket.connect();
        }

        return () => {
            socket.off('portfolio:update');
            socket.off('agent:activity');
            socket.off('trade:completed');
            socket.off('system:status');
        };
    }, [updatePortfolio, updateStatus, addActivity, addTrade]);
};