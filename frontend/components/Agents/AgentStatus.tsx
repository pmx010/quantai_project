// components/Agents/AgentStatus.tsx
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { AGENT_EMOJIS, AGENT_COLORS } from '../../lib/constants';

interface AgentStatusProps {
    name: string;
    status: 'active' | 'idle' | 'error';
    lastAction: string;
    lastActionTime: string;
}

export const AgentStatus = ({
    name,
    status,
    lastAction,
    lastActionTime
}: AgentStatusProps) => {
    const getStatusColor = () => {
        switch (status) {
            case 'active':
                return 'default';
            case 'idle':
                return 'secondary';
            case 'error':
                return 'destructive';
            default:
                return 'secondary';
        }
    };

    const agentKey = name.toLowerCase().replace(' ', '-') as keyof typeof AGENT_EMOJIS;
    const emoji = AGENT_EMOJIS[agentKey] || '🤖';
    const color = AGENT_COLORS[agentKey] || '#666';

    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium flex items-center">
                    <span className="mr-2">{emoji}</span>
                    {name}
                </CardTitle>
                <Badge variant={getStatusColor()}>{status}</Badge>
            </CardHeader>
            <CardContent>
                <p className="text-sm text-muted-foreground">{lastAction}</p>
                <p className="text-xs text-muted-foreground mt-1">{lastActionTime}</p>
            </CardContent>
        </Card>
    );
};