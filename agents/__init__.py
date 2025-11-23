"""
Base agent for Quant AI system.
All specialized agents inherit from this class.
"""

from spoon_ai.agents.toolcall import ToolCallAgent
from spoon_ai.tools import ToolManager
from spoon_ai.chat import ChatBot
from pydantic import Field
from typing import List, Dict, Any, Optional
from quantai_project.tools import get_all_tools


class QuantAIBaseAgent(ToolCallAgent):
    """Base class for all Quant AI agents"""
    
    name: str = "base_agent"
    description: str = "Base agent for Quant AI"
    personality: str = ""
    agent_role: str = ""
    
    system_prompt: str = """
    You are a specialized trading agent in the Quant AI system.
    Use available tools to gather information and make decisions.
    Be concise and actionable in your responses.
    """
    
    next_step_prompt: str = (
        "Based on the previous result, decide what to do next. "
        "If you have enough information to make a decision, state it clearly."
    )
    
    max_steps: int = 5
    
    available_tools: ToolManager = Field(
        default_factory=lambda: ToolManager(get_all_tools())
    )
    
    def __init__(self, llm: Optional[ChatBot] = None, **kwargs):
        """Initialize agent with LLM"""
        if llm is None:
            llm = ChatBot(llm_provider="openai", model_name="gpt-4-mini")
        super().__init__(llm=llm, **kwargs)
    
    async def analyze(self, prompt: str) -> str:
        """Run analysis with custom prompt"""
        return await self.run(prompt)
    
    def get_personality_hint(self) -> str:
        """Get personality for narrator context"""
        return f"[{self.name} speaking with personality: {self.personality}]"
