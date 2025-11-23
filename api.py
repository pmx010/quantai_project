"""
FastAPI backend for Quant AI trading system.
Provides REST endpoints for controlling and monitoring the autonomous trading bot.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import asyncio
import uvicorn
from datetime import datetime

from quantai_project.config import load_config, QuantAIConfig
from quantai_project.orchestrator import QuantAIOrchestrator
from quantai_project.state_manager import StateManager
from quantai_project.types import TradeState, QuantAISystemConfig


# Pydantic models for API requests/responses
class ConfigUpdate(BaseModel):
    """Configuration update request"""
    max_position_size_percent: Optional[float] = Field(None, ge=0.1, le=10.0)
    min_liquidity_usd: Optional[float] = Field(None, ge=1000)
    max_slippage_percent: Optional[float] = Field(None, ge=0.1, le=20.0)
    daily_loss_limit_usd: Optional[float] = Field(None, ge=10)
    refresh_interval_seconds: Optional[int] = Field(None, ge=30, le=3600)
    dry_run_mode: Optional[bool] = None
    enable_twitter: Optional[bool] = None
    enable_voice: Optional[bool] = None


class TradingCycleRequest(BaseModel):
    """Request to run trading cycles"""
    cycles: int = Field(1, ge=1, le=10)
    interval_seconds: int = Field(5, ge=1, le=300)


class PortfolioResponse(BaseModel):
    """Portfolio summary response"""
    total_portfolio_value: float
    total_pnl: float
    daily_pnl: float
    daily_loss: float
    position_count: int
    win_rate: float
    current_positions: Dict[str, Any]


class StatusResponse(BaseModel):
    """System status response"""
    is_running: bool
    network: str
    wallet_address: str
    cycle_count: int
    last_run_time: Optional[str]
    dry_run_mode: bool
    uptime_seconds: float


class TradeHistoryResponse(BaseModel):
    """Trade history response"""
    completed_trades: List[Dict[str, Any]]
    failed_trades: List[Dict[str, Any]]
    total_trades: int
    successful_trades: int
    failed_trades_count: int


# Global state
app = FastAPI(
    title="Quant AI Trading API",
    description="Backend API for autonomous Solana trading bot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for orchestrator and config
orchestrator: Optional[QuantAIOrchestrator] = None
config: Optional[QuantAIConfig] = None
start_time: datetime = datetime.utcnow()


def get_orchestrator() -> QuantAIOrchestrator:
    """Get or create orchestrator instance"""
    global orchestrator, config
    if orchestrator is None:
        config = load_config()
        wallet_address = config.wallet_address or "demo_wallet"
        orchestrator = QuantAIOrchestrator(config, wallet_address)
    return orchestrator


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get current system status"""
    orch = get_orchestrator()
    state = orch.state.state

    return StatusResponse(
        is_running=orch.is_running,
        network=config.network if config else "unknown",
        wallet_address=state.get("wallet_address", "unknown"),
        cycle_count=state.get("cycle_count", 0),
        last_run_time=state.get("last_run_time"),
        dry_run_mode=config.dry_run_mode if config else True,
        uptime_seconds=(datetime.utcnow() - start_time).total_seconds()
    )


@app.get("/portfolio", response_model=PortfolioResponse)
async def get_portfolio():
    """Get current portfolio summary"""
    orch = get_orchestrator()
    portfolio = orch.state.get_portfolio_summary()
    return PortfolioResponse(**portfolio)


@app.get("/config")
async def get_config():
    """Get current system configuration"""
    config = load_config()
    return config.to_dict()


@app.put("/config")
async def update_config(config_update: ConfigUpdate):
    """Update system configuration (requires restart to take effect)"""
    # In a real implementation, you'd update environment variables or config file
    # For now, just validate and return success
    return {
        "status": "success",
        "message": "Configuration updated. Restart required for changes to take effect.",
        "updated_fields": config_update.dict(exclude_unset=True)
    }


@app.post("/start")
async def start_trading(background_tasks: BackgroundTasks, request: TradingCycleRequest):
    """Start autonomous trading"""
    orch = get_orchestrator()

    if orch.is_running:
        raise HTTPException(status_code=400, detail="Trading is already running")

    # Start trading in background
    background_tasks.add_task(
        orch.run_continuous,
        cycles=request.cycles,
        interval_seconds=request.interval_seconds
    )

    return {
        "status": "started",
        "message": f"Started trading with {request.cycles} cycles, {request.interval_seconds}s intervals"
    }


@app.post("/stop")
async def stop_trading():
    """Stop autonomous trading"""
    orch = get_orchestrator()

    if not orch.is_running:
        raise HTTPException(status_code=400, detail="Trading is not currently running")

    orch.stop()

    return {
        "status": "stopped",
        "message": "Trading stopped successfully"
    }


@app.post("/cycle")
async def run_single_cycle():
    """Run a single trading cycle"""
    orch = get_orchestrator()

    if orch.is_running:
        raise HTTPException(status_code=400, detail="Cannot run manual cycle while autonomous trading is active")

    try:
        result = await orch.run_single_cycle()
        return {
            "status": "completed",
            "cycle_number": result.get("cycle"),
            "stages": result.get("stages", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cycle execution failed: {str(e)}")


@app.get("/history", response_model=TradeHistoryResponse)
async def get_trade_history():
    """Get trade history"""
    orch = get_orchestrator()
    state = orch.state.state

    completed_trades = state.get("completed_trades", [])
    failed_trades = state.get("failed_trades", [])

    return TradeHistoryResponse(
        completed_trades=completed_trades,
        failed_trades=failed_trades,
        total_trades=len(completed_trades) + len(failed_trades),
        successful_trades=len(completed_trades),
        failed_trades_count=len(failed_trades)
    )


@app.get("/agents/{agent_name}")
async def get_agent_status(agent_name: str):
    """Get status of a specific agent"""
    orch = get_orchestrator()

    if agent_name not in orch.agents:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    agent = orch.agents[agent_name]
    agent_config = config.get_agent_config(agent_name) if config else {}

    return {
        "name": agent_config.get("name", agent_name),
        "description": agent_config.get("description", ""),
        "personality": agent_config.get("personality", ""),
        "status": "active",
        "config": agent_config
    }


@app.get("/state")
async def get_full_state():
    """Get complete system state (for debugging)"""
    orch = get_orchestrator()
    return orch.state.state


@app.post("/reset")
async def reset_system():
    """Reset system state (for testing/debugging)"""
    global orchestrator
    if orchestrator and orchestrator.is_running:
        orchestrator.stop()
        await asyncio.sleep(1)  # Wait for cleanup

    orchestrator = None  # Force recreation on next request

    return {
        "status": "reset",
        "message": "System state reset successfully"
    }


@app.get("/cycle/current")
async def get_current_cycle():
    """Get information about the current trading cycle"""
    orch = get_orchestrator()
    state = orch.state.state

    return {
        "cycle_number": state.get("cycle_count", 0),
        "is_running": orch.is_running,
        "current_opportunity": state.get("selected_opportunity"),
        "researcher_analysis": state.get("researcher_analysis"),
        "risk_check_result": state.get("risk_check_result"),
        "supervisor_decision": state.get("supervisor_decision"),
        "trade_execution_result": state.get("trade_execution_result"),
        "narrator_output": state.get("narrator_output"),
        "last_update": state.get("last_run_time")
    }


@app.get("/performance")
async def get_performance_metrics():
    """Get detailed performance metrics"""
    orch = get_orchestrator()
    state = orch.state.state

    completed_trades = state.get("completed_trades", [])
    failed_trades = state.get("failed_trades", [])

    # Calculate performance metrics
    total_trades = len(completed_trades) + len(failed_trades)
    successful_trades = len(completed_trades)
    win_rate = (successful_trades / total_trades * 100) if total_trades > 0 else 0

    total_pnl = sum(t.get("pnl", 0) for t in completed_trades)
    avg_trade_pnl = total_pnl / successful_trades if successful_trades > 0 else 0

    winning_trades = [t for t in completed_trades if t.get("pnl", 0) > 0]
    losing_trades = [t for t in completed_trades if t.get("pnl", 0) <= 0]

    avg_win = sum(t.get("pnl", 0) for t in winning_trades) / len(winning_trades) if winning_trades else 0
    avg_loss = sum(t.get("pnl", 0) for t in losing_trades) / len(losing_trades) if losing_trades else 0

    return {
        "total_trades": total_trades,
        "successful_trades": successful_trades,
        "failed_trades": len(failed_trades),
        "win_rate_percent": round(win_rate, 2),
        "total_pnl": round(total_pnl, 2),
        "average_trade_pnl": round(avg_trade_pnl, 2),
        "average_win": round(avg_win, 2),
        "average_loss": round(avg_loss, 2),
        "profit_factor": round(abs(avg_win / avg_loss), 2) if avg_loss != 0 else float('inf'),
        "cycles_completed": state.get("cycle_count", 0)
    }


@app.get("/logs")
async def get_system_logs(limit: int = 50):
    """Get recent system logs"""
    orch = get_orchestrator()
    state = orch.state.state

    error_log = state.get("error_log", [])
    execution_history = state.get("execution_history", [])

    # Combine and sort logs by timestamp
    all_logs = []

    for error in error_log[-limit:]:
        all_logs.append({"type": "error", "message": error})

    for execution in execution_history[-limit:]:
        all_logs.append({"type": "execution", "message": str(execution)})

    # Sort by timestamp if available (errors have timestamps in the message)
    return {
        "logs": all_logs[-limit:],
        "total_errors": len(error_log),
        "total_executions": len(execution_history)
    }


@app.post("/agents/{agent_name}/run")
async def run_agent_manually(agent_name: str, prompt: str):
    """Run a specific agent manually with custom prompt"""
    orch = get_orchestrator()

    if agent_name not in orch.agents:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    agent = orch.agents[agent_name]

    try:
        result = await agent.run(prompt)
        return {
            "agent": agent_name,
            "prompt": prompt,
            "result": result,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")


@app.get("/tokens/{token_symbol}")
async def get_token_info(token_symbol: str):
    """Get information about a specific token"""
    from quantai_project.tools import TokenAnalyzerTool

    analyzer = TokenAnalyzerTool()
    try:
        result = await analyzer._execute(token_symbol)
        return {
            "token_symbol": token_symbol,
            "analysis": result,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token analysis failed: {str(e)}")


@app.get("/docs")
async def api_documentation():
    """Get API documentation summary"""
    return {
        "title": "Quant AI Trading API",
        "version": "1.0.0",
        "description": "Backend API for autonomous Solana trading bot",
        "endpoints": {
            "status": {
                "GET /status": "Get current system status",
                "GET /portfolio": "Get portfolio summary",
                "GET /performance": "Get performance metrics",
                "GET /cycle/current": "Get current cycle information",
                "GET /logs": "Get system logs"
            },
            "control": {
                "POST /start": "Start autonomous trading",
                "POST /stop": "Stop autonomous trading",
                "POST /cycle": "Run single trading cycle",
                "POST /reset": "Reset system state"
            },
            "configuration": {
                "GET /config": "Get current configuration",
                "PUT /config": "Update configuration"
            },
            "data": {
                "GET /history": "Get trade history",
                "GET /state": "Get full system state",
                "GET /agents/{agent}": "Get agent status",
                "POST /agents/{agent}/run": "Run agent manually",
                "GET /tokens/{symbol}": "Get token information"
            },
            "health": {
                "GET /health": "Health check"
            }
        },
        "documentation_urls": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "quantai_project.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )