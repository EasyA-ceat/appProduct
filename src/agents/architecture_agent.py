from crewai import Agent
from src.llm_config import LLMConfig


def create_architecture_agent(llm_config: LLMConfig):
    return Agent(
        role="技术架构师",
        goal="设计系统技术架构和技术方案",
        backstory="你是一位资深的后端架构师和DevOps专家，擅长设计高可用、可扩展的系统架构。",
        llm=llm_config.create_llm("architecture_agent"),
        verbose=True,
        allow_delegation=False
    )
