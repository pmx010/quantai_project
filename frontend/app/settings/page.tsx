'use client';

import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Switch } from '../../components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';

export default function SettingsPage() {
    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold">Settings</h1>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>Trading Parameters</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div>
                            <Label htmlFor="max-position">Max Position Size (%)</Label>
                            <Input id="max-position" type="number" defaultValue={10} />
                        </div>
                        <div>
                            <Label htmlFor="min-liquidity">Min Liquidity (USD)</Label>
                            <Input id="min-liquidity" type="number" defaultValue={10000} />
                        </div>
                        <div>
                            <Label htmlFor="max-slippage">Max Slippage (%)</Label>
                            <Input id="max-slippage" type="number" defaultValue={1} />
                        </div>
                        <div>
                            <Label htmlFor="daily-loss">Daily Loss Limit (USD)</Label>
                            <Input id="daily-loss" type="number" defaultValue={100} />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Network Settings</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div>
                            <Label htmlFor="network">Network</Label>
                            <Select defaultValue="devnet">
                                <SelectTrigger>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="devnet">Devnet</SelectItem>
                                    <SelectItem value="mainnet">Mainnet</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div>
                            <Label htmlFor="wallet">Wallet Address</Label>
                            <Input id="wallet" defaultValue="..." />
                        </div>
                        <div>
                            <Label htmlFor="rpc">RPC Endpoint</Label>
                            <Input id="rpc" defaultValue="https://api.devnet.solana.com" />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Optional Features</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-center space-x-2">
                            <Switch id="twitter" />
                            <Label htmlFor="twitter">Enable Twitter</Label>
                        </div>
                        <div className="flex items-center space-x-2">
                            <Switch id="voice" />
                            <Label htmlFor="voice">Enable Voice</Label>
                        </div>
                        <div className="flex items-center space-x-2">
                            <Switch id="logging" />
                            <Label htmlFor="logging">Enable Logging</Label>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>API Keys</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div>
                            <Label htmlFor="openai">OpenAI API Key</Label>
                            <Input id="openai" type="password" placeholder="sk-..." />
                        </div>
                        <div>
                            <Label htmlFor="twitter-consumer">Twitter Consumer Key</Label>
                            <Input id="twitter-consumer" type="password" />
                        </div>
                        <div>
                            <Label htmlFor="elevenlabs">ElevenLabs Key</Label>
                            <Input id="elevenlabs" type="password" />
                        </div>
                    </CardContent>
                </Card>
            </div>

            <div className="flex space-x-4">
                <Button>Save Settings</Button>
                <Button variant="outline">Reset to Default</Button>
                <Button variant="outline">Export Config</Button>
            </div>
        </div>
    );
}