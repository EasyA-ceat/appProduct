from crewai import Task


def create_development_task(agent):
    return Task(
        description="""基于架构文档进行代码开发：
        
        请根据技术架构文档进行代码实现：
        1. 项目结构搭建
        2. 后端代码实现
        3. 前端代码实现
        4. 配置文件
        5. 部署脚本
        
        请输出可运行的代码实现。""",
        agent=agent,
        expected_output="完整的代码实现，包含前端和后端代码"
    )
