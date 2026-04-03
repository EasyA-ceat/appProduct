from crewai import Task


def create_research_product_task(agent):
    return Task(
        description="""复核PRD文档，验证其可行性：
        
        请基于前面的调研报告，对PRD文档进行复核：
        1. 验证PRD中的需求是否符合市场调研结果
        2. 检查是否有遗漏的用户需求
        3. 评估技术可行性
        4. 提出改进建议
        
        请输出复核报告。""",
        agent=agent,
        expected_output="PRD复核报告，包含验证结果和改进建议"
    )
