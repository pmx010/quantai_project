"""
State management for Quant AI trading system.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from quantai_project.types import (
    TradeState,
    PositionData,
    OpportunityData,
    TradeData,
    FailedTradeData,
)


class StateManager:
    """Manages trading state and history"""
    
    def __init__(self, wallet_address: str):
        """Initialize state manager"""
        self.wallet_address = wallet_address
        self.state: TradeState = {
            "wallet_address": wallet_address,
            "wallet_balance_sol": 0.0,
            "wallet_balance_usdc": 0.0,
            "current_positions": {},
            "total_pnl": 0.0,
            "daily_pnl": 0.0,
            "daily_loss": 0.0,
            "market_opportunities": [],
            "selected_opportunity": None,
            "researcher_analysis": None,
            "risk_check_result": None,
            "supervisor_decision": None,
            "trade_execution_result": None,
            "narrator_output": None,
            "completed_trades": [],
            "failed_trades": [],
            "last_run_time": None,
            "cycle_count": 0,
            "error_log": [],
            "execution_history": [],
        }
    
    def update_wallet_balance(self, sol: float, usdc: float):
        """Update wallet balances"""
        self.state["wallet_balance_sol"] = sol
        self.state["wallet_balance_usdc"] = usdc
    
    def add_position(self, token_mint: str, position: PositionData):
        """Add or update a position"""
        self.state["current_positions"][token_mint] = position
    
    def remove_position(self, token_mint: str):
        """Remove a closed position"""
        if token_mint in self.state["current_positions"]:
            del self.state["current_positions"][token_mint]
    
    def add_completed_trade(self, trade: TradeData):
        """Record a completed trade"""
        trade_id = f"TRADE_{uuid.uuid4().hex[:8]}"
        trade["trade_id"] = trade_id
        self.state["completed_trades"].append(trade)
        
        # Update P&L
        if trade.get("pnl"):
            self.state["total_pnl"] += trade["pnl"]
            self.state["daily_pnl"] += trade["pnl"]
            if trade["pnl"] < 0:
                self.state["daily_loss"] += abs(trade["pnl"])
    
    def add_failed_trade(self, failed_trade: FailedTradeData):
        """Record a failed trade"""
        failed_trade["trade_id"] = f"FAILED_{uuid.uuid4().hex[:8]}"
        self.state["failed_trades"].append(failed_trade)
    
    def add_error(self, error_message: str):
        """Log an error"""
        timestamp = datetime.utcnow().isoformat()
        self.state["error_log"].append(f"[{timestamp}] {error_message}")
    
    def set_researcher_analysis(self, analysis: Dict[str, Any]):
        """Set researcher analysis results"""
        self.state["researcher_analysis"] = analysis
    
    def set_risk_check(self, result: Dict[str, Any]):
        """Set risk check results"""
        self.state["risk_check_result"] = result
    
    def set_supervisor_decision(self, decision: Dict[str, Any]):
        """Set supervisor decision"""
        self.state["supervisor_decision"] = decision
    
    def set_trade_execution(self, result: Dict[str, Any]):
        """Set trade execution results"""
        self.state["trade_execution_result"] = result
    
    def set_narrator_output(self, output: Dict[str, Any]):
        """Set narrator output"""
        self.state["narrator_output"] = output
    
    def get_current_opportunity(self) -> Optional[OpportunityData]:
        """Get current selected opportunity"""
        return self.state.get("selected_opportunity")
    
    def set_current_opportunity(self, opportunity: Optional[OpportunityData]):
        """Set current selected opportunity"""
        self.state["selected_opportunity"] = opportunity
    
    def increment_cycle(self):
        """Increment cycle counter"""
        self.state["cycle_count"] += 1
        self.state["last_run_time"] = datetime.utcnow().isoformat()
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get summary of current portfolio"""
        positions = self.state["current_positions"]
        position_count = len(positions)
        
        total_value = sum(p.get("amount", 0) * p.get("current_price", 0) for p in positions.values())
        
        return {
            "position_count": position_count,
            "total_portfolio_value": total_value,
            "total_pnl": self.state["total_pnl"],
            "daily_pnl": self.state["daily_pnl"],
            "daily_loss": self.state["daily_loss"],
            "win_rate": self._calculate_win_rate(),
        }
    
    def _calculate_win_rate(self) -> float:
        """Calculate win rate from completed trades"""
        trades = self.state["completed_trades"]
        if not trades:
            return 0.0
        
        winning_trades = sum(1 for t in trades if t.get("pnl", 0) > 0)
        return (winning_trades / len(trades)) * 100
    
    def reset_daily_metrics(self):
        """Reset daily metrics (call at daily reset)"""
        self.state["daily_pnl"] = 0.0
        self.state["daily_loss"] = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Export state as dictionary"""
        return self.state
    
    def to_json(self) -> str:
        """Export state as JSON"""
        # Convert non-serializable objects
        state_copy = json.loads(json.dumps(self.state, default=str))
        return json.dumps(state_copy, indent=2)
    
    def get_state(self) -> TradeState:
        """Get current state"""
        return self.state
