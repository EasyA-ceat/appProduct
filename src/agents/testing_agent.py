from crewai import Agent
from src.llm_config import LLMConfig


def create_testing_agent(llm_config: LLMConfig):
    return Agent(
        role="资深测试架构师",
        goal="制定测试计划并执行全面测试",
        backstory="你是一位资深的测试专家，擅长制定测试策略，发现系统bug，确保产品质量。",
        llm=llm_config.create_llm("testing_agent"),
        verbose=True,
        allow_delegation=False
    )
