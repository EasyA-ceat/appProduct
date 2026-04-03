from crewai import Task


def create_architecture_task(agent):
    return Task(
        description="""基于设计文档进行技术架构设计：
        
        请根据设计文档进行技术架构设计：
        1. 系统架构设计
        2. 技术选型说明
        3. 数据库设计
        4. API接口设计
        5. 部署架构设计
        
        请输出详细的技术架构文档。""",
        agent=agent,
        expected_output="详细的技术架构文档"
    )
