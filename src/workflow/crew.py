from crewai import Crew, Process, Task
from typing import Optional

from src.llm_config import LLMConfig
from src.output_config import OutputConfigManager
from src.monitoring.state_tracker import StateTracker
from src.monitoring.logger import WorkflowLogger
from src.monitoring.metrics import MetricsCollector
from src.output.manager import OutputManager
from src.output.validator import OutputValidator
from src.workflow.context import WorkflowContext

from src.agents.research_agent import create_research_agent
from src.agents.product_agent import create_product_agent
from src.agents.research_product_agent import create_research_product_agent
from src.agents.design_agent import create_design_agent
from src.agents.architecture_agent import create_architecture_agent
from src.agents.development_agent import create_development_agent
from src.agents.security_agent import create_security_agent
from src.agents.testing_agent import create_testing_agent
from src.agents.deployment_agent import create_deployment_agent


class AppWorkflowCrew:
    def __init__(
        self,
        llm_config_path: str = "config/agents.yaml",
        output_config_path: str = "config/output.yaml"
    ):
        self.llm_config = LLMConfig(llm_config_path)
        self.output_config = OutputConfigManager(output_config_path)
        
        self.state_tracker = StateTracker()
        self.logger = WorkflowLogger()
        self.metrics = MetricsCollector()
        self.output_manager = OutputManager(self.output_config.config.output_dir)
        self.output_validator = OutputValidator(
            self.output_config.get_max_total_size_bytes(),
            self.output_config.get_max_file_size_bytes(),
            self.output_config.config.allowed_file_types
        )
        
        self.context = WorkflowContext()
        self.project_dir: Optional[str] = None
        self.task_results = {}
        self.max_retries = 3
    
    def setup(self, user_idea: str):
        self.context.user_idea = user_idea
        self.project_dir = self.output_manager.create_project_dir()
        
        self.state_tracker.reset()
        self.metrics.reset()
        self.task_results = {}
        
        task_names = [
            "research", "product", "research_product",
            "design", "architecture", "development",
            "security_review", "testing", "deployment"
        ]
        for task_name in task_names:
            self.state_tracker.init_task(task_name)
    
    def _save_task_output(self, task_name: str, output):
        output_str = str(output)
        
        total_valid, total_msg = self.output_validator.validate_total_size(self.project_dir)
        if not total_valid:
            if self.output_config.config.space_limit_strategy == "stop":
                self.logger.warning(f"空间限制: {total_msg}，停止保存输出")
                return
            elif self.output_config.config.space_limit_strategy == "warn":
                self.logger.warning(f"空间警告: {total_msg}")
        
        filepath = None
        if task_name == "research":
            self.context.research_report = output_str
            filepath = self.output_manager.save_research_report(self.project_dir, output_str)
        elif task_name == "product":
            self.context.prd_document = output_str
            filepath = self.output_manager.save_prd_document(self.project_dir, output_str)
        elif task_name == "research_product":
            self.context.research_product_report = output_str
            filepath = self.output_manager.save_research_product_report(self.project_dir, output_str)
        elif task_name == "design":
            self.context.design_document = output_str
            filepath = self.output_manager.save_design_document(self.project_dir, output_str)
        elif task_name == "architecture":
            self.context.architecture_document = output_str
            filepath = self.output_manager.save_architecture_document(self.project_dir, output_str)
        elif task_name == "development":
            self.context.development_output = {"result": output_str}
        elif task_name == "security_review":
            self.context.extra["security_review_report"] = output_str
            filepath = self.output_manager.save_file(self.project_dir, "06_security_review_report.md", output_str)
        elif task_name == "testing":
            self.context.testing_report = output_str
            filepath = self.output_manager.save_testing_report(self.project_dir, output_str)
        elif task_name == "deployment":
            self.context.deployment_output = output_str
            filepath = self.output_manager.save_deployment_output(self.project_dir, output_str)
        
        if filepath:
            file_valid, file_msg = self.output_validator.validate_file_size(filepath)
            if not file_valid:
                self.logger.warning(f"文件大小警告: {file_msg}")
    
    def _check_security_issues(self, output: str) -> bool:
        output_lower = output.lower()
        keywords = ["漏洞", "风险", "问题", "不安全", "warning", "critical", "high", "需要修复", "建议修复"]
        return any(keyword in output_lower for keyword in keywords)
    
    def _check_test_failure(self, output: str) -> bool:
        output_lower = output.lower()
        keywords = ["失败", "未通过", "错误", "bug", "failure", "error", "not passed", "test failed"]
        return any(keyword in output_lower for keyword in keywords)
    
    def _execute_single_task(self, task_name: str, task, agent, retry_count: int = 0):
        self.state_tracker.start_task(task_name)
        self.metrics.start_task(task_name)
        self.logger.task_start(task_name)
        
        try:
            result = task.execute_sync()
            self.task_results[task_name] = result
            self._save_task_output(task_name, result)
            self.state_tracker.complete_task(task_name)
            self.metrics.end_task(task_name, success=True)
            self.logger.task_complete(task_name)
            return result, True
            
        except Exception as e:
            error_msg = str(e)
            self.state_tracker.fail_task(task_name, error_msg)
            self.metrics.end_task(task_name, success=False)
            self.logger.task_fail(task_name, error_msg)
            raise
    
    def run(self, user_idea: str):
        self.setup(user_idea)
        
        self.logger.info("=" * 60)
        self.logger.info("App 生产工作流开始")
        self.logger.info(f"用户想法: {user_idea}")
        self.logger.info("=" * 60)
        
        self.state_tracker.start_workflow()
        self.metrics.start_workflow()
        
        try:
            research_agent = create_research_agent(self.llm_config)
            product_agent = create_product_agent(self.llm_config)
            research_product_agent = create_research_product_agent(self.llm_config)
            design_agent = create_design_agent(self.llm_config)
            architecture_agent = create_architecture_agent(self.llm_config)
            development_agent = create_development_agent(self.llm_config)
            security_agent = create_security_agent(self.llm_config)
            testing_agent = create_testing_agent(self.llm_config)
            deployment_agent = create_deployment_agent(self.llm_config)
            
            research_task = Task(
                description=f"""基于用户想法进行市场调研：
                用户想法: {user_idea}
                
                请完成以下调研内容：
                1. 市场分析：分析该产品的市场规模、增长趋势
                2. 用户分析：目标用户画像、痛点需求
                3. 竞品分析：主要竞争对手分析
                4. 机会分析：市场机会和切入点
                5. 风险分析：潜在风险和应对建议
                
                请输出详细的调研报告。""",
                agent=research_agent,
                expected_output="详细的市场调研报告，包含市场分析、用户分析、竞品分析等内容"
            )
            
            product_task = Task(
                description=f"""基于用户想法和前面的调研报告编写PRD文档：
                用户想法: {user_idea}
                
                请参考前面的调研报告，编写完整的产品需求文档(PRD)，包含：
                1. 产品概述：产品定位、目标、愿景
                2. 用户故事：核心用户场景
                3. 功能需求：详细功能列表
                4. 非功能需求：性能、安全、可用性等
                5. 产品 roadmap：阶段规划
                
                请输出完整的PRD文档。""",
                agent=product_agent,
                expected_output="完整的产品需求文档(PRD)"
            )
            
            research_product_task = Task(
                description="""复核PRD文档，验证其可行性：
                
                请基于前面的调研报告和PRD文档，对PRD进行复核：
                1. 验证PRD中的需求是否符合市场调研结果
                2. 检查是否有遗漏的用户需求
                3. 评估技术可行性
                4. 提出改进建议
                
                请输出复核报告。""",
                agent=research_product_agent,
                expected_output="PRD复核报告，包含验证结果和改进建议"
            )
            
            design_task = Task(
                description="""基于PRD进行UI/UX设计：
                
                请根据PRD文档进行UI/UX设计：
                1. 信息架构设计
                2. 页面流程设计
                3. 关键页面UI设计描述
                4. 交互设计说明
                5. 设计规范建议
                
                请输出详细的设计文档。""",
                agent=design_agent,
                expected_output="详细的UI/UX设计文档"
            )
            
            architecture_task = Task(
                description="""基于设计文档进行技术架构设计：
                
                请根据设计文档进行技术架构设计：
                1. 系统架构设计
                2. 技术选型说明
                3. 数据库设计
                4. API接口设计
                5. 部署架构设计
                
                请输出详细的技术架构文档。""",
                agent=architecture_agent,
                expected_output="详细的技术架构文档"
            )
            
            development_task = Task(
                description="""基于架构文档进行代码开发：
                
                请根据技术架构文档进行代码实现：
                1. 项目结构搭建
                2. 后端代码实现
                3. 前端代码实现
                4. 配置文件
                5. 部署脚本
                
                请输出可运行的代码实现。""",
                agent=development_agent,
                expected_output="完整的代码实现，包含前端和后端代码"
            )
            
            security_review_task = Task(
                description="""对开发完成的系统进行安全审查：
                
                请对前面开发的系统进行全面的安全审查：
                1. 代码安全审计
                2. 依赖安全检查
                3. 敏感信息泄露检查
                4. 安全漏洞扫描
                5. 安全建议输出
                
                如果发现安全问题，请明确列出并提供修复建议。如果通过，请输出"安全审查通过"。""",
                agent=security_agent,
                expected_output="安全审查报告，包含发现的安全问题和修复建议"
            )
            
            testing_task = Task(
                description="""对开发完成的系统进行测试：
                
                请制定测试计划并执行测试：
                1. 测试计划
                2. 测试用例设计
                3. 功能测试
                4. 性能测试
                5. 测试报告
                
                如果测试未通过，请明确列出失败原因。如果通过，请输出"测试通过"。""",
                agent=testing_agent,
                expected_output="完整的测试报告"
            )
            
            deployment_task = Task(
                description="""制定部署方案并实现自动化部署：
                
                请制定部署方案并实现：
                1. 部署环境规划
                2. CI/CD流水线设计
                3. 容器化配置
                4. 监控和运维方案
                5. 部署文档
                
                请输出完整的部署方案。""",
                agent=deployment_agent,
                expected_output="完整的部署方案和文档"
            )
            
            self._execute_single_task("research", research_task, research_agent)
            self._execute_single_task("product", product_task, product_agent)
            self._execute_single_task("research_product", research_product_task, research_product_agent)
            self._execute_single_task("design", design_task, design_agent)
            self._execute_single_task("architecture", architecture_task, architecture_agent)
            
            retry_count = 0
            while retry_count < self.max_retries:
                self._execute_single_task("development", development_task, development_agent)
                
                security_result, _ = self._execute_single_task("security_review", security_review_task, security_agent)
                if self._check_security_issues(str(security_result)):
                    retry_count += 1
                    self.logger.warning(f"安全审查发现问题，返回开发阶段修复 (重试 {retry_count}/{self.max_retries})")
                    continue
                
                testing_result, _ = self._execute_single_task("testing", testing_task, testing_agent)
                if self._check_test_failure(str(testing_result)):
                    retry_count += 1
                    self.logger.warning(f"测试未通过，返回开发阶段修复 (重试 {retry_count}/{self.max_retries})")
                    continue
                
                break
            
            if retry_count >= self.max_retries:
                self.logger.error(f"已达到最大重试次数 {self.max_retries}，工作流终止")
                self.state_tracker.end_workflow()
                self.metrics.end_workflow()
                return False
            
            self._execute_single_task("deployment", deployment_task, deployment_agent)
            
            self.state_tracker.end_workflow()
            self.metrics.end_workflow()
            
            self.logger.info("=" * 60)
            self.logger.info("工作流执行完成！")
            self.logger.info(f"项目输出目录: {self.project_dir}")
            self.logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"工作流执行失败: {str(e)}")
            self.state_tracker.end_workflow()
            self.metrics.end_workflow()
            return False
