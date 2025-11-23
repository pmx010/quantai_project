"""
Quant AI – Multi-Asset Autonomous Trading System

A squad of 5 specialized AI agents that hunt alpha across all Solana tokens,
debate each other, and execute real on-chain trades without asking you.

Built with SpoonOS + Solana toolkits.
"""

__version__ = "0.1.0"
__author__ = "Quant AI Team"

from quantai_project.config import QuantAIConfig
from quantai_project.state_manager import StateManager
from quantai_project.orchestrator import QuantAIOrchestrator
from quantai_project import api

__all__ = [
    "QuantAIConfig",
    "StateManager",
    "QuantAIOrchestrator",
    "api",
]
