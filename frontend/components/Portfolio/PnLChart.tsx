// components/Portfolio/PnLChart.tsx
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// Mock data - in real app, this would come from API
const data = [
    { time: '00:00', pnl: 0 },
    { time: '04:00', pnl: 25 },
    { time: '08:00', pnl: 50 },
    { time: '12:00', pnl: 75 },
    { time: '16:00', pnl: 100 },
    { time: '20:00', pnl: 125 },
];

export const PnLChart = () => {
    return (
        <Card>
            <CardHeader>
                <CardTitle>P&L Over Time</CardTitle>
            </CardHeader>
            <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="time" />
                        <YAxis />
                        <Tooltip
                            formatter={(value: number) => [`$${value}`, 'P&L']}
                        />
                        <Line
                            type="monotone"
                            dataKey="pnl"
                            stroke="#0066FF"
                            strokeWidth={2}
                            dot={{ fill: '#0066FF' }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
};