"""
Multi-agent orchestrator for Quant AI trading system.
Coordinates the 5 agents to debate and execute trades.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json

from quantai_project.config import QuantAIConfig
from quantai_project.state_manager import StateManager
from quantai_project.agents.researcher import ResearcherAgent
from quantai_project.agents.risk_manager import RiskManagerAgent
from quantai_project.agents.trader import TraderAgent
from quantai_project.agents.narrator import NarratorAgent
from quantai_project.agents.supervisor import SupervisorAgent


class QuantAIOrchestrator:
    """
    Main orchestrator for Quant AI trading system.
    Coordinates all 5 agents in a trading cycle.
    """
    
    def __init__(self, config: QuantAIConfig, wallet_address: str = "demo_wallet"):
        """Initialize orchestrator with config"""
        self.config = config
        self.state = StateManager(wallet_address)
        
        # Initialize all agents
        self.researcher = ResearcherAgent()
        self.risk_manager = RiskManagerAgent()
        self.trader = TraderAgent()
        self.narrator = NarratorAgent()
        self.supervisor = SupervisorAgent()
        
        self.agents = {
            "researcher": self.researcher,
            "risk_manager": self.risk_manager,
            "trader": self.trader,
            "narrator": self.narrator,
            "supervisor": self.supervisor,
        }
        
        self.cycle_number = 0
        self.is_running = False
    
    async def run_single_cycle(self) -> Dict[str, Any]:
        """
        Run a single trading cycle with all 5 agents
        
        Workflow:
        1. Researcher finds alpha opportunities
        2. For each opportunity:
           a. Risk Manager vetos or approves
           b. Supervisor gives final GO/NO-GO
           c. If GO: Trader executes
           d. Narrator announces with memes
        
        Returns:
            Cycle results with all decisions
        """
        self.cycle_number += 1
        print(f"\n{'='*70}")
        print(f"🔄 QUANT AI CYCLE #{self.cycle_number}")
        print(f"{'='*70}")
        print(f"Time: {datetime.utcnow().isoformat()}\n")
        
        self.state.increment_cycle()
        results = {
            "cycle": self.cycle_number,
            "timestamp": datetime.utcnow().isoformat(),
            "stages": {}
        }
        
        # Stage 1: Researcher finds opportunities
        print("📊 Stage 1: RESEARCHER - Hunting Alpha")
        print("-" * 70)
        researcher_result = await self._run_researcher_stage()
        results["stages"]["researcher"] = researcher_result
        print(f"✓ Found {len(researcher_result.get('opportunities', []))} opportunities\n")
        
        # Stage 2-5: Process each opportunity
        opportunities = researcher_result.get("opportunities", [])
        if not opportunities:
            print("⚠️  No opportunities found. Skipping to next cycle.\n")
            return results
        
        # Take top opportunity for demo
        top_opp = opportunities[0] if opportunities else None
        if not top_opp:
            return results
        
        print(f"🎯 Processing: {top_opp.get('token_symbol', 'UNKNOWN')}\n")
        
        # Stage 2: Risk Manager vetos or approves
        print("⚠️  Stage 2: RISK MANAGER - Risk Assessment")
        print("-" * 70)
        risk_result = await self._run_risk_manager_stage(top_opp)
        results["stages"]["risk_manager"] = risk_result
        
        if not risk_result.get("approved"):
            print(f"❌ VETO: {risk_result.get('reason', 'Safety check failed')}\n")
            return results
        
        print("✓ Risk check PASSED\n")
        
        # Stage 3: Supervisor gives final approval
        print("👔 Stage 3: SUPERVISOR - Executive Decision")
        print("-" * 70)
        supervisor_result = await self._run_supervisor_stage(top_opp, risk_result)
        results["stages"]["supervisor"] = supervisor_result
        
        if not supervisor_result.get("approved"):
            print(f"🛑 NO-GO: {supervisor_result.get('reason', 'Executive decision')}\n")
            return results
        
        print("✓ Executive approval: GO\n")
        
        # Stage 4: Trader executes
        print("🎬 Stage 4: TRADER - Executing Swap")
        print("-" * 70)
        trader_result = await self._run_trader_stage(top_opp)
        results["stages"]["trader"] = trader_result
        
        if trader_result.get("success"):
            print(f"✓ Trade executed: {trader_result.get('tx_hash', 'N/A')}\n")
        else:
            print(f"❌ Trade failed: {trader_result.get('error', 'Unknown error')}\n")
        
        # Stage 5: Narrator announces
        print("🎤 Stage 5: NARRATOR - Trade Announcement")
        print("-" * 70)
        narrator_result = await self._run_narrator_stage(top_opp, trader_result)
        results["stages"]["narrator"] = narrator_result
        print(f"📢 {narrator_result.get('announcement', 'Trade announced!')}\n")
        
        # Summary
        print("=" * 70)
        print("📈 CYCLE SUMMARY")
        print("=" * 70)
        portfolio = self.state.get_portfolio_summary()
        print(f"Portfolio Value: ${portfolio.get('total_portfolio_value', 0):,.2f}")
        print(f"Total P&L: ${portfolio.get('total_pnl', 0):+,.2f}")
        print(f"Daily P&L: ${portfolio.get('daily_pnl', 0):+,.2f}")
        print(f"Win Rate: {portfolio.get('win_rate', 0):.0f}%\n")
        
        return results
    
    async def _run_researcher_stage(self) -> Dict[str, Any]:
        """Run researcher analysis"""
        try:
            result = await self.researcher.find_opportunities("normal")
            
            # Mock response for demo
            opportunities = [
                {
                    "token_mint": "addr1",
                    "token_symbol": "WOOF",
                    "alpha_score": 72.0,
                    "reasoning": "Bullish momentum + new partnerships",
                    "price": 0.0042,
                    "volume": 250_000,
                    "market_cap": 5_000_000,
                    "timestamp": datetime.utcnow().isoformat()
                },
                {
                    "token_mint": "addr2",
                    "token_symbol": "BONK",
                    "alpha_score": 65.0,
                    "reasoning": "Established memecoin with sustained volume",
                    "price": 0.00003,
                    "volume": 500_000,
                    "market_cap": 15_000_000,
                    "timestamp": datetime.utcnow().isoformat()
                }
            ]
            
            self.state.set_researcher_analysis({"opportunities": opportunities})
            return {
                "status": "success",
                "opportunities": opportunities,
                "analysis": result
            }
        except Exception as e:
            self.state.add_error(f"Researcher error: {str(e)}")
            return {"status": "error", "error": str(e), "opportunities": []}
    
    async def _run_risk_manager_stage(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Run risk manager assessment"""
        try:
            token_symbol = opportunity.get("token_symbol", "UNKNOWN")
            
            result = await self.risk_manager.assess_trade(token_symbol, 100)
            
            # Mock response for demo
            approved = True
            rug_score = 15  # Low risk
            reason = "Liquidity and holder distribution look healthy"
            
            if rug_score > 70:
                approved = False
                reason = "Rug score too high - potential rugpull risk"
            
            risk_check = {
                "token": token_symbol,
                "approved": approved,
                "rug_score": rug_score,
                "reason": reason,
                "liquidity": "✅ $125K",
                "holders": "✅ 1,250",
                "concentration": "✅ 8.5%"
            }
            
            self.state.set_risk_check(risk_check)
            return risk_check
        except Exception as e:
            self.state.add_error(f"Risk Manager error: {str(e)}")
            return {"status": "error", "error": str(e), "approved": False}
    
    async def _run_supervisor_stage(
        self,
        opportunity: Dict[str, Any],
        risk_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run supervisor final decision"""
        try:
            token_symbol = opportunity.get("token_symbol", "UNKNOWN")
            alpha_score = opportunity.get("alpha_score", 0)
            
            portfolio = self.state.get_portfolio_summary()
            
            result = await self.supervisor.make_decision(
                token_symbol=token_symbol,
                alpha_score=alpha_score,
                risk_recommendation="PASS" if risk_result.get("approved") else "VETO",
                portfolio_value=portfolio.get("total_portfolio_value", 1000),
                daily_loss=portfolio.get("daily_loss", 0),
                daily_loss_limit=self.config.daily_loss_limit_usd
            )
            
            # Mock response for demo
            approved = risk_result.get("approved", False)
            reason = "Alpha score strong, risk manager approved, daily loss limits intact"
            
            decision = {
                "token": token_symbol,
                "approved": approved,
                "reason": reason,
                "alpha_score": alpha_score,
                "decision": "GO" if approved else "NO-GO",
            }
            
            self.state.set_supervisor_decision(decision)
            return decision
        except Exception as e:
            self.state.add_error(f"Supervisor error: {str(e)}")
            return {"status": "error", "error": str(e), "approved": False}
    
    async def _run_trader_stage(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Run trader execution"""
        try:
            token_symbol = opportunity.get("token_symbol", "UNKNOWN")
            
            # Simulate trade execution
            result = await self.trader.execute_trade(
                input_token="USDC",
                output_token=token_symbol,
                amount=100,
                slippage=1.0
            )
            
            # Mock successful trade
            execution = {
                "success": True,
                "tx_hash": f"5{self._generate_tx_hash()}",
                "input": "USDC",
                "output": token_symbol,
                "amount": 100,
                "error": None
            }
            
            self.state.set_trade_execution(execution)
            return execution
        except Exception as e:
            self.state.add_error(f"Trader error: {str(e)}")
            return {"success": False, "error": str(e), "tx_hash": None}
    
    async def _run_narrator_stage(
        self,
        opportunity: Dict[str, Any],
        trader_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run narrator announcement"""
        try:
            token_symbol = opportunity.get("token_symbol", "UNKNOWN")
            alpha_score = opportunity.get("alpha_score", 0)
            tx_hash = trader_result.get("tx_hash") if trader_result.get("success") else None
            
            result = await self.narrator.announce_trade(
                input_token="USDC",
                output_token=token_symbol,
                amount=100,
                alpha_score=alpha_score,
                transaction_hash=tx_hash
            )
            
            # Mock announcement
            announcement = {
                "token": token_symbol,
                "tweet": f"Just aped ${{token_symbol}} 🚀🚀🚀 Alpha score: {alpha_score:.0f}/100. Let's go ser! 💎🙌",
                "voice": f"Yo, just aped {token_symbol}. Alpha score is {alpha_score:.0f} out of 100. Let's go to the moon, ser!",
                "announcement": f"🎤 Just aped ${{{token_symbol}}} with confidence!",
                "tx": tx_hash or "(simulated)"
            }
            
            self.state.set_narrator_output(announcement)
            return announcement
        except Exception as e:
            self.state.add_error(f"Narrator error: {str(e)}")
            return {"status": "error", "error": str(e), "announcement": ""}
    
    async def run_continuous(self, cycles: int = 3, interval_seconds: int = 5):
        """
        Run trading bot continuously
        
        Args:
            cycles: Number of cycles to run
            interval_seconds: Seconds between cycles
        """
        self.is_running = True
        print(f"\n{'='*70}")
        print(f"🚀 QUANT AI STARTING")
        print(f"{'='*70}")
        print(f"Network: {self.config.network}")
        print(f"Cycles: {cycles}")
        print(f"Interval: {interval_seconds}s")
        print(f"Dry Run: {self.config.dry_run_mode}")
        print(f"{'='*70}\n")
        
        try:
            for i in range(cycles):
                if not self.is_running:
                    break
                
                await self.run_single_cycle()
                
                if i < cycles - 1:
                    print(f"\n⏳ Next cycle in {interval_seconds} seconds...")
                    await asyncio.sleep(interval_seconds)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down...")
        finally:
            self.is_running = False
            print("\n" + "=" * 70)
            print("✓ Quant AI Session Complete")
            print("=" * 70)
            self._print_final_summary()
    
    def stop(self):
        """Stop the bot"""
        self.is_running = False
    
    def _generate_tx_hash(self) -> str:
        """Generate mock transaction hash"""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=60))
    
    def _print_final_summary(self):
        """Print final session summary"""
        portfolio = self.state.get_portfolio_summary()
        
        print("\n📊 Final Portfolio Summary")
        print(f"  Total Value: ${portfolio.get('total_portfolio_value', 0):,.2f}")
        print(f"  Total P&L: ${portfolio.get('total_pnl', 0):+,.2f}")
        print(f"  Daily P&L: ${portfolio.get('daily_pnl', 0):+,.2f}")
        print(f"  Active Positions: {portfolio.get('position_count', 0)}")
        print(f"  Win Rate: {portfolio.get('win_rate', 0):.0f}%")
        print(f"\n  Cycles Completed: {self.state.state.get('cycle_count', 0)}")
        print(f"  Trades Executed: {len(self.state.state.get('completed_trades', []))}")
        print(f"  Failed Trades: {len(self.state.state.get('failed_trades', []))}")
