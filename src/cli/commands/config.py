import click
from src.llm_config import LLMConfig
from src.output_config import OutputConfigManager
from src.cli.display import (
    display_header,
    display_agent_config,
    display_output_config,
    display_space_usage
)


@click.group(name="config")
def config_group():
    """配置管理"""
    pass


@config_group.group(name="agents")
def agents_group():
    """Agent LLM 配置"""
    pass


@agents_group.command(name="list")
@click.option("--config", "-c", default="config/agents.yaml", help="配置文件路径")
def agents_list(config):
    """列出所有Agent配置"""
    display_header("Agent LLM 配置")
    
    llm_config = LLMConfig(config)
    display_agent_config(llm_config)


@agents_group.command(name="show")
@click.argument("agent_name")
@click.option("--config", "-c", default="config/agents.yaml", help="配置文件路径")
def agents_show(agent_name, config):
    """显示指定Agent配置"""
    display_header(f"Agent 配置: {agent_name}")
    
    llm_config = LLMConfig(config)
    agent_config = llm_config.get_agent_config(agent_name)
    
    if not agent_config:
        click.secho(f"未找到 Agent: {agent_name}", fg="red")
        return
    
    from rich.table import Table
    from rich.console import Console
    console = Console()
    
    table = Table()
    table.add_column("配置项", style="cyan")
    table.add_column("值", style="magenta")
    
    for key, value in agent_config.items():
        table.add_row(key, str(value))
    
    console.print(table)


@agents_group.command(name="set")
@click.argument("agent_name")
@click.option("--llm", help="LLM提供商 (openai/anthropic)")
@click.option("--model", help="模型名称")
@click.option("--temperature", type=float, help="温度参数")
@click.option("--max-tokens", type=int, help="最大token数")
@click.option("--config", "-c", default="config/agents.yaml", help="配置文件路径")
def agents_set(agent_name, llm, model, temperature, max_tokens, config):
    """修改Agent配置"""
    llm_config = LLMConfig(config)
    agent_config = llm_config.get_agent_config(agent_name)
    
    if not agent_config:
        click.secho(f"未找到 Agent: {agent_name}", fg="red")
        return
    
    if llm:
        agent_config['llm_provider'] = llm
    if model:
        agent_config['model'] = model
    if temperature is not None:
        agent_config['temperature'] = temperature
    if max_tokens is not None:
        agent_config['max_tokens'] = max_tokens
    
    llm_config.set_agent_config(agent_name, agent_config)
    
    click.secho(f"Agent {agent_name} 配置已更新", fg="green")
    display_agent_config(llm_config)


@config_group.group(name="output")
def output_group():
    """输出配置"""
    pass


@output_group.command(name="list")
@click.option("--config", "-c", default="config/output.yaml", help="配置文件路径")
def output_list(config):
    """列出输出配置"""
    display_header("输出配置")
    
    output_config = OutputConfigManager(config)
    display_output_config(output_config)


@output_group.command(name="set")
@click.option("--max-total-size", help="最大总空间 (如: 500MB)")
@click.option("--max-file-size", help="最大单文件 (如: 50MB)")
@click.option("--space-limit-strategy", help="空间超限策略 (warn/stop/auto_clean)")
@click.option("--compress-output", type=bool, help="是否压缩输出")
@click.option("--config", "-c", default="config/output.yaml", help="配置文件路径")
def output_set(max_total_size, max_file_size, space_limit_strategy, compress_output, config):
    """修改输出配置"""
    output_config = OutputConfigManager(config)
    
    if max_total_size:
        output_config.config.max_total_size = max_total_size
    if max_file_size:
        output_config.config.max_file_size = max_file_size
    if space_limit_strategy:
        output_config.config.space_limit_strategy = space_limit_strategy
    if compress_output is not None:
        output_config.config.compress_output = compress_output
    
    output_config.save_config()
    
    click.secho("输出配置已更新", fg="green")
    display_output_config(output_config)


@output_group.command(name="space")
@click.option("--config", "-c", default="config/output.yaml", help="配置文件路径")
def output_space(config):
    """查看空间使用情况"""
    display_header("空间使用情况")
    
    output_config = OutputConfigManager(config)
    display_space_usage(
        output_config.config.output_dir,
        output_config.get_max_total_size_bytes()
    )


@output_group.command(name="allow-ext")
@click.option("--add", "-a", multiple=True, help="添加允许的文件扩展名")
@click.option("--remove", "-r", multiple=True, help="移除允许的文件扩展名")
@click.option("--config", "-c", default="config/output.yaml", help="配置文件路径")
def output_allow_ext(add, remove, config):
    """管理允许的文件扩展名"""
    output_config = OutputConfigManager(config)
    
    for ext in add:
        if ext not in output_config.config.allowed_file_types:
            output_config.config.allowed_file_types.append(ext)
            click.secho(f"已添加: {ext}", fg="green")
    
    for ext in remove:
        if ext in output_config.config.allowed_file_types:
            output_config.config.allowed_file_types.remove(ext)
            click.secho(f"已移除: {ext}", fg="red")
    
    output_config.save_config()
    display_output_config(output_config)
