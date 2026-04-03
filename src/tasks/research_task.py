from crewai import Task
from src.agents.research_agent import create_research_agent


def create_research_task(agent, user_idea: str):
    return Task(
        description=f"""基于用户想法进行市场调研：
        用户想法: {user_idea}
        
        请完成以下调研内容：
        1. 市场分析：分析该产品的市场规模、增长趋势
        2. 用户分析：目标用户画像、痛点需求
        3. 竞品分析：主要竞争对手分析
        4. 机会分析：市场机会和切入点
        5. 风险分析：潜在风险和应对建议
        
        请输出详细的调研报告。""",
        agent=agent,
        expected_output="详细的市场调研报告，包含市场分析、用户分析、竞品分析等内容"
    )
