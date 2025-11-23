// app/components/StatusBar.tsx
import { Badge } from '../../components/ui/badge';
import { useSystemStore } from '../../lib/stores/system';
import { formatRelativeTime } from '../../lib/formatters';

export const StatusBar = () => {
    const { isRunning, network, walletAddress, lastRunTime } = useSystemStore();

    return (
        <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
            <div className="flex items-center space-x-4">
                <Badge variant={isRunning ? 'default' : 'destructive'}>
                    {isRunning ? '🟢 Running' : '🔴 Stopped'}
                </Badge>
                <Badge variant="outline">
                    🌐 {network}
                </Badge>
                <span className="text-sm text-muted-foreground">
                    Wallet: {walletAddress || 'Not connected'}
                </span>
            </div>
            <div className="text-sm text-muted-foreground">
                Last cycle: {lastRunTime ? formatRelativeTime(lastRunTime) : 'Never'}
            </div>
        </div>
    );
};