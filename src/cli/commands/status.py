import click
from src.monitoring.state_tracker import StateTracker
from src.monitoring.metrics import MetricsCollector
from src.cli.display import display_header, display_workflow_status


@click.command(name="status")
def status_command():
    """查看工作流当前状态"""
    display_header("工作流状态")
    
    state_tracker = StateTracker()
    metrics = MetricsCollector()
    
    display_workflow_status(state_tracker, metrics)
