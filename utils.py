"""
Utility functions for Quant AI system.
"""

from datetime import datetime
from typing import Dict, Any, List


def format_usd(amount: float) -> str:
    """Format amount as USD"""
    sign = "+" if amount >= 0 else ""
    return f"{sign}${amount:,.2f}"


def format_percent(percent: float) -> str:
    """Format percentage with sign"""
    sign = "+" if percent >= 0 else ""
    return f"{sign}{percent:.2f}%"


def format_token_amount(amount: float, decimals: int = 6) -> str:
    """Format token amount with proper decimals"""
    if amount > 1_000_000:
        return f"{amount/1_000_000:.2f}M"
    elif amount > 1_000:
        return f"{amount/1_000:.2f}K"
    else:
        return f"{amount:.6f}"


def calculate_win_rate(completed_trades: List[Dict[str, Any]]) -> float:
    """Calculate win rate from completed trades"""
    if not completed_trades:
        return 0.0
    
    winning = sum(1 for t in completed_trades if t.get("pnl", 0) > 0)
    return (winning / len(completed_trades)) * 100


def format_portfolio_summary(summary: Dict[str, Any]) -> str:
    """Format portfolio summary as readable text"""
    lines = [
        "📊 Portfolio Summary",
        f"  Value: {format_usd(summary.get('total_portfolio_value', 0))}",
        f"  Total P&L: {format_usd(summary.get('total_pnl', 0))}",
        f"  Daily P&L: {format_usd(summary.get('daily_pnl', 0))}",
        f"  Win Rate: {summary.get('win_rate', 0):.0f}%",
        f"  Positions: {summary.get('position_count', 0)} active",
    ]
    return "\n".join(lines)


def get_opportunity_emoji(alpha_score: float) -> str:
    """Get emoji for alpha score"""
    if alpha_score >= 80:
        return "🚀🚀🚀"
    elif alpha_score >= 70:
        return "🚀🚀"
    elif alpha_score >= 60:
        return "🚀"
    elif alpha_score >= 50:
        return "📈"
    else:
        return "📉"


def get_sentiment_emoji(pnl_percent: float) -> str:
    """Get emoji for P&L sentiment"""
    if pnl_percent > 20:
        return "🚀"
    elif pnl_percent > 5:
        return "📈"
    elif pnl_percent > 0:
        return "✅"
    elif pnl_percent > -5:
        return "📉"
    elif pnl_percent > -20:
        return "🔴"
    else:
        return "💀"


def format_agent_decision(agent_name: str, decision: str, confidence: float = None) -> str:
    """Format agent decision for output"""
    icon = {
        "researcher": "🔍",
        "risk_manager": "⚠️ ",
        "trader": "🎬",
        "narrator": "🎤",
        "supervisor": "👔"
    }.get(agent_name.lower(), "🤖")
    
    confidence_str = f" ({confidence:.0f}% confidence)" if confidence else ""
    return f"{icon} {agent_name}: {decision}{confidence_str}"


def get_next_cycle_time(current_time: datetime, interval_seconds: int) -> datetime:
    """Calculate next cycle execution time"""
    from datetime import timedelta
    return current_time + timedelta(seconds=interval_seconds)


def format_transaction_link(tx_hash: str, network: str = "devnet") -> str:
    """Format Solscan transaction link"""
    if network == "mainnet":
        return f"https://solscan.io/tx/{tx_hash}"
    else:
        return f"https://solscan.io/tx/{tx_hash}?cluster=devnet"


def validate_token_symbol(symbol: str) -> bool:
    """Validate token symbol format"""
    return len(symbol) <= 20 and symbol.isalnum()


def validate_wallet_address(address: str) -> bool:
    """Validate Solana wallet address format (base58)"""
    import re
    # Base58 regex pattern
    base58_pattern = r'^[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{44}$'
    return bool(re.match(base58_pattern, address))


def format_error_message(error: Exception, context: str = "") -> str:
    """Format error for logging"""
    timestamp = datetime.utcnow().isoformat()
    error_type = type(error).__name__
    error_msg = str(error)
    
    if context:
        return f"[{timestamp}] {context}: {error_type}: {error_msg}"
    else:
        return f"[{timestamp}] {error_type}: {error_msg}"
