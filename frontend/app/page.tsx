'use client';

import { StatusBar } from './components/StatusBar';
import { PortfolioCard } from '../components/Portfolio/PortfolioCard';
import { PositionsList } from '../components/Portfolio/PositionsList';
import { PnLChart } from '../components/Portfolio/PnLChart';
import { AllocationChart } from '../components/Portfolio/AllocationChart';
import { ControlPanel } from '../components/Trading/ControlPanel';
import { AgentActivityFeed } from '../components/Agents/AgentActivityFeed';
import { useWebSocket } from './hooks/useWebSocket';

export default function Dashboard() {
  useWebSocket(); // Connect to WebSocket

  return (
    <div className="space-y-6">
      <StatusBar />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <PortfolioCard />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <PnLChart />
            <AllocationChart />
          </div>
          <PositionsList />
        </div>

        <div className="space-y-6">
          <ControlPanel />
          <AgentActivityFeed />
        </div>
      </div>
    </div>
  );
}
