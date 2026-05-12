"""感知Agent - 风险信号采集与实体对齐"""
import random
from datetime import datetime
from typing import Optional
from ..models import RiskEvent, AlertLevel, AgentRole


class PerceptionAgent:
    """7x24风险感知Agent"""
    
    def __init__(self):
        self.name = AgentRole.PERCEPTION
        self.scanned_events = 0
        
    def scan(self) -> Optional[RiskEvent]:
        """
        扫描外部数据源，发现风险事件
        实际生产环境接入：新闻API、气象API、港口数据API等
        """
        # 30%概率发现风险
        if random.random() > 0.3:
            return None
            
        self.scanned_events += 1
        event_id = f"EVT-{self.scanned_events:06d}"
        
        scenarios = [
            {
                "type": "台风",
                "supplier": "马尼拉港-供应商A",
                "skus": ["SKU-8842", "SKU-8843"],
                "severity": AlertLevel.RED,
                "source": "国家气象局",
                "chain": [
                    "台风海神形成",
                    "路径预测：72h后抵达马尼拉",
                    "马尼拉港将关闭48-72h",
                    "影响SCP航线",
                    "波及SKU-8842/8843的BOM层级"
                ]
            },
            {
                "type": "限电",
                "supplier": "河内工厂-供应商B",
                "skus": ["SKU-7721"],
                "severity": AlertLevel.YELLOW,
                "source": "越南电力公司公告",
                "chain": [
                    "越南北部电力短缺",
                    "河内工业区发布限电通知",
                    "供应商B工厂产能受限60%",
                    "影响SKU-7721交付"
                ]
            },
            {
                "type": "港口拥堵",
                "supplier": "洛杉矶港-供应商C", 
                "skus": ["SKU-3390", "SKU-3391"],
                "severity": AlertLevel.YELLOW,
                "source": "MarineTraffic AIS数据",
                "chain": [
                    "洛杉矶港泊位利用率>90%",
                    "平均等待时间增加至5天",
                    "供应商C货物滞留",
                    "影响SKU-3390/3391到港时间"
                ]
            }
        ]
        
        scenario = random.choice(scenarios)
        return RiskEvent(
            event_id=event_id,
            timestamp=datetime.now(),
            event_type=scenario["type"],
            affected_supplier=scenario["supplier"],
            affected_skus=scenario["skus"],
            duration_hours=random.randint(24, 96),
            severity=scenario["severity"],
            source=scenario["source"],
            reasoning_chain=scenario["chain"]
        )
