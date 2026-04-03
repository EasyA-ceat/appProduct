from crewai import Agent
from src.llm_config import LLMConfig


def create_research_product_agent(llm_config: LLMConfig):
    return Agent(
        role="产品调研复核专家",
        goal="复核PRD文档，结合市场调研结果进行验证和补充",
        backstory="你是一位严谨的产品复核专家，擅长通过搜索验证PRD的可行性，发现潜在问题并提出改进建议。",
        llm=llm_config.create_llm("research_product_agent"),
        verbose=True,
        allow_delegation=False
    )
