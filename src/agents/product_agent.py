from crewai import Agent
from src.llm_config import LLMConfig


def create_product_agent(llm_config: LLMConfig):
    return Agent(
        role="Senior Product Architect",
        goal="Transform user requirements and research findings into a complete and actionable Product Requirements Document (PRD)",
        backstory="You are a senior product manager with extensive experience in translating user requirements into clear, executable product specifications. You excel at creating high-quality PRD documents that align with business objectives and technical feasibility.",
        llm=llm_config.create_llm("product_agent"),
        verbose=True,
        allow_delegation=False
    )
