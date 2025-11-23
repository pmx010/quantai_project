"""
Type definitions for Quant AI trading system.
"""

from typing import TypedDict, Dict, List, Optional, Any
from datetime import datetime


class TokenMetadata(TypedDict, total=False):
    """Token information"""
    mint: str
    symbol: str
    name: str
    decimals: int
    market_cap_usd: float
    price_usd: float
    volume_24h_usd: float
    price_change_24h_percent: float
    holder_count: int
    top_holder_percent: float
    liquidity_usd: float
    is_new_launch: bool
    age_hours: float


class PositionData(TypedDict, total=False):
    """Active trading position"""
    token_mint: str
    token_symbol: str
    amount: float
    entry_price: float
    entry_time: str
    current_price: float
    unrealized_pnl: float
    unrealized_pnl_percent: float


class OpportunityData(TypedDict, total=False):
    """Trading opportunity identified by researcher"""
    token_mint: str
    token_symbol: str
    alpha_score: float  # 0-100
    reasoning: str
    price: float
    volume: float
    market_cap: float
    timestamp: str


class ResearcherAnalysis(TypedDict, total=False):
    """Output from Researcher agent"""
    opportunities: List[OpportunityData]
    market_sentiment: str
    top_pick: Optional[OpportunityData]
    analysis_time: str


class RiskCheckResult(TypedDict, total=False):
    """Output from Risk Manager agent"""
    recommendation: str  # "PASS" or "VETO"
    confidence_score: float  # 0-100
    liquidity_check: str
    holder_check: str
    rug_score: float  # 0-100, higher = more risky
    reasoning: str


class SupervisorDecision(TypedDict, total=False):
    """Output from Supervisor agent"""
    decision: str  # "GO" or "NO-GO"
    rationale: str
    portfolio_impact: str
    daily_loss_check: str


class TradeExecutionResult(TypedDict, total=False):
    """Output from Trader agent"""
    success: bool
    transaction_hash: Optional[str]
    error_message: Optional[str]
    swap_details: Dict[str, Any]
    execution_time: str


class NarratorOutput(TypedDict, total=False):
    """Output from Narrator agent"""
    tweet_text: str
    voice_script: Optional[str]
    meme_description: str
    humor_level: str  # "mild", "medium", "maximum"


class TradeData(TypedDict, total=False):
    """Completed trade record"""
    trade_id: str
    token_symbol: str
    token_mint: str
    direction: str  # "BUY" or "SELL"
    amount: float
    price: float
    transaction_hash: str
    timestamp: str
    pnl: float
    narrator_output: NarratorOutput


class FailedTradeData(TypedDict, total=False):
    """Failed trade record"""
    trade_id: str
    token_symbol: str
    timestamp: str
    error_reason: str
    retry_count: int


class TradeState(TypedDict, total=False):
    """Complete state of the trading system"""
    # Wallet & Portfolio
    wallet_address: str
    wallet_balance_sol: float
    wallet_balance_usdc: float
    
    # Portfolio
    current_positions: Dict[str, PositionData]
    total_pnl: float
    daily_pnl: float
    daily_loss: float
    
    # Current Trade Cycle
    market_opportunities: List[OpportunityData]
    selected_opportunity: Optional[OpportunityData]
    
    # Agent Decisions (current cycle)
    researcher_analysis: Optional[ResearcherAnalysis]
    risk_check_result: Optional[RiskCheckResult]
    supervisor_decision: Optional[SupervisorDecision]
    trade_execution_result: Optional[TradeExecutionResult]
    narrator_output: Optional[NarratorOutput]
    
    # Trade History
    completed_trades: List[TradeData]
    failed_trades: List[FailedTradeData]
    
    # Metadata
    last_run_time: Optional[str]
    cycle_count: int
    error_log: List[str]
    execution_history: List[Dict[str, Any]]


class AgentConfig(TypedDict, total=False):
    """Configuration for an individual agent"""
    name: str
    description: str
    personality: str
    max_steps: int
    temperature: float
    llm_provider: str
    llm_model: str


class QuantAISystemConfig(TypedDict, total=False):
    """System-wide configuration"""
    network: str  # "devnet" or "mainnet"
    solana_rpc_url: str
    refresh_interval_seconds: int
    
    # Position Sizing & Risk
    max_position_size_percent: float
    min_liquidity_usd: float
    max_slippage_percent: float
    daily_loss_limit_usd: float
    max_holder_concentration_percent: float
    min_holder_count: int
    
    # Optional Features
    enable_twitter: bool
    enable_voice: bool
    dry_run_mode: bool
    
    # Agent Configurations
    researcher_config: AgentConfig
    risk_manager_config: AgentConfig
    trader_config: AgentConfig
    narrator_config: AgentConfig
    supervisor_config: AgentConfig
