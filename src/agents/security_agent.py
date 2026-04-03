from crewai import Agent
from src.llm_config import LLMConfig


def create_security_agent(llm_config: LLMConfig):
    return Agent(
        role="Senior Security Reviewer",
        goal="Conduct comprehensive security audit on the developed system, identify vulnerabilities, and provide actionable security recommendations",
        backstory="You are a senior security expert specializing in code security auditing, dependency analysis, sensitive information leak detection, and vulnerability scanning. You excel at identifying security weaknesses and providing remediation guidance.",
        llm=llm_config.create_llm("security_agent"),
        verbose=True,
        allow_delegation=False
    )
