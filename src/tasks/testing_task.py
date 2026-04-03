from crewai import Task


def create_testing_task(agent):
    return Task(
        description="""对开发完成的系统进行测试：
        
        请制定测试计划并执行测试：
        1. 测试计划
        2. 测试用例设计
        3. 功能测试
        4. 性能测试
        5. 测试报告
        
        请输出完整的测试报告。""",
        agent=agent,
        expected_output="完整的测试报告"
    )
