"""
Risk Manager Agent - Vetoes dangerous trades.
"""

from spoon_ai.tools import ToolManager
from spoon_ai.chat import ChatBot
from pydantic import Field
from typing import Optional, Dict, Any

from quantai_project.agents import QuantAIBaseAgent
from quantai_project.tools import get_all_tools


class RiskManagerAgent(QuantAIBaseAgent):
    """
    Risk Manager Agent - Risk Assessor
    Checks liquidity, holder count, rug-score — vetoes degen
    """
    
    name: str = "Risk Manager"
    description: str = "Risk analyzer - vetoes dangerous trades"
    personality: str = "Paranoid dad mode"
    agent_role: str = "risk_manager"
    
    system_prompt: str = """
    You are the Risk Manager in a Quant AI trading system. Your job is to protect capital.
    
    Your responsibilities:
    1. Assess rugpull risk for proposed trades
    2. Check critical safety metrics:
       - Liquidity (min $10K for safe trading)
       - Holder count (min 50 holders for safety)
       - Top holder concentration (max 30% safe)
       - Token age (newer = higher risk)
    3. Calculate a rugpull score (0-100, higher = riskier)
    4. Make a PASS or VETO recommendation
    5. Explain your reasoning in paranoid but clear terms
    
    Always use the liquidity_checker tool to analyze risk.
    Your job is to say NO to bad trades, even if they have alpha potential.
    
    Remember: Your personality is "Paranoid dad mode" - better safe than sorry!
    """
    
    next_step_prompt: str = (
        "Based on the liquidity check, is this token safe to trade? "
        "PASS if metrics are healthy, VETO if there's significant risk."
    )
    
    max_steps: int = 5
    temperature: float = 0.3  # Conservative
    
    available_tools: ToolManager = Field(
        default_factory=lambda: ToolManager(get_all_tools())
    )
    
    async def assess_trade(self, token_symbol: str, amount: float) -> Dict[str, Any]:
        """
        Assess risk for a proposed trade
        
        Args:
            token_symbol: Token to trade
            amount: Amount to trade
        
        Returns:
            Risk assessment with PASS/VETO recommendation
        """
        prompt = f"""
        Assess the risk of trading ${token_symbol} with ${amount}.
        
        Use the liquidity_checker tool to analyze:
        1. Liquidity levels
        2. Holder distribution
        3. Rugpull indicators
        
        Then make a decision: PASS (safe) or VETO (too risky)?
        Provide specific concerns and confidence score (0-100).
        """
        
        result = await self.run(prompt)
        return {
            "token": token_symbol,
            "amount": amount,
            "assessment": result,
            "agent": "Risk Manager"
        }
    
    async def check_liquidity(self, token_symbol: str) -> Dict[str, Any]:
        """Check liquidity metrics for a token"""
        prompt = f"""
        Check the liquidity and safety metrics for ${token_symbol}.
        
        Use the liquidity_checker tool and report:
        1. Total liquidity in USD
        2. Holder count
        3. Top holder concentration %
        4. Rugpull risk score (0-100)
        5. Overall safety assessment
        """
        
        result = await self.run(prompt)
        return {
            "token": token_symbol,
            "liquidity_check": result,
            "agent": "Risk Manager"
        }
    
    async def veto_or_approve(self, token_symbol: str, alpha_score: float) -> Dict[str, Any]:
        """
        Veto or approve a trade based on risk vs. alpha
        
        Args:
            token_symbol: Token to evaluate
            alpha_score: Alpha score from Researcher (0-100)
        
        Returns:
            VETO or PASS decision
        """
        prompt = f"""
        Token: ${token_symbol}
        Alpha Score (from Researcher): {alpha_score}/100
        
        Check the liquidity and risk metrics.
        
        Decision logic:
        - If rug_score > 70: VETO (too risky)
        - If liquidity < $10K: VETO (too thin)
        - If holder concentration > 30%: VETO (whale risk)
        - If holder count < 50: VETO (distribution risk)
        - Otherwise: PASS
        
        Make your decision and explain why.
        """
        
        result = await self.run(prompt)
        return {
            "token": token_symbol,
            "alpha_score": alpha_score,
            "decision": result,
            "agent": "Risk Manager"
        }
