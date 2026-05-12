"""供应商Agent - 产能与约束检查"""
from ..models import Proposal, AgentEvaluation, AgentRole


class SupplierAgent:
    """供应商关系与产能管理Agent"""
    
    def __init__(self):
        self.name = AgentRole.SUPPLIER
        
        # 供应商产能锁定情况（实际应接SRM系统）
        self._capacity_locks = {
            "巴生港-供应商D": {"locked": 0.3, "min_order": 100},
            "新加坡港-供应商G": {"locked": 0.15, "min_order": 200},
            "深圳工厂-供应商E": {"locked": 0.1, "min_order": 50},
            "曼谷工厂-供应商H": {"locked": 0.2, "min_order": 80},
            "温哥华港-供应商F": {"locked": 0.5, "min_order": 150},
            "休斯顿港-供应商I": {"locked": 0.25, "min_order": 120}
        }
        
        self.lock_threshold = 0.4  # 产能锁定阈值
    
    def check_constraints(self, proposal: Proposal) -> AgentEvaluation:
        """检查目标供应商的产能约束"""
        constraints = self._capacity_locks.get(
            proposal.supplier_to, 
            {"locked": 0.0, "min_order": 0}
        )
        
        locked_pct = constraints["locked"]
        passed = locked_pct < self.lock_threshold
        
        if passed:
            reasoning = f"供应商产能可用：锁定{locked_pct:.0%}，低于阈值{self.lock_threshold:.0%}"
            suggestions = []
        else:
            reasoning = f"供应商产能不足：已锁定{locked_pct:.0%}，超过阈值{self.lock_threshold:.0%}"
            suggestions = [
                f"建议使用备选供应商",
                f"联系供应商确认是否可释放部分产能",
                f"考虑分单至多个供应商"
            ]
        
        return AgentEvaluation(
            agent_role=self.name,
            score=locked_pct,
            passed=passed,
            reasoning=reasoning,
            suggestions=suggestions
        )
