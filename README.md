<img width="1555" height="892" alt="image" src="https://github.com/user-attachments/assets/5ae0888c-52ff-4c46-b8ee-b141abb37ed0" />



# QuantAI Project

Core implementation of the Quant AI autonomous trading system with 5 specialized AI agents for trading. Built with SpoonOS framework.

## Architecture

### Core Modules
- **`config.py`** - Configuration & environment variables
- **`types.py`** - Type definitions for state management
- **`state_manager.py`** - Trade state & portfolio tracking
- **`orchestrator.py`** - Multi-agent coordination
- **`utils.py`** - Helper functions
- **`api.py`** - FastAPI backend server

### Agents (`agents/`)
5 specialized AI agents with distinct roles:
- **Researcher** - Finds trading opportunities
- **Risk Manager** - Assesses and vetoes risky trades
- **Trader** - Executes swaps via Jupiter
- **Narrator** - Announces trades with memes
- **Supervisor** - Makes final approval decisions

### Tools (`tools/`)
- **Token Analyzer** - Market data & metrics
- **Liquidity Checker** - Risk assessment
- **Trade Executor** - Jupiter swap execution
- **Portfolio Manager** - Position tracking

## Key Classes

### QuantAIOrchestrator
```python
orchestrator = QuantAIOrchestrator(config)
await orchestrator.run_single_cycle()
```

### StateManager
```python
state = StateManager()
portfolio = state.get_portfolio_summary()
```

### Base Agent
```python
class MyAgent(QuantAIBaseAgent):
    name = "My Agent"
    personality = "Agent style"
    system_prompt = "Instructions"
```

## Usage

### Basic Setup
```python
from quantai_project.config import load_config
from quantai_project.orchestrator import QuantAIOrchestrator

config = load_config()
orchestrator = QuantAIOrchestrator(config)
result = await orchestrator.run_single_cycle()
```

### API Server
```python
from quantai_project.api import create_app
app = create_app()
# uvicorn quantai_project.api:app --reload
```

## Configuration

Key environment variables:
- `SOLANA_NETWORK` - devnet/mainnet
- `OPENAI_API_KEY` - LLM provider
- `MAX_POSITION_SIZE_PERCENT` - Risk limit (1%)
- `DAILY_LOSS_LIMIT_USD` - Stop-loss ($100)

## Safety Features

- Devnet mode for safe testing
- 1% max position size per trade
- Daily loss limits
- Rugpull detection
- Slippage protection (5% max)

## Development

### Adding Agents
1. Inherit from `QuantAIBaseAgent`
2. Implement methods & personality
3. Add to orchestrator

### Adding Tools
1. Inherit from `QuantAITool`
2. Implement `_execute()` method

## API Endpoints

REST API for monitoring: `/status`, `/portfolio`, `/cycle`, `/start`, `/stop`

See main README for full API docs.

## License

MIT License
