// lib/stores/agents.ts
import { create } from 'zustand';
import { AgentActivity } from '../types';

interface AgentState {
    activities: AgentActivity[];
    addActivity: (activity: AgentActivity) => void;
    clearActivities: () => void;
}

export const useAgentStore = create<AgentState>((set) => ({
    activities: [],
    addActivity: (activity) =>
        set((state) => ({
            activities: [activity, ...state.activities.slice(0, 99)], // Keep last 100
        })),
    clearActivities: () => set({ activities: [] }),
}));