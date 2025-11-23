'use client';

import { TradeTable } from '../components/Trading/TradeTable';

export default function TradesPage() {
    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold">Trading</h1>
            <TradeTable />
        </div>
    );
}