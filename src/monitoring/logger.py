import logging
import os
from datetime import datetime
from typing import Optional


class WorkflowLogger:
    def __init__(self, log_dir: str = "logs", log_file: str = "workflow.log"):
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, log_file)
        self._ensure_log_dir()
        self._setup_logger()
    
    def _ensure_log_dir(self):
        os.makedirs(self.log_dir, exist_ok=True)
    
    def _setup_logger(self):
        self.logger = logging.getLogger("app_workflow")
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s  %(message)s',
                datefmt='%H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def agent_start(self, agent_name: str):
        self.info(f"{agent_name} 开始执行...")
    
    def agent_complete(self, agent_name: str, duration: float):
        self.info(f"{agent_name} 完成，耗时: {duration:.1f}s")
    
    def task_start(self, task_name: str):
        self.info(f"Task '{task_name}' 开始...")
    
    def task_complete(self, task_name: str):
        self.info(f"Task '{task_name}' 完成")
    
    def task_fail(self, task_name: str, error: str):
        self.error(f"Task '{task_name}' 失败: {error}")
    
    def get_recent_logs(self, tail: int = 50) -> list:
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return lines[-tail:] if tail > 0 else lines
        return []
