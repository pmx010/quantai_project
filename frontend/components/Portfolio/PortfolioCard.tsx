// components/Portfolio/PortfolioCard.tsx
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { StatBox } from '../Common/StatBox';
import { usePortfolioStore } from '../../lib/stores/portfolio';
import { formatCurrency, formatPercentage } from '../../lib/formatters';

export const PortfolioCard = () => {
    const { portfolioValue, totalPnL, dailyPnL, dailyLoss } = usePortfolioStore();

    const pnlColor = totalPnL >= 0 ? 'up' : 'down';

    return (
        <Card>
            <CardHeader>
                <CardTitle>Portfolio Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                    <StatBox
                        title="Total Value"
                        value={formatCurrency(portfolioValue)}
                        trend={pnlColor}
                    />
                    <StatBox
                        title="Total P&L"
                        value={formatCurrency(totalPnL)}
                        subtitle={formatPercentage(totalPnL / (portfolioValue - totalPnL) || 0)}
                        trend={pnlColor}
                    />
                </div>
                <div className="grid grid-cols-2 gap-4">
                    <StatBox
                        title="Daily P&L"
                        value={formatCurrency(dailyPnL)}
                        trend={dailyPnL >= 0 ? 'up' : 'down'}
                    />
                    <StatBox
                        title="Daily Loss"
                        value={formatCurrency(dailyLoss)}
                        trend="down"
                    />
                </div>
            </CardContent>
        </Card>
    );
};