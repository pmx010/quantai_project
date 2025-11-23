// lib/stores/trades.ts
import { create } from 'zustand';
import { Trade, TradeFilter } from '../types';

interface TradeState {
    trades: Trade[];
    filteredTrades: Trade[];
    filter: TradeFilter;
    addTrade: (trade: Trade) => void;
    setFilter: (filter: TradeFilter) => void;
    clearTrades: () => void;
}

export const useTradeStore = create<TradeState>((set, get) => ({
    trades: [],
    filteredTrades: [],
    filter: {},
    addTrade: (trade) =>
        set((state) => {
            const newTrades = [trade, ...state.trades];
            return {
                trades: newTrades,
                filteredTrades: applyFilter(newTrades, state.filter),
            };
        }),
    setFilter: (filter) =>
        set((state) => ({
            filter,
            filteredTrades: applyFilter(state.trades, filter),
        })),
    clearTrades: () => set({ trades: [], filteredTrades: [] }),
}));

function applyFilter(trades: Trade[], filter: TradeFilter): Trade[] {
    return trades.filter((trade) => {
        if (filter.status && trade.status !== filter.status) return false;
        if (filter.token && !trade.token.toLowerCase().includes(filter.token.toLowerCase())) return false;
        if (filter.dateRange) {
            const tradeDate = new Date(trade.timestamp);
            const start = new Date(filter.dateRange.start);
            const end = new Date(filter.dateRange.end);
            if (tradeDate < start || tradeDate > end) return false;
        }
        return true;
    });
}