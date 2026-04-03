#!/usr/bin/env python3
import click
from dotenv import load_dotenv

load_dotenv()

from src.cli.commands.run import run_command
from src.cli.commands.status import status_command
from src.cli.commands.logs import logs_command
from src.cli.commands.metrics import metrics_command
from src.cli.commands.config import config_group


@click.group()
def cli():
    """App 全自动生产工作流 - 基于 CrewAI 的多 Agent 协作系统"""
    pass


cli.add_command(run_command)
cli.add_command(status_command)
cli.add_command(logs_command)
cli.add_command(metrics_command)
cli.add_command(config_group)


if __name__ == "__main__":
    cli()
