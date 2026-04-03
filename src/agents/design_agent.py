from crewai import Agent
from src.llm_config import LLMConfig


def create_design_agent(llm_config: LLMConfig):
    return Agent(
        role="UIUX设计架构师",
        goal="根据PRD设计用户界面和交互体验",
        backstory="你是一位资深的UI/UX设计师，擅长创造美观且易用的用户界面，注重用户体验和视觉设计。",
        llm=llm_config.create_llm("design_agent"),
        verbose=True,
        allow_delegation=False
    )
