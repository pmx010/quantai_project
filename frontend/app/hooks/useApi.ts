// hooks/useApi.ts
import useSWR from 'swr';
import { api } from '../lib/api';

export const usePortfolio = () => {
    return useSWR('portfolio', api.getPortfolio, {
        refreshInterval: 5000, // 5 seconds
    });
};

export const useSystemStatus = () => {
    return useSWR('status', api.getStatus, {
        refreshInterval: 5000,
    });
};

export const useTrades = () => {
    return useSWR('trades', api.getTrades, {
        refreshInterval: 10000, // 10 seconds
    });
};

export const useAgents = () => {
    return useSWR('agents', api.getAgents, {
        refreshInterval: 30000, // 30 seconds
    });
};