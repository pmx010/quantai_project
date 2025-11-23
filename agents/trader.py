"""
Trader Agent - Executes swaps via Jupiter.
"""

from spoon_ai.tools import ToolManager
from spoon_ai.chat import ChatBot
from pydantic import Field
from typing import Optional, Dict, Any

from quantai_project.agents import QuantAIBaseAgent
from quantai_project.tools import get_all_tools


class TraderAgent(QuantAIBaseAgent):
    """
    Trader Agent - Execution Specialist
    Executes the actual swap using Jupiter best route
    """
    
    name: str = "Trader"
    description: str = "Execution specialist - sends the swaps"
    personality: str = "Sending it"
    agent_role: str = "trader"
    
    system_prompt: str = """
    You are the Trader in a Quant AI trading system. Your job is to execute trades.
    
    Your responsibilities:
    1. Execute swaps via Jupiter Aggregator
    2. Find the best route for token swaps
    3. Respect slippage limits (max 5%)
    4. Respect position sizing (max 1% of wallet)
    5. Handle transaction errors gracefully
    6. Confirm execution with transaction hash
    
    Always use the trade_executor tool to execute swaps.
    Be precise about amounts and slippage.
    
    Remember: Your personality is "Sending it" - no hesitation, but be careful!
    """
    
    next_step_prompt: str = (
        "Execute the swap using the trade_executor tool. "
        "Confirm the transaction and get the hash."
    )
    
    max_steps: int = 5
    temperature: float = 0.1  # Very conservative for execution
    
    available_tools: ToolManager = Field(
        default_factory=lambda: ToolManager(get_all_tools())
    )
    
    async def execute_trade(
        self,
        input_token: str,
        output_token: str,
        amount: float,
        slippage: float = 1.0
    ) -> Dict[str, Any]:
        """
        Execute a token swap
        
        Args:
            input_token: Token to sell (e.g., 'USDC')
            output_token: Token to buy (e.g., 'WOOF')
            amount: Amount to trade
            slippage: Max slippage % (default 1%)
        
        Returns:
            Execution result with transaction hash
        """
        prompt = f"""
        Execute a swap:
        - Sell {amount} {input_token}
        - Buy {output_token}
        - Max slippage: {slippage}%
        
        Use the trade_executor tool to:
        1. Find the best route via Jupiter
        2. Execute the swap
        3. Return the transaction hash
        
        Confirm the swap was successful.
        """
        
        result = await self.run(prompt)
        return {
            "input": input_token,
            "output": output_token,
            "amount": amount,
            "slippage": slippage,
            "execution": result,
            "agent": "Trader"
        }
    
    async def simulate_trade(
        self,
        input_token: str,
        output_token: str,
        amount: float
    ) -> Dict[str, Any]:
        """
        Simulate a trade without executing
        
        Args:
            input_token: Token to sell
            output_token: Token to buy
            amount: Amount to trade
        
        Returns:
            Simulated trade result
        """
        prompt = f"""
        Simulate a swap (dry run):
        - Sell {amount} {input_token}
        - Buy {output_token}
        
        Use the trade_executor tool to simulate the swap.
        Show expected output amount and slippage.
        DO NOT execute the actual trade.
        """
        
        result = await self.run(prompt)
        return {
            "input": input_token,
            "output": output_token,
            "amount": amount,
            "simulation": result,
            "agent": "Trader"
        }
    
    async def check_position_size(self, wallet_balance: float, trade_amount: float) -> Dict[str, Any]:
        """
        Verify trade size respects risk limits
        
        Args:
            wallet_balance: Current wallet balance in USD
            trade_amount: Proposed trade amount in USD
        
        Returns:
            Approval or request to reduce size
        """
        max_position_percent = 1.0  # 1% max
        max_position_usd = wallet_balance * (max_position_percent / 100)
        
        return {
            "wallet_balance": wallet_balance,
            "proposed_trade": trade_amount,
            "max_position": max_position_usd,
            "max_position_percent": max_position_percent,
            "approved": trade_amount <= max_position_usd,
            "recommended_size": min(trade_amount, max_position_usd),
            "agent": "Trader"
        }
