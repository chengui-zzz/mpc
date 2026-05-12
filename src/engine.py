"""多Agent协作引擎 - 沙盘推演核心"""
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .models import Decision, RiskEvent, AgentEvaluation
from .agents import (
    PerceptionAgent,
    PlanningAgent,
    InventoryAgent,
    SupplierAgent,
    TransportAgent
)


class SandboxEngine:
    """多Agent协作沙盘引擎"""
    
    def __init__(self):
        self.console = Console()
        
        # 初始化所有Agent
        self.perception = PerceptionAgent()
        self.planning = PlanningAgent()
        self.inventory = InventoryAgent()
        self.supplier = SupplierAgent()
        self.transport = TransportAgent()
        
        # 决策历史（用于反思学习）
        self.decision_history: List[Decision] = []
    
    def run_cycle(self) -> Optional[Decision]:
        """执行一次完整的感知-决策-协作循环"""
        self.console.rule("[bold blue]供应链风险巡检周期")
        
        # 阶段1：感知
        self.console.print("\n[bold]🔍 阶段1：风险感知[/bold]")
        event = self.perception.scan()
        
        if not event:
            self.console.print("[green]✅ 本轮未发现风险事件[/green]")
            return None
        
        # 显示风险信息
        self._display_risk_event(event)
        
        # 阶段2：规划
        self.console.print("\n[bold]📋 阶段2：方案规划[/bold]")
        proposal = self.planning.propose(event)
        self._display_proposal(proposal)
        
        # 阶段3：多Agent协作评估
        self.console.print("\n[bold]🤝 阶段3：多Agent协作评估[/bold]")
        evaluations = self._collaborative_evaluation(proposal)
        
        # 阶段4：汇聚决策
        self.console.print("\n[bold]⚖️  阶段4：决策汇聚[/bold]")
        decision = self._aggregate_decision(proposal, evaluations, event)
        
        # 记录历史
        self.decision_history.append(decision)
        
        return decision
    
    def _display_risk_event(self, event: RiskEvent):
        """展示风险事件详情"""
        table = Table(title="风险事件详情")
        table.add_column("字段", style="cyan")
        table.add_column("值", style="white")
        
        table.add_row("事件ID", event.event_id)
        table.add_row("类型", event.event_type)
        table.add_row("影响供应商", event.affected_supplier)
        table.add_row("影响SKU", ", ".join(event.affected_skus))
        table.add_row("严重程度", f"[{event.severity.value}]{event.severity.value}[/]")
        table.add_row("数据来源", event.source)
        
        self.console.print(table)
        
        # 显示推理链
        self.console.print("\n[bold]多跳推理链：[/bold]")
        for i, step in enumerate(event.reasoning_chain, 1):
            self.console.print(f"  {i}. {step}")
    
    def _display_proposal(self, proposal):
        """展示应急方案"""
        panel = Panel(
            f"[bold]方案：[/bold]{proposal.description}\n"
            f"成本增加：{proposal.cost_increase_pct}%\n"
            f"预计交期：{proposal.lead_time_days}天\n"
            f"备选方案：{', '.join(proposal.alternatives) if proposal.alternatives else '无'}",
            title="规划Agent方案",
            border_style="yellow"
        )
        self.console.print(panel)
    
    def _collaborative_evaluation(self, proposal) -> List[AgentEvaluation]:
        """
        多Agent协作评估
        各Agent从自身维度评估方案，给出通过/否决意见
        """
        evaluations = []
        
        # 库存Agent评估
        self.console.print("\n[cyan]📦 库存Agent评估中...[/cyan]")
        inv_eval = self.inventory.evaluate(proposal)
        evaluations.append(inv_eval)
        self._display_evaluation(inv_eval)
        
        # 供应商Agent评估
        self.console.print("\n[cyan]🏭 供应商Agent评估中...[/cyan]")
        supp_eval = self.supplier.check_constraints(proposal)
        evaluations.append(supp_eval)
        self._display_evaluation(supp_eval)
        
        # 运输Agent评估
        self.console.print("\n[cyan]🚚 运输Agent评估中...[/cyan]")
        trans_eval = self.transport.calc_feasibility(proposal)
        evaluations.append(trans_eval)
        self._display_evaluation(trans_eval)
        
        return evaluations
    
    def _display_evaluation(self, evaluation: AgentEvaluation):
        """显示单个Agent的评估结果"""
        status = "✅ 通过" if evaluation.passed else "❌ 未通过"
        self.console.print(
            f"  [{evaluation.agent_role.value}] {status} "
            f"(分数: {evaluation.score:.2f})"
        )
        self.console.print(f"  理由: {evaluation.reasoning}")
        if evaluation.suggestions:
            for sug in evaluation.suggestions:
                self.console.print(f"  💡 {sug}")
    
    def _aggregate_decision(
        self, 
        proposal
