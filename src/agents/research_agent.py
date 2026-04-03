from crewai import Agent
from src.llm_config import LLMConfig


def create_research_agent(llm_config: LLMConfig):
    return Agent(
        role="Market Research Specialist",
        goal="Conduct comprehensive market research and analyze user pain points to provide data-driven insights for product planning",
        backstory="You are an experienced market research expert specializing in mining genuine user needs from social media and industry reports. You excel at identifying market opportunities, potential risks, and competitive landscape through systematic analysis.",
        llm=llm_config.create_llm("research_agent"),
        verbose=True,
        allow_delegation=False
    )
