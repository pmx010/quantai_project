"""
Supervisor Agent - Final decision maker and CEO of the bot.
"""

from spoon_ai.tools import ToolManager
from spoon_ai.chat import ChatBot
from pydantic import Field
from typing import Optional, Dict, Any

from quantai_project.agents import QuantAIBaseAgent
from quantai_project.tools import get_all_tools


class SupervisorAgent(QuantAIBaseAgent):
    """
    Supervisor Agent - Executive Decision Maker
    Final boss — asks "should we actually do this?" and gives GO/NO-GO
    """
    
    name: str = "Supervisor"
    description: str = "Final decision maker - CEO of the bot"
    personality: str = "The CEO"
    agent_role: str = "supervisor"
    
    system_prompt: str = """
    You are the Supervisor (CEO) in a Quant AI trading system. Your job is FINAL APPROVAL.
    
    Your responsibilities:
    1. Review all agent recommendations (Researcher, Risk Manager)
    2. Consider portfolio state and risk limits
    3. Check daily loss limits
    4. Evaluate portfolio diversity
    5. Make final GO or NO-GO decision
    6. Provide executive rationale
    
    Decision logic:
    - GO if: Risk Manager says PASS, daily loss < limit, reasonable position
    - NO-GO if: Risk Manager says VETO, daily loss too high, portfolio too concentrated
    - NO-GO if: Beta risk too high or position sizing violates limits
    
    Your role is to prevent bad trades while allowing good ones.
    You have VETO power and MUST use it to protect capital.
    
    Remember: Your personality is "The CEO" - professional, decisive, and risk-aware!
    """
    
    next_step_prompt: str = (
        "After reviewing all factors, make a final GO or NO-GO decision. "
        "Provide executive reasoning."
    )
    
    max_steps: int = 5
    temperature: float = 0.5  # Balanced
    
    available_tools: ToolManager = Field(
        default_factory=lambda: ToolManager(get_all_tools())
    )
    
    async def make_decision(
        self,
        token_symbol: str,
        alpha_score: float,
        risk_recommendation: str,
        portfolio_value: float,
        daily_loss: float,
        daily_loss_limit: float
    ) -> Dict[str, Any]:
        """
        Make final GO/NO-GO decision for a trade
        
        Args:
            token_symbol: Token to trade
            alpha_score: Alpha score from Researcher (0-100)
            risk_recommendation: PASS or VETO from Risk Manager
            portfolio_value: Current portfolio value
            daily_loss: Current daily loss
            daily_loss_limit: Daily loss limit
        
        Returns:
            GO or NO-GO decision with reasoning
        """
        daily_loss_remaining = daily_loss_limit - daily_loss
        
        prompt = f"""
        Executive Decision Required for: ${token_symbol}
        
        Summary:
        - Alpha Score: {alpha_score}/100
        - Risk Manager: {risk_recommendation}
        - Portfolio Value: ${portfolio_value:,.2f}
        - Daily P&L: {daily_loss:+,.2f} (limit: ${daily_loss_limit})
        - Loss Budget Remaining: ${daily_loss_remaining:,.2f}
        
        Decision criteria:
        1. Risk Manager recommendation must be PASS (otherwise veto)
        2. Daily loss must not exceed limit
        3. Alpha score must be > 50 to be worth the risk
        4. Position must not exceed 1% of portfolio
        
        Make a GO or NO-GO decision as the CEO.
        Provide clear executive reasoning.
        """
        
        result = await self.run(prompt)
        return {
            "token": token_symbol,
            "alpha_score": alpha_score,
            "risk_recommendation": risk_recommendation,
            "portfolio_value": portfolio_value,
            "daily_loss": daily_loss,
            "daily_loss_limit": daily_loss_limit,
            "decision": result,
            "agent": "Supervisor"
        }
    
    async def review_portfolio(
        self,
        total_value: float,
        position_count: int,
        largest_position_percent: float,
        daily_pnl: float
    ) -> Dict[str, Any]:
        """
        Review overall portfolio health
        
        Args:
            total_value: Total portfolio value
            position_count: Number of active positions
            largest_position_percent: Size of largest position as % of portfolio
            daily_pnl: Daily P&L
        
        Returns:
            Portfolio health assessment and recommendations
        """
        prompt = f"""
        Portfolio Health Review:
        - Total Value: ${total_value:,.2f}
        - Active Positions: {position_count}
        - Largest Position: {largest_position_percent:.1f}% of portfolio
        - Daily P&L: ${daily_pnl:+,.2f}
        
        As the CEO, assess:
        1. Is portfolio properly diversified? (no position > 10% ideally)
        2. Are we taking appropriate risk?
        3. Should we scale up, scale down, or hold?
        4. Any positions we should close?
        
        Provide strategic recommendations.
        """
        
        result = await self.run(prompt)
        return {
            "total_value": total_value,
            "position_count": position_count,
            "largest_position": largest_position_percent,
            "daily_pnl": daily_pnl,
            "assessment": result,
            "agent": "Supervisor"
        }
    
    async def should_keep_trading(
        self,
        daily_loss: float,
        daily_loss_limit: float,
        win_rate: float,
        consecutive_losses: int
    ) -> Dict[str, Any]:
        """
        Determine if we should keep trading or take a break
        
        Args:
            daily_loss: Current daily loss
            daily_loss_limit: Daily loss limit
            win_rate: Current win rate %
            consecutive_losses: Number of consecutive losses
        
        Returns:
            KEEP_TRADING or TAKE_A_BREAK recommendation
        """
        loss_percent = (daily_loss / daily_loss_limit) * 100 if daily_loss_limit > 0 else 0
        
        prompt = f"""
        Trading Decision:
        - Daily Loss: ${daily_loss:,.2f} / ${daily_loss_limit:,.2f} ({loss_percent:.0f}%)
        - Win Rate: {win_rate:.0f}%
        - Consecutive Losses: {consecutive_losses}
        
        Should we KEEP_TRADING or TAKE_A_BREAK?
        
        Consider:
        1. Are we burning through daily loss limit?
        2. Is win rate too low (< 40%)?
        3. Are we on a losing streak (> 5 losses)?
        4. Should we reset and come back tomorrow?
        
        Provide CEO recommendation.
        """
        
        result = await self.run(prompt)
        return {
            "daily_loss": daily_loss,
            "daily_loss_limit": daily_loss_limit,
            "loss_percent": loss_percent,
            "win_rate": win_rate,
            "consecutive_losses": consecutive_losses,
            "recommendation": result,
            "agent": "Supervisor"
        }
