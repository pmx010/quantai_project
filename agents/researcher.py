"""
Researcher Agent - Finds alpha opportunities across Solana tokens.
"""

from spoon_ai.tools import ToolManager
from spoon_ai.chat import ChatBot
from pydantic import Field
from typing import Optional, Dict, Any

from quantai_project.agents import QuantAIBaseAgent
from quantai_project.tools import get_all_tools


class ResearcherAgent(QuantAIBaseAgent):
    """
    Researcher Agent - Alpha Hunter
    Scans top volume tokens + new launches, finds alpha opportunities
    """
    
    name: str = "Researcher"
    description: str = "Alpha hunter - scans tokens for opportunities"
    personality: str = "I smell 100x"
    agent_role: str = "researcher"
    
    system_prompt: str = """
    You are the Researcher in a Quant AI trading system. Your job is to hunt alpha.
    
    Your responsibilities:
    1. Analyze market trends and token performance
    2. Identify promising trading opportunities based on:
       - Price momentum (bullish signals)
       - Volume trends (increasing or unusual)
       - Market cap and liquidity levels
       - Holder distribution
       - Launch timing (new tokens often have alpha)
    3. Score each opportunity (0-100) based on potential upside
    4. Focus on legitimate opportunities, not pure gambling
    
    Always use the token_analyzer tool to get data on potential tokens.
    Be specific about why each opportunity has alpha potential.
    
    Remember: Your personality is "I smell 100x" - be optimistic but data-driven.
    """
    
    next_step_prompt: str = (
        "Based on the token analysis, decide if this is an alpha opportunity. "
        "If yes, provide a score (0-100). If no, move to the next token."
    )
    
    max_steps: int = 10
    
    available_tools: ToolManager = Field(
        default_factory=lambda: ToolManager(get_all_tools())
    )
    
    async def find_opportunities(self, market_condition: str = "normal") -> Dict[str, Any]:
        """
        Find trading opportunities in current market
        
        Args:
            market_condition: "bullish", "bearish", or "normal"
        
        Returns:
            Dictionary with list of opportunities and analysis
        """
        prompt = f"""
        Current market condition: {market_condition}
        
        Analyze these potential tokens for alpha opportunities:
        - $WOOF (new memecoin)
        - $BONK (established memecoin)
        - $RAY (DEX token)
        - $COPE (emerging)
        - $COPE2 (just launched)
        
        For each token, use the token_analyzer tool to get data.
        Then score each opportunity 0-100 based on alpha potential.
        Return your top 3 picks with detailed reasoning.
        """
        
        result = await self.run(prompt)
        return {
            "analysis": result,
            "timestamp": "now",
            "agent": "Researcher"
        }
    
    async def analyze_token(self, token_symbol: str) -> Dict[str, Any]:
        """Analyze a single token for alpha"""
        prompt = f"""
        Analyze ${token_symbol} for alpha opportunities.
        Use the token_analyzer tool to get market data.
        
        Provide:
        1. Current price and momentum
        2. Volume analysis
        3. Holder distribution assessment
        4. Alpha score (0-100)
        5. Risk/reward ratio
        6. Whether to pursue this opportunity
        """
        
        result = await self.run(prompt)
        return {
            "token": token_symbol,
            "analysis": result,
            "agent": "Researcher"
        }
