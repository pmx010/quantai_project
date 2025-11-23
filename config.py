"""
Configuration for Quant AI trading system.
"""

import os
from typing import Dict, Any
from quantai_project.types import QuantAISystemConfig, AgentConfig


class QuantAIConfig:
    """System configuration management"""
    
    def __init__(self):
        """Initialize config from environment variables and defaults"""
        self.network = os.getenv("SOLANA_NETWORK", "devnet")
        self.solana_rpc_url = os.getenv(
            "SOLANA_RPC_URL",
            "https://api.devnet.solana.com" if self.network == "devnet" else "https://api.mainnet.solana.com"
        )
        self.wallet_address = os.getenv("WALLET_ADDRESS", "")
        self.wallet_secret = os.getenv("WALLET_SECRET_KEY", "")
        
        # Trading parameters
        self.max_position_size_percent = float(os.getenv("MAX_POSITION_SIZE_PERCENT", "1.0"))
        self.min_liquidity_usd = float(os.getenv("MIN_LIQUIDITY_USD", "10000"))
        self.max_slippage_percent = float(os.getenv("MAX_SLIPPAGE_PERCENT", "5.0"))
        self.daily_loss_limit_usd = float(os.getenv("DAILY_LOSS_LIMIT_USD", "100"))
        self.max_holder_concentration_percent = float(os.getenv("MAX_HOLDER_CONCENTRATION_PERCENT", "30.0"))
        self.min_holder_count = int(os.getenv("MIN_HOLDER_COUNT", "50"))
        
        # Execution
        self.refresh_interval_seconds = int(os.getenv("REFRESH_INTERVAL_SECONDS", "180"))  # 3 minutes
        
        # Optional features
        self.enable_twitter = os.getenv("ENABLE_TWITTER", "false").lower() == "true"
        self.enable_voice = os.getenv("ENABLE_VOICE", "false").lower() == "true"
        self.dry_run_mode = os.getenv("DRY_RUN_MODE", "true").lower() == "true"  # Safe by default
        
        # LLM Defaults
        self.llm_provider = os.getenv("LLM_PROVIDER", "openai")
        self.llm_model = os.getenv("LLM_MODEL", "gpt-4-mini")
        
        # API Keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.twitter_api_key = os.getenv("TWITTER_API_KEY", "")
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY", "")
        self.jupiter_api_url = os.getenv("JUPITER_API_URL", "https://price.jup.ag")
    
    def get_agent_config(self, agent_name: str) -> AgentConfig:
        """Get configuration for a specific agent"""
        configs: Dict[str, AgentConfig] = {
            "researcher": {
                "name": "Researcher",
                "description": "Alpha hunter - scans tokens for opportunities",
                "personality": "I smell 100x",
                "max_steps": 5,
                "temperature": 0.7,
                "llm_provider": self.llm_provider,
                "llm_model": self.llm_model,
            },
            "risk_manager": {
                "name": "Risk Manager",
                "description": "Risk analyzer - vetoes dangerous trades",
                "personality": "Paranoid dad mode",
                "max_steps": 5,
                "temperature": 0.3,  # Conservative
                "llm_provider": self.llm_provider,
                "llm_model": self.llm_model,
            },
            "trader": {
                "name": "Trader",
                "description": "Execution specialist - sends the swaps",
                "personality": "Sending it",
                "max_steps": 5,
                "temperature": 0.1,  # Very conservative for execution
                "llm_provider": self.llm_provider,
                "llm_model": self.llm_model,
            },
            "narrator": {
                "name": "Narrator",
                "description": "Communications - announces trades with memes",
                "personality": "Professional shitposter",
                "max_steps": 3,
                "temperature": 0.9,  # Creative/fun
                "llm_provider": self.llm_provider,
                "llm_model": self.llm_model,
            },
            "supervisor": {
                "name": "Supervisor",
                "description": "Final decision maker - CEO of the bot",
                "personality": "The CEO",
                "max_steps": 5,
                "temperature": 0.5,  # Balanced
                "llm_provider": self.llm_provider,
                "llm_model": self.llm_model,
            },
        }
        return configs.get(agent_name, configs["researcher"])
    
    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary"""
        return {
            "network": self.network,
            "solana_rpc_url": self.solana_rpc_url,
            "wallet_address": self.wallet_address,
            "max_position_size_percent": self.max_position_size_percent,
            "min_liquidity_usd": self.min_liquidity_usd,
            "max_slippage_percent": self.max_slippage_percent,
            "daily_loss_limit_usd": self.daily_loss_limit_usd,
            "max_holder_concentration_percent": self.max_holder_concentration_percent,
            "min_holder_count": self.min_holder_count,
            "refresh_interval_seconds": self.refresh_interval_seconds,
            "enable_twitter": self.enable_twitter,
            "enable_voice": self.enable_voice,
            "dry_run_mode": self.dry_run_mode,
            "llm_provider": self.llm_provider,
            "llm_model": self.llm_model,
        }
    
    def validate(self) -> bool:
        """Validate critical configuration"""
        if not self.wallet_address and not os.getenv("DEMO_MODE"):
            print("⚠️  Warning: WALLET_ADDRESS not set. Running in demo mode.")
        
        if self.network == "mainnet" and self.dry_run_mode:
            print("ℹ️  Mainnet selected but DRY_RUN_MODE=true. No real trades will execute.")
        
        if self.network == "mainnet" and not self.wallet_secret:
            print("❌ Error: WALLET_SECRET_KEY required for mainnet execution")
            return False
        
        return True


def load_config() -> QuantAIConfig:
    """Load configuration"""
    config = QuantAIConfig()
    config.validate()
    return config
