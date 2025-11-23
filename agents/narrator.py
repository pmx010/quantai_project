"""
Narrator Agent - Announces trades with memes and personality.
"""

from spoon_ai.tools import ToolManager
from spoon_ai.chat import ChatBot
from pydantic import Field
from typing import Optional, Dict, Any

from quantai_project.agents import QuantAIBaseAgent
from quantai_project.tools import get_all_tools


class NarratorAgent(QuantAIBaseAgent):
    """
    Narrator Agent - Communications Specialist
    Explains every decision with memes + optional voice narration
    """
    
    name: str = "Narrator"
    description: str = "Communications - announces trades with memes"
    personality: str = "Professional shitposter"
    agent_role: str = "narrator"
    
    system_prompt: str = """
    You are the Narrator in a Quant AI trading system. Your job is to communicate.
    
    Your responsibilities:
    1. Create meme-filled trade announcements
    2. Explain trades in crypto/defi lingo
    3. Generate funny but informative tweets
    4. Describe trades for voice synthesis
    5. React to wins and losses with personality
    6. Use crypto slang and memes appropriately
    
    Style guidelines:
    - Use 🚀 🌙 💎 🙌 for bull trades
    - Use 🛑 📉 ⚠️ 🔴 for warnings/losses
    - Keep tweets under 280 characters (for real posts)
    - Be funny but not offensive
    - Include $SYMBOL tags
    - End trades with "ser" or other crypto slang
    
    Remember: Your personality is "Professional shitposter" - funny, informative, and on-brand!
    """
    
    next_step_prompt: str = (
        "Create a funny but informative trade announcement. "
        "Include both a tweet text and voice script."
    )
    
    max_steps: int = 3
    temperature: float = 0.9  # Creative!
    
    available_tools: ToolManager = Field(
        default_factory=lambda: ToolManager(get_all_tools())
    )
    
    async def announce_trade(
        self,
        input_token: str,
        output_token: str,
        amount: float,
        alpha_score: float,
        transaction_hash: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Announce a trade with memes and personality
        
        Args:
            input_token: Token sold
            output_token: Token bought
            amount: Amount traded
            alpha_score: Alpha score (0-100)
            transaction_hash: Optional tx hash for real trades
        
        Returns:
            Meme-filled announcement with tweet and voice script
        """
        tx_link = f"https://solscan.io/tx/{transaction_hash}" if transaction_hash else "(simulated)"
        
        prompt = f"""
        Create a hilarious trade announcement for this swap:
        - Sold: {amount} {input_token}
        - Bought: {output_token}
        - Alpha Score: {alpha_score}/100
        - TX: {tx_link}
        
        Generate:
        1. A funny tweet (under 280 chars) with emojis
        2. A voice script (2-3 sentences)
        3. Description of the meme energy (e.g., "bullish hype", "cautious optimism")
        
        Use crypto slang, end with "ser" or similar.
        Make it entertaining while still informative.
        """
        
        result = await self.run(prompt)
        return {
            "input": input_token,
            "output": output_token,
            "announcement": result,
            "agent": "Narrator"
        }
    
    async def react_to_result(
        self,
        token_symbol: str,
        pnl_percent: float,
        pnl_amount: float
    ) -> Dict[str, Any]:
        """
        React to trade result (win or loss)
        
        Args:
            token_symbol: Token traded
            pnl_percent: Profit/loss percentage
            pnl_amount: Profit/loss in USD
        
        Returns:
            Reaction with appropriate sentiment
        """
        sentiment = "WINNING" if pnl_percent > 0 else "REKT" if pnl_percent < -10 else "BLEEDING"
        
        prompt = f"""
        React to this trade result:
        - Token: ${token_symbol}
        - P&L: {pnl_percent:+.1f}% (${pnl_amount:+,.2f})
        - Sentiment: {sentiment}
        
        Create:
        1. A funny but honest reaction tweet
        2. Whether we're celebrating or coping
        3. What we do next (HODL, exit, average down?)
        
        Keep it real but entertaining.
        """
        
        result = await self.run(prompt)
        return {
            "token": token_symbol,
            "pnl_percent": pnl_percent,
            "pnl_amount": pnl_amount,
            "reaction": result,
            "agent": "Narrator"
        }
    
    async def summarize_portfolio(
        self,
        total_value: float,
        daily_pnl: float,
        win_rate: float,
        position_count: int
    ) -> Dict[str, Any]:
        """
        Summarize portfolio status with personality
        
        Args:
            total_value: Total portfolio value
            daily_pnl: Daily P&L
            win_rate: Win rate %
            position_count: Number of active positions
        
        Returns:
            Portfolio summary announcement
        """
        prompt = f"""
        Summarize our portfolio status with personality:
        - Portfolio Value: ${total_value:,.2f}
        - Daily P&L: ${daily_pnl:+,.2f}
        - Win Rate: {win_rate:.0f}%
        - Active Positions: {position_count}
        
        Create:
        1. A snappy portfolio update tweet
        2. Overall vibe/sentiment of the day
        3. What we're watching next
        
        Make it hype if we're winning, hopeful if we're down.
        """
        
        result = await self.run(prompt)
        return {
            "total_value": total_value,
            "daily_pnl": daily_pnl,
            "win_rate": win_rate,
            "position_count": position_count,
            "summary": result,
            "agent": "Narrator"
        }
