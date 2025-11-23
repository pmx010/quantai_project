// components/Trading/TradeTable.tsx
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../ui/table';
import { useTradeStore } from '../../lib/stores/trades';
import { formatCurrency, formatDate } from '../../lib/formatters';
import { TradeFilter } from '../../lib/types';

export const TradeTable = () => {
    const { filteredTrades, setFilter } = useTradeStore();
    const [searchToken, setSearchToken] = useState('');
    const [statusFilter, setStatusFilter] = useState<string>('all');

    const handleFilterChange = () => {
        const filter: TradeFilter = {};
        if (searchToken) filter.token = searchToken;
        if (statusFilter !== 'all') filter.status = statusFilter as any;
        setFilter(filter);
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>Trade History</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="flex space-x-2 mb-4">
                    <Input
                        placeholder="Search by token..."
                        value={searchToken}
                        onChange={(e) => setSearchToken(e.target.value)}
                        className="flex-1"
                    />
                    <Select value={statusFilter} onValueChange={setStatusFilter}>
                        <SelectTrigger className="w-32">
                            <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="all">All</SelectItem>
                            <SelectItem value="win">Win</SelectItem>
                            <SelectItem value="loss">Loss</SelectItem>
                            <SelectItem value="pending">Pending</SelectItem>
                        </SelectContent>
                    </Select>
                    <Button onClick={handleFilterChange}>Filter</Button>
                </div>

                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Token</TableHead>
                            <TableHead>Type</TableHead>
                            <TableHead>Amount</TableHead>
                            <TableHead>Entry</TableHead>
                            <TableHead>Exit</TableHead>
                            <TableHead>P&L</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Time</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {filteredTrades.map((trade) => (
                            <TableRow key={trade.id}>
                                <TableCell>{trade.token}</TableCell>
                                <TableCell className="capitalize">{trade.type}</TableCell>
                                <TableCell>{trade.amount}</TableCell>
                                <TableCell>{formatCurrency(trade.entryPrice)}</TableCell>
                                <TableCell>{trade.exitPrice ? formatCurrency(trade.exitPrice) : '-'}</TableCell>
                                <TableCell className={trade.pnl && trade.pnl >= 0 ? 'text-green-600' : 'text-red-600'}>
                                    {trade.pnl ? formatCurrency(trade.pnl) : '-'}
                                </TableCell>
                                <TableCell>
                                    <span className={`px-2 py-1 rounded text-xs ${trade.status === 'completed' ? 'bg-green-100 text-green-800' :
                                            trade.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                                                'bg-red-100 text-red-800'
                                        }`}>
                                        {trade.status}
                                    </span>
                                </TableCell>
                                <TableCell>{formatDate(trade.timestamp)}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CardContent>
        </Card>
    );
};