# Quant AI Dashboard

## Overview

A **real-time trading dashboard** for monitoring and controlling the Quant AI autonomous trading bot. Displays live portfolio data, agent activity, trade history, and system controls.

## Features

### Core Functionalities
- ✅ Real-time portfolio monitoring (P&L, positions, balance)
- ✅ Live agent activity feed (what agents are doing)
- ✅ Trading controls (start/stop cycles, manual execution)
- ✅ Performance analytics (win rate, metrics, history)
- ✅ Configuration management (risk limits, parameters)
- ✅ Trade history with details and replay
- ✅ System health and status monitoring

### Non-Functional Goals
- **Performance**: Real-time updates (WebSocket)
- **Responsiveness**: Works on desktop and tablet
- **Reliability**: Graceful degradation when API unavailable
- **Accessibility**: Clear, intuitive UI
- **Scalability**: Support multiple concurrent connections

## Tech Stack

### Frontend Framework
- React 18+ (component-based, hooks)
- TypeScript (type safety)
- Next.js 14+ (SSR, API routes, deployment)
- TailwindCSS (styling, responsive design)
- shadcn/ui v4 (pre-built components)

### Libraries
- SWR or React Query (data fetching)
- Socket.io (WebSocket for real-time updates)
- Recharts (charts and graphs)
- Zustand (state management)
- date-fns (date/time formatting)

### Build & Deploy
- Vercel (Next.js hosting)
- Docker (containerization)
- GitHub Actions (CI/CD)

## Project Structure

```
quantai_project/frontend/
├── app/
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Home/dashboard page
│   ├── api/
│   │   └── socket.ts     # WebSocket API endpoint
│   ├── dashboard/
│   │   ├── page.tsx      # Main dashboard
│   │   ├── layout.tsx
│   │   └── components/   # Dashboard components
│   ├── trades/
│   │   ├── page.tsx      # Trade history page
│   │   └── [id]/         # Trade detail page
│   ├── agents/
│   │   ├── page.tsx      # Agent management
│   │   └── [name]/       # Agent detail page
│   ├── settings/
│   │   └── page.tsx      # Configuration page
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── StatusBar.tsx
│   │   └── ...
│   ├── hooks/
│   │   ├── useApi.ts          # API data fetching
│   │   ├── useWebSocket.ts    # WebSocket connection
│   │   ├── usePortfolio.ts    # Portfolio state
│   │   ├── useSystemStatus.ts # System status
│   │   └── useAutoRefresh.ts  # Auto-refresh logic
│   ├── lib/
│   │   ├── api.ts             # API client
│   │   ├── types.ts           # TypeScript types
│   │   ├── formatters.ts      # Formatting utilities
│   │   ├── constants.ts       # App constants
│   │   └── socket.ts          # WebSocket client
│   ├── styles/
│   │   ├── globals.css        # Global styles
│   │   └── theme.css          # Theme variables
│   ├── config/
│   │   └── dashboard.config.ts # Dashboard configuration
├── components/           # Shared components
│   ├── Portfolio/
│   │   ├── PortfolioCard.tsx
│   │   ├── PositionsList.tsx
│   │   ├── PnLChart.tsx
│   │   └── AllocationChart.tsx
│   ├── Trading/
│   │   ├── ControlPanel.tsx
│   │   ├── CycleExecutor.tsx
│   │   ├── TradeCard.tsx
│   │   └── TradeTable.tsx
│   ├── Agents/
│   │   ├── AgentStatus.tsx
│   │   ├── AgentCard.tsx
│   │   ├── AgentActivityFeed.tsx
│   │   └── AgentDebugger.tsx
│   ├── Charts/
│   │   ├── WinRateChart.tsx
│   │   ├── PerformanceChart.tsx
│   │   ├── PnLChart.tsx
│   │   └── TimeseriesChart.tsx
│   └── Common/
│       ├── Card.tsx
│       ├── Badge.tsx
│       ├── StatBox.tsx
│       ├── Button.tsx
│       └── Modal.tsx
├── hooks/
├── lib/
├── styles/
├── config/
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── next.config.js
├── Dockerfile
└── .env.example
```

## Installation

### Prerequisites
- Node.js 18+
- npm or yarn

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd quantai/quantai_project/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   Copy `.env.example` to `.env.local` and fill in the values:
   ```bash
   cp .env.example .env.local
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Environment Variables

Create a `.env.local` file in the root of the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SOCKET_URL=http://localhost:8000
NEXT_PUBLIC_NETWORK=devnet
API_TIMEOUT_MS=5000
```

## Usage

### Main Dashboard
- View real-time portfolio value and P&L
- Monitor active positions
- Control trading cycles
- See live agent activity

### Trading Page
- View detailed trade history
- Filter and sort trades
- Execute manual trades

### Agents Page
- Monitor agent status
- Debug agent actions
- Run custom prompts

### Settings Page
- Configure trading parameters
- Manage API keys
- Adjust system settings

## API Integration

The dashboard connects to the Quant AI backend API. Key endpoints:

- `GET /portfolio` - Get portfolio data
- `GET /status` - Get system status
- `POST /start` - Start trading with cycles and interval
- `POST /stop` - Stop trading
- `POST /cycle` - Run a single cycle
- `GET /trades` - Get trade history
- `GET /agents` - Get agent information

WebSocket events:
- `portfolio:update` - Portfolio data updates
- `agent:activity` - Agent activity messages
- `trade:completed` - Trade completion notifications
- `cycle:complete` - Cycle completion
- `system:status` - System status updates

## Development

### Adding Components
Use shadcn/ui for consistent UI components:
```bash
npx shadcn@latest add [component-name]
```

### State Management
Use Zustand stores for global state:
- Portfolio store
- System status store
- Agent activity store
- Trades store

### Styling
- Use TailwindCSS classes
- Follow the design system colors and spacing
- Ensure responsive design

### Testing
- Write unit tests for components
- Test API integrations
- Validate WebSocket connections

## Deployment

### Vercel
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push

### Docker
1. Build the Docker image:
   ```bash
   docker build -t quantai-dashboard .
   ```

2. Run the container:
   ```bash
   docker run -p 3000:3000 quantai-dashboard
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open an issue on GitHub or contact the development team.

---

**Ready to build the most epic trading dashboard! 🚀**
