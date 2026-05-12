
"""核心数据模型定义"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from datetime import datetime


class AlertLevel(Enum):
    GREEN = "green"
    YELLOW = "yellow" 
    RED = "red"


class AgentRole(Enum):
    PERCEPTION = "perception"
    PLANNING = "planning"
    INVENTORY = "inventory"
    SUPPLIER = "supplier"
    TRANSPORT = "transport"
    REFLECTION = "reflection"


@dataclass
class RiskEvent:
    """感知Agent输出的结构化风险"""
    event_id: str
    timestamp: datetime
    event_type: str          # 台风、限电、港口拥堵
    affected_supplier: str
    affected_skus: List[str]
    duration_hours: int
    severity: AlertLevel
    source: str              # 数据来源
    # 多跳推理链
    reasoning_chain: List[str] = field(default_factory=list)


@dataclass 
class Proposal:
    """规划Agent的方案"""
    action: str
    supplier_from: str
    supplier_to: str
    cost_increase_pct: float
    lead_time_days: int
    description: str
    alternatives: List[str] = field(default_factory=list)


@dataclass
class AgentEvaluation:
    """单个Agent的评估结果"""
    agent_role: AgentRole
    score: float             # 0-1，越低越好
    passed: bool
    reasoning: str
    suggestions: List[str] = field(default_factory=list)


@dataclass
class Decision:
    """最终决策"""
    proposal: Proposal
    evaluations: List[AgentEvaluation]
    approved: bool
    requires_manual_review: bool
    final_reasoning: str
    reflection_notes: Optional[str] = None
