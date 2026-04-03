import click
from src.monitoring.metrics import MetricsCollector
from src.cli.display import display_header, display_metrics


@click.command(name="metrics")
def metrics_command():
    """查看指标统计"""
    display_header("指标统计")
    
    metrics = MetricsCollector()
    display_metrics(metrics)
