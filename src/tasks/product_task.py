from crewai import Task


def create_product_task(agent, user_idea: str):
    return Task(
        description=f"""基于用户想法和调研报告编写PRD文档：
        用户想法: {user_idea}
        
        请参考前面的调研报告，编写完整的产品需求文档(PRD)，包含：
        1. 产品概述：产品定位、目标、愿景
        2. 用户故事：核心用户场景
        3. 功能需求：详细功能列表
        4. 非功能需求：性能、安全、可用性等
        5. 产品 roadmap：阶段规划
        
        请输出完整的PRD文档。""",
        agent=agent,
        expected_output="完整的产品需求文档(PRD)"
    )
