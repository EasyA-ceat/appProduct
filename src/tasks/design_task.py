from crewai import Task


def create_design_task(agent):
    return Task(
        description="""基于PRD进行UI/UX设计：
        
        请根据PRD文档进行UI/UX设计：
        1. 信息架构设计
        2. 页面流程设计
        3. 关键页面UI设计描述
        4. 交互设计说明
        5. 设计规范建议
        
        请输出详细的设计文档。""",
        agent=agent,
        expected_output="详细的UI/UX设计文档"
    )
