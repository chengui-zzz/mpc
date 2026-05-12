"""主程序入口"""
import sys
import time
from rich.console import Console
from rich.panel import Panel
from engine import SandboxEngine


def main():
    console = Console()
    
    console.print(Panel.fit(
        "[bold cyan]供应链风险巡检多Agent协作系统 v1.0[/bold cyan]\n"
        "[dim]感知 → 规划 → 多Agent博弈 → 决策 → 执行[/dim]",
        border_style="cyan"
    ))
    
    engine = SandboxEngine()
    
    # 运行多个巡检周期
    cycles = 3
    for i in range(cycles):
        console.print(f"\n[bold]══════ 第 {i+1}/{cycles} 轮巡检 ══════[/bold]")
        decision = engine.run_cycle()
        
        if decision:
            console.print(f"\n[bold]📊 决策摘要：[/bold]")
            console.print(f"  方案：{decision.proposal.description}")
            console.print(f"  结果：{'✅ 通过' if decision.approved else '❌ 否决'}")
            console.print(f"  审核：{'需要' if decision.requires_manual_review else '自动执行'}")
        
        time.sleep(1)  # 模拟巡检间隔
    
    # 输出统计
    console.print("\n[bold green]══════ 巡检完成 ══════[/bold green]")
    total = len(engine.decision_history)
    approved = sum(1 for d in engine.decision_history if d.approved)
    console.print(f"总决策数：{total}")
    console.print(f"通过率：{approved}/{total} ({approved/total*100:.0f}%)" if total > 0 else "无决策")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
