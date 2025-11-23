// components/Trading/ControlPanel.tsx
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Switch } from '../ui/switch';
import { api } from '../../lib/api';
import { useSystemStore } from '../../lib/stores/system';

export const ControlPanel = () => {
    const [cycles, setCycles] = useState(1);
    const [interval, setInterval] = useState(30);
    const [isDryRun, setIsDryRun] = useState(false);
    const [dailyLossLimit, setDailyLossLimit] = useState(100);
    const { isRunning } = useSystemStore();

    const handleStart = async () => {
        try {
            await api.startTrading(cycles, interval);
        } catch (error) {
            console.error('Failed to start trading:', error);
        }
    };

    const handleStop = async () => {
        try {
            await api.stopTrading();
        } catch (error) {
            console.error('Failed to stop trading:', error);
        }
    };

    const handleCycle = async () => {
        try {
            await api.runCycle();
        } catch (error) {
            console.error('Failed to run cycle:', error);
        }
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>Cycle Control Panel</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="flex space-x-2">
                    <Button
                        onClick={handleStart}
                        disabled={isRunning}
                        className="flex-1"
                    >
                        ▶ Start Trading
                    </Button>
                    <Button
                        onClick={handleStop}
                        disabled={!isRunning}
                        variant="destructive"
                        className="flex-1"
                    >
                        ◼ Stop
                    </Button>
                    <Button
                        onClick={handleCycle}
                        disabled={!isRunning}
                        variant="outline"
                        className="flex-1"
                    >
                        → Run Cycle
                    </Button>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <Label htmlFor="cycles">Cycles</Label>
                        <Input
                            id="cycles"
                            type="number"
                            value={cycles}
                            onChange={(e) => setCycles(Number(e.target.value))}
                            min={1}
                            max={10}
                        />
                    </div>
                    <div>
                        <Label htmlFor="interval">Interval (seconds)</Label>
                        <Input
                            id="interval"
                            type="number"
                            value={interval}
                            onChange={(e) => setInterval(Number(e.target.value))}
                            min={10}
                            max={300}
                        />
                    </div>
                </div>

                <div className="flex items-center space-x-2">
                    <Switch
                        id="dry-run"
                        checked={isDryRun}
                        onCheckedChange={setIsDryRun}
                    />
                    <Label htmlFor="dry-run">Dry Run Mode</Label>
                </div>

                <div>
                    <Label htmlFor="daily-loss">Daily Loss Limit ($)</Label>
                    <Input
                        id="daily-loss"
                        type="number"
                        value={dailyLossLimit}
                        onChange={(e) => setDailyLossLimit(Number(e.target.value))}
                        min={0}
                    />
                </div>
            </CardContent>
        </Card>
    );
};