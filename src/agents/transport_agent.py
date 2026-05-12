"""运输Agent - 多式联运路径规划"""
import random
from ..models import Proposal, AgentEvaluation, AgentRole


class TransportAgent:
    """物流运输评估Agent"""
    
    def __init__(self):
        self.name = AgentRole.TRANSPORT
        
        # 多式联运方案库
        self._intermodal_routes = {
            ("马尼拉港", "巴生港"): "海运直达（3天）",
            ("马尼拉港", "新加坡港"): "海运+铁路（4天）",
            ("河内工厂", "深圳工厂"): "陆运（2天）",
            ("河内工厂", "曼谷工厂"): "公路+海运（5天）",
            ("洛杉矶港", "温哥华港"): "铁路（4天）",
            ("洛杉矶港", "休斯顿港"): "铁路+公路（6天）"
        }
    
    def calc_feasibility(self, proposal: Proposal) -> AgentEvaluation:
        """计算运输可行性和最优路径"""
        # 提取港口/工厂名称用于路由匹配
        from_location = proposal.supplier_from.split("-")[0]
        to_location = proposal.supplier_to.split("-")[0]
        
        route_key = (from_location, to_location)
        route = self._intermodal_routes.get(route_key, "多式联运组合")
        
        # 模拟运输成本和时间计算
        transit_time = int(route.split("（")[1].replace("天）", "")) if "天）" in route else 5
        delay_risk = min(transit_time / 10, 1.0)
        
        passed = delay_risk < 0.6
        
        if passed:
            reasoning = f"运输可行：{route}，延误风险{d

elay_risk:.0%}"
            suggestions = []
        else:
            reasoning = f"运输高风险：{route}，延误风险{d

elay_risk:.0%}，建议启用备选路线"
            suggestions = [
                "建议拆分运输：急单空运，大货海运",
                "考虑中转港避让拥堵区域",
                "预book铁路运力作为backup"
            ]
        
        return AgentEvaluation(
            agent_role=self.name,
            score=delay_risk,
            passed=passed,
            reasoning=reasoning,
            suggestions=suggestions
        )
