"""库存Agent - 长程库存回溯模拟"""
import random
from ..models import Proposal, AgentEvaluation, AgentRole


class InventoryAgent:
    """库存水位评估Agent"""
    
    def __init__(self):
        self.name = AgentRole.INVENTORY
        self.history_lookback_days = 60
    
    def evaluate(self, proposal: Proposal) -> AgentEvaluation:
        """
        回溯60天数据，模拟库存消耗
        检测是否存在库存缺口风险
        """
        # 模拟多维度库存计算
        demand_volatility = random.uniform(0.1, 0.5)
        safety_stock_level = random.uniform(0.3, 0.8)
        projected_gap = demand_volatility * (1 - safety_stock_level)
        
        score = projected_gap
        passed = score < 0.7
        
        if passed:
            reasoning = f"库存安全：回溯{self.history_lookback_days}天，安全库存充足"
            suggestions = []
        else:
            reasoning = f"库存缺口预警：60天后备件库存出现{score:.0%}缺口"
            suggestions = [
                "建议启用安全库存缓冲",
                "考虑分批转移订单以分散风险",
                "优先消耗已有库存，延缓转移"
            ]
        
        return AgentEvaluation(
            agent_role=self.name,
            score=score,
            passed=passed,
            reasoning=reasoning,
            suggestions=suggestions
        )
