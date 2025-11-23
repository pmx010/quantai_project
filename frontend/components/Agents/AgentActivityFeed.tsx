// components/Agents/AgentActivityFeed.tsx
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { ScrollArea } from '../ui/scroll-area';
import { useAgentStore } from '../../lib/stores/agents';
import { AGENT_EMOJIS } from '../../lib/constants';
import { formatRelativeTime } from '../../lib/formatters';

export const AgentActivityFeed = () => {
    const { activities } = useAgentStore();

    return (
        <Card>
            <CardHeader>
                <CardTitle>Live Agent Feed</CardTitle>
            </CardHeader>
            <CardContent>
                <ScrollArea className="h-64">
                    <div className="space-y-2">
                        {activities.length === 0 ? (
                            <p className="text-muted-foreground text-center py-4">
                                No recent activity
                            </p>
                        ) : (
                            activities.map((activity) => {
                                const agentKey = activity.agent.toLowerCase().replace(' ', '-') as keyof typeof AGENT_EMOJIS;
                                const emoji = AGENT_EMOJIS[agentKey] || '🤖';

                                return (
                                    <div
                                        key={activity.id}
                                        className="flex items-start space-x-3 p-2 rounded-lg bg-muted/50"
                                    >
                                        <span className="text-lg">{emoji}</span>
                                        <div className="flex-1">
                                            <p className="text-sm">
                                                <span className="font-medium">{activity.agent}:</span> {activity.message}
                                            </p>
                                            <p className="text-xs text-muted-foreground">
                                                {formatRelativeTime(activity.timestamp)}
                                            </p>
                                        </div>
                                    </div>
                                );
                            })
                        )}
                    </div>
                </ScrollArea>
            </CardContent>
        </Card>
    );
};