from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.layout import Layout
from rich.text import Text
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from src.monitoring.state_tracker import StateTracker, TaskStatus
from src.monitoring.metrics import MetricsCollector


console = Console()


def format_duration(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))


def display_header(title: str):
    console.print(Panel(f"[bold cyan]{title}[/bold cyan]", expand=False))


def display_workflow_status(state_tracker: StateTracker, metrics: MetricsCollector):
    layout = Layout()
    
    task_order = [
        "research", "product", "research_product", 
        "design", "architecture", "development", 
        "security_review", "testing", "deployment"
    ]
    
    task_display_names = {
        "research": "调研阶段",
        "product": "产品阶段",
        "research_product": "调研产品",
        "design": "设计阶段",
        "architecture": "架构阶段",
        "development": "开发阶段",
        "security_review": "安全审查",
        "testing": "测试阶段",
        "deployment": "部署阶段"
    }
    
    table = Table(title="工作流执行状态")
    table.add_column("序号", style="cyan")
    table.add_column("阶段", style="magenta")
    table.add_column("状态", style="green")
    table.add_column("耗时", style="yellow")
    
    for idx, task_name in enumerate(task_order, 1):
        task = state_tracker.tasks.get(task_name)
        if task:
            status_icon = {
                TaskStatus.PENDING: "○ 等待",
                TaskStatus.IN_PROGRESS: "● 执行中",
                TaskStatus.COMPLETED: "✓ 完成",
                TaskStatus.FAILED: "✗ 失败"
            }.get(task.status, "○ 等待")
            
            status_color = {
                TaskStatus.PENDING: "white",
                TaskStatus.IN_PROGRESS: "yellow",
                TaskStatus.COMPLETED: "green",
                TaskStatus.FAILED: "red"
            }.get(task.status, "white")
            
            duration = format_duration(task.duration_seconds) if task.duration_seconds > 0 else "-"
        else:
            status_icon = "○ 等待"
            status_color = "white"
            duration = "-"
        
        table.add_row(
            str(idx),
            task_display_names.get(task_name, task_name),
            f"[{status_color}]{status_icon}[/{status_color}]",
            duration
        )
    
    progress = state_tracker.get_progress()
    total_duration = state_tracker.get_total_duration()
    
    console.print(table)
    console.print()
    console.print(f"总进度: [bold]{progress:.1f}%[/bold] | 已运行时间: [bold yellow]{format_duration(total_duration)}[/bold yellow]")


def display_metrics(metrics: MetricsCollector):
    summary = metrics.get_summary()
    
    table = Table(title="指标统计")
    table.add_column("指标", style="cyan")
    table.add_column("值", style="magenta")
    
    table.add_row("总耗时", format_duration(summary['total_duration_seconds']))
    table.add_row("总 Token 使用", f"{summary['total_tokens']:,}")
    table.add_row("成功率", f"{summary['success_rate']:.1f}%")
    table.add_row("任务数", str(summary['task_count']))
    
    console.print(table)
    
    if summary['task_metrics']:
        console.print()
        task_table = Table(title="各任务指标")
        task_table.add_column("任务", style="cyan")
        task_table.add_column("状态", style="magenta")
        task_table.add_column("耗时", style="yellow")
        task_table.add_column("Token", style="green")
        
        for task_name, task_metric in summary['task_metrics'].items():
            status = "✓ 成功" if task_metric['success'] else "✗ 失败"
            status_color = "green" if task_metric['success'] else "red"
            task_table.add_row(
                task_name,
                f"[{status_color}]{status}[/{status_color}]",
                format_duration(task_metric['duration_seconds']),
                f"{task_metric['token_usage']:,}"
            )
        
        console.print(task_table)


def display_logs(logs: list, tail: int = 50):
    console.print(Panel("执行日志", expand=False))
    for line in logs[-tail:]:
        console.print(line.rstrip())


def display_agent_config(llm_config):
    agents = llm_config.config.get('agents', {})
    
    table = Table(title="Agent LLM 配置")
    table.add_column("Agent", style="cyan")
    table.add_column("Provider", style="magenta")
    table.add_column("Model", style="yellow")
    table.add_column("Temperature", style="green")
    
    for agent_name, config in agents.items():
        table.add_row(
            agent_name,
            config.get('llm_provider', '-'),
            config.get('model', '-'),
            str(config.get('temperature', '-'))
        )
    
    console.print(table)


def display_output_config(output_config):
    config = output_config.config
    
    table = Table(title="输出配置")
    table.add_column("配置项", style="cyan")
    table.add_column("值", style="magenta")
    
    table.add_row("最大总空间", config.max_total_size)
    table.add_row("最大单文件", config.max_file_size)
    table.add_row("输出目录", config.output_dir)
    table.add_row("日志目录", config.logs_dir)
    table.add_row("空间策略", config.space_limit_strategy)
    table.add_row("压缩输出", "是" if config.compress_output else "否")
    
    console.print(table)
    
    console.print()
    console.print("允许的文件类型:")
    file_types_table = Table(show_header=False, box=None)
    file_types = config.allowed_file_types
    for i in range(0, len(file_types), 4):
        row = file_types[i:i+4]
        row.extend([''] * (4 - len(row)))
        file_types_table.add_row(*row)
    console.print(file_types_table)


def display_space_usage(output_dir: str, max_size: int):
    import os
    
    total_size = 0
    file_count = 0
    
    if os.path.exists(output_dir):
        for dirpath, dirnames, filenames in os.walk(output_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
                file_count += 1
    
    usage_percent = (total_size / max_size) * 100 if max_size > 0 else 0
    
    def format_size(size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    table = Table(title="空间使用情况")
    table.add_column("项目", style="cyan")
    table.add_column("值", style="magenta")
    
    table.add_row("已使用空间", format_size(total_size))
    table.add_row("最大空间", format_size(max_size))
    table.add_row("使用率", f"{usage_percent:.1f}%")
    table.add_row("文件数量", str(file_count))
    
    console.print(table)
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("空间使用", total=100)
        progress.update(task, completed=usage_percent)


def display_success():
    console.print()
    console.print(Panel("[bold green]✓ 工作流执行成功！[/bold green]", expand=False))


def display_error(error: str):
    console.print()
    console.print(Panel(f"[bold red]✗ 错误: {error}[/bold red]", expand=False))
