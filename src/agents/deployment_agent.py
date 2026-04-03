from crewai import Agent
from src.llm_config import LLMConfig


def create_deployment_agent(llm_config: LLMConfig):
    return Agent(
        role="DevOps架构师",
        goal="制定部署方案并实现自动化部署",
        backstory="你是一位资深的DevOps专家，擅长CI/CD流水线设计，实现自动化部署和运维。",
        llm=llm_config.create_llm("deployment_agent"),
        verbose=True,
        allow_delegation=False
    )
