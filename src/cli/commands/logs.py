import click
from src.monitoring.logger import WorkflowLogger
from src.cli.display import display_header, display_logs


@click.command(name="logs")
@click.option("--tail", "-n", default=50, type=int, help="显示最后N行日志")
def logs_command(tail):
    """查看执行日志"""
    display_header("执行日志")
    
    logger = WorkflowLogger()
    logs = logger.get_recent_logs(tail=tail)
    
    display_logs(logs, tail=tail)
