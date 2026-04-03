import click
from src.input.parser import IdeaParser
from src.workflow.crew import AppWorkflowCrew
from src.cli.display import (
    display_header,
    display_workflow_status,
    display_metrics,
    display_success,
    display_error
)


@click.command(name="run")
@click.option("--idea", "-i", help="直接输入您的APP想法")
@click.option("--idea-file", "-f", help="从文件读取APP想法")
@click.option("--config", "-c", default="config/agents.yaml", help="Agent配置文件路径")
@click.option("--output-config", "-o", default="config/output.yaml", help="输出配置文件路径")
def run_command(idea, idea_file, config, output_config):
    """运行APP生产工作流"""
    display_header("App 生产工作流")
    
    idea_parser = IdeaParser()
    user_idea = idea_parser.parse_from_cli(idea, idea_file)
    
    click.echo()
    click.secho(f"您的想法: {user_idea}", fg="cyan")
    click.echo()
    
    if not click.confirm("确认开始工作流？", default=True):
        click.echo("已取消")
        return
    
    crew = AppWorkflowCrew(
        llm_config_path=config,
        output_config_path=output_config
    )
    
    success = crew.run(user_idea)
    
    display_workflow_status(crew.state_tracker, crew.metrics)
    click.echo()
    display_metrics(crew.metrics)
    
    if success:
        display_success()
    else:
        display_error("工作流执行失败，请查看日志")
