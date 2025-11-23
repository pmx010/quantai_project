// lib/stores/system.ts
import { create } from 'zustand';
import { SystemStatus } from '../types';

interface SystemState extends SystemStatus {
    updateStatus: (data: SystemStatus) => void;
}

export const useSystemStore = create<SystemState>((set) => ({
    isRunning: false,
    network: 'devnet',
    walletAddress: '',
    cycleCount: 0,
    lastRunTime: '',
    uptime: 0,
    updateStatus: (data) =>
        set({
            isRunning: data.isRunning,
            network: data.network,
            walletAddress: data.walletAddress,
            cycleCount: data.cycleCount,
            lastRunTime: data.lastRunTime,
            uptime: data.uptime,
        }),
}));