// components/Portfolio/AllocationChart.tsx
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { usePortfolioStore } from '../../lib/stores/portfolio';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

export const AllocationChart = () => {
    const { positions } = usePortfolioStore();

    const data = positions.map((position, index) => ({
        name: position.token,
        value: position.amount * position.currentPrice,
        color: COLORS[index % COLORS.length],
    }));

    if (data.length === 0) {
        return (
            <Card>
                <CardHeader>
                    <CardTitle>Portfolio Allocation</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-muted-foreground">No positions to display</p>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>Portfolio Allocation</CardTitle>
            </CardHeader>
            <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                    <PieChart>
                        <Pie
                            data={data}
                            cx="50%"
                            cy="50%"
                            outerRadius={60}
                            fill="#8884d8"
                            dataKey="value"
                            label={({ name, percent }) => `${name} ${percent ? (percent * 100).toFixed(0) : 0}%`}
                        >
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Pie>
                        <Tooltip formatter={(value: number) => [`$${value.toFixed(2)}`, 'Value']} />
                    </PieChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
};