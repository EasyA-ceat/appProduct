from crewai import Task


def create_deployment_task(agent):
    return Task(
        description="""制定部署方案并实现自动化部署：
        
        请制定部署方案并实现：
        1. 部署环境规划
        2. CI/CD流水线设计
        3. 容器化配置
        4. 监控和运维方案
        5. 部署文档
        
        请输出完整的部署方案。""",
        agent=agent,
        expected_output="完整的部署方案和文档"
    )
