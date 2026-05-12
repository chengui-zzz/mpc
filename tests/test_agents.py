"""Agent单元测试"""
import unittest
from datetime import datetime
from src.models import RiskEvent, AlertLevel
from src.agents import (
    PerceptionAgent,
    PlanningAgent,
    InventoryAgent,
    SupplierAgent,
    TransportAgent
)


class TestAgents(unittest.TestCase):
    
    def setUp(self):
        self.perception = PerceptionAgent()
        self.planning = PlanningAgent()
        self.inventory = InventoryAgent()
        self.supplier = SupplierAgent()
        self.transport = TransportAgent()
        
        self.sample_event = RiskEvent(
            event_id="TEST-001",
            timestamp=datetime.now(),
            event_type="台风",
            affected_supplier="马尼拉港-供应商A",
            affected_skus=["SKU-8842"],
            duration_hours=48,
            severity=AlertLevel.RED,
            source="测试"
        )
    
    def test_perception_scan(self):
        """测试感知Agent"""
        # 多次扫描，确保有时返回事件
        events = []
        for _ in range(10):
            event = self.perception.scan()
            if event:
                events.append(event)
        self.assertGreater(len(events), 0, "应至少捕获一个风险事件")
    
    def test_planning_propose(self):
        """测试规划Agent"""
        proposal = self.planning.propose(self.sample_event)
        self.assertIsNotNone(proposal)
        self.assertGreater(proposal.cost_increase_pct, 0)
    
    def test_inventory_evaluate(self):
        """测试库存Agent"""
        proposal = self.planning.propose(self.sample_event)
        evaluation = self.inventory.evaluate(proposal)
        self.assertIsNotNone(evaluation)
        self.assertTrue(0 <= evaluation.score <= 1)
    
    def test_supplier_check(self):
        """测试供应商Agent"""
        proposal = self.planning.propose(self.sample_event)
        evaluation = self.supplier.check_constraints(proposal)
        self.assertIsNotNone(evaluation)
    
    def test_transport_feasibility(self):
        """测试运输Agent"""
        proposal = self.planning.propose(self.sample_event)
        evaluation = self.transport.calc_feasibility(proposal)
        self.assertIsNotNone(evaluation)


if __name__ == "__main__":
    unittest.main()
