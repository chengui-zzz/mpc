"""规划Agent - 应急方案生成"""
from ..models import Proposal, RiskEvent, AgentRole


class PlanningAgent:
    """供应链规划专家Agent"""
    
    def __init__(self):
        self.name = AgentRole.PLANNING
        
        # 备选供应商映射表（实际应接ERP系统）
        self._alt_suppliers = {
            "马尼拉港-供应商A": ["巴生港-供应商D", "新加坡港-供应商G"],
            "河内工厂-供应商B": ["深圳工厂-供应商E", "曼谷工厂-供应商H"],
            "洛杉矶港-供应商C": ["温哥华港-供应商F", "休斯顿港-供应商I"]
        }
    
    def propose(self, event: RiskEvent) -> Proposal:
        """基于风险事件，生成应急方案"""
        alts = self._alt_suppliers.get(
            event.affected_supplier, 
            ["备用供应商-X"]
        )
        
        primary_alt = alts[0]
        cost_increase = 15.0 if event.severity.value == "red" else 10.0
        
        return Proposal(
            action="订单紧急转移",
            supplier_from=event.affected_supplier,
            supplier_to=primary_alt,
            cost_increase_pct=cost_increase,
            lead_time_days=5 if event.severity.value == "red" else 3,
            description=f"因{event.event_type}事件，将{event.affected_supplier}订单转移至{primary_alt}",
            alternatives=alts[1:]  # 备选方案
        )
    
    def adjust(self, original: Proposal, feedback: str) -> Proposal:
        """根据其他Agent反馈调整方案"""
        # 增加缓冲成本和时间
        adjusted = Proposal(
            action=original.action,
            supplier_from=original.supplier_from,
            supplier_to=original.alternatives[0] if original.alternatives else original.supplier_to,
            cost_increase_pct=original.cost_increase_pct + 5.0,
            lead_time_days=original.lead_time_days + 2,
            description=f"{original.description}（调整后方案：{feedback}）",
            alternatives=original.alternatives[1:]
        )
        return adjusted
