'use client';

import { AgentStatus } from '../../components/Agents/AgentStatus';
import { AgentActivityFeed } from '../../components/Agents/AgentActivityFeed';

// Mock data - in real app, this would come from API
const mockAgents = [
    {
        name: 'Researcher',
        status: 'active' as const,
        lastAction: 'Scanning tokens...',
        lastActionTime: '2 minutes ago',
    },
    {
        name: 'Risk Manager',
        status: 'idle' as const,
        lastAction: 'Approved WOOF trade',
        lastActionTime: '5 minutes ago',
    },
    {
        name: 'Trader',
        status: 'active' as const,
        lastAction: 'Executing swap...',
        lastActionTime: '1 minute ago',
    },
    {
        name: 'Supervisor',
        status: 'idle' as const,
        lastAction: 'Monitoring cycle',
        lastActionTime: '10 minutes ago',
    },
    {
        name: 'Narrator',
        status: 'idle' as const,
        lastAction: 'Posted on Twitter',
        lastActionTime: '15 minutes ago',
    },
];

export default function AgentsPage() {
    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold">Agents</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {mockAgents.map((agent) => (
                    <AgentStatus
                        key={agent.name}
                        name={agent.name}
                        status={agent.status}
                        lastAction={agent.lastAction}
                        lastActionTime={agent.lastActionTime}
                    />
                ))}
            </div>

            <AgentActivityFeed />
        </div>
    );
}