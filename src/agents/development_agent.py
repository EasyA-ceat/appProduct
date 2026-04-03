from crewai import Agent
from src.llm_config import LLMConfig


def create_development_agent(llm_config: LLMConfig):
    return Agent(
        role="全栈开发工程师",
        goal="根据架构设计实现前后端代码",
        backstory="你是一位资深的全栈开发工程师，擅长前端和后端开发，能够写出高质量、可维护的代码。",
        llm=llm_config.create_llm("development_agent"),
        verbose=True,
        allow_delegation=False
    )
