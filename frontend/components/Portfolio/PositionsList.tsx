// components/Portfolio/PositionsList.tsx
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { usePortfolioStore } from '../../lib/stores/portfolio';
import { formatCurrency, formatNumber } from '../../lib/formatters';
import { POSITION_STATUSES } from '../../lib/constants';

export const PositionsList = () => {
    const { positions } = usePortfolioStore();

    if (positions.length === 0) {
        return (
            <Card>
                <CardHeader>
                    <CardTitle>Current Positions</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-muted-foreground">No active positions</p>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>Current Positions</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="space-y-2">
                    {positions.map((position, index) => (
                        <div
                            key={index}
                            className="flex items-center justify-between p-3 border rounded-lg"
                        >
                            <div className="flex items-center space-x-3">
                                <span className="text-lg">{POSITION_STATUSES[position.status]}</span>
                                <div>
                                    <p className="font-medium">{position.token}</p>
                                    <p className="text-sm text-muted-foreground">
                                        {formatNumber(position.amount)} coins
                                    </p>
                                </div>
                            </div>
                            <div className="text-right">
                                <p className="font-medium">
                                    {formatCurrency(position.unrealizedPnL)}
                                </p>
                                <p className="text-sm text-muted-foreground">
                                    Entry: {formatCurrency(position.entryPrice)}
                                </p>
                            </div>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
};