// lib/stores/portfolio.ts
import { create } from 'zustand';
import { PortfolioData, Position } from '../types';

interface PortfolioState {
    portfolioValue: number;
    totalPnL: number;
    dailyPnL: number;
    dailyLoss: number;
    positions: Position[];
    updatePortfolio: (data: PortfolioData) => void;
}

export const usePortfolioStore = create<PortfolioState>((set) => ({
    portfolioValue: 0,
    totalPnL: 0,
    dailyPnL: 0,
    dailyLoss: 0,
    positions: [],
    updatePortfolio: (data) =>
        set({
            portfolioValue: data.totalValue,
            totalPnL: data.totalPnL,
            dailyPnL: data.dailyPnL,
            dailyLoss: data.dailyLoss,
            positions: data.positions,
        }),
}));