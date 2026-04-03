import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class TaskMetrics:
    task_name: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_seconds: float = 0.0
    token_usage: int = 0
    success: bool = True


class MetricsCollector:
    def __init__(self, metrics_file: str = "logs/metrics.json"):
        self.metrics_file = metrics_file
        self.task_metrics: Dict[str, TaskMetrics] = {}
        self.workflow_start_time: Optional[datetime] = None
        self.workflow_end_time: Optional[datetime] = None
        self.total_tokens: int = 0
        self._ensure_log_dir()
        self._load_metrics()
    
    def _ensure_log_dir(self):
        os.makedirs(os.path.dirname(self.metrics_file), exist_ok=True)
    
    def _load_metrics(self):
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.workflow_start_time = datetime.fromisoformat(data['workflow_start_time']) if data.get('workflow_start_time') else None
                    self.workflow_end_time = datetime.fromisoformat(data['workflow_end_time']) if data.get('workflow_end_time') else None
                    self.total_tokens = data.get('total_tokens', 0)
                    for task_name, task_data in data.get('task_metrics', {}).items():
                        self.task_metrics[task_name] = TaskMetrics(**task_data)
            except:
                pass
    
    def _save_metrics(self):
        data = {
            'workflow_start_time': self.workflow_start_time.isoformat() if self.workflow_start_time else None,
            'workflow_end_time': self.workflow_end_time.isoformat() if self.workflow_end_time else None,
            'total_tokens': self.total_tokens,
            'total_duration_seconds': self.get_total_duration(),
            'success_rate': self.get_success_rate(),
            'task_metrics': {
                task_name: asdict(task)
                for task_name, task in self.task_metrics.items()
            }
        }
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def start_workflow(self):
        self.workflow_start_time = datetime.now()
        self._save_metrics()
    
    def end_workflow(self):
        self.workflow_end_time = datetime.now()
        self._save_metrics()
    
    def start_task(self, task_name: str):
        self.task_metrics[task_name] = TaskMetrics(
            task_name=task_name,
            start_time=datetime.now().isoformat()
        )
        self._save_metrics()
    
    def end_task(self, task_name: str, success: bool = True, token_usage: int = 0):
        if task_name in self.task_metrics:
            self.task_metrics[task_name].end_time = datetime.now().isoformat()
            self.task_metrics[task_name].success = success
            self.task_metrics[task_name].token_usage = token_usage
            
            if self.task_metrics[task_name].start_time:
                start = datetime.fromisoformat(self.task_metrics[task_name].start_time)
                end = datetime.fromisoformat(self.task_metrics[task_name].end_time)
                self.task_metrics[task_name].duration_seconds = (end - start).total_seconds()
            
            self.total_tokens += token_usage
            self._save_metrics()
    
    def get_total_duration(self) -> float:
        if self.workflow_start_time and self.workflow_end_time:
            return (self.workflow_end_time - self.workflow_start_time).total_seconds()
        elif self.workflow_start_time:
            return (datetime.now() - self.workflow_start_time).total_seconds()
        return 0.0
    
    def get_success_rate(self) -> float:
        if not self.task_metrics:
            return 100.0
        successful = sum(1 for task in self.task_metrics.values() if task.success)
        return (successful / len(self.task_metrics)) * 100
    
    def get_summary(self) -> Dict[str, Any]:
        return {
            'total_duration_seconds': self.get_total_duration(),
            'total_tokens': self.total_tokens,
            'success_rate': self.get_success_rate(),
            'task_count': len(self.task_metrics),
            'task_metrics': {
                task_name: asdict(task)
                for task_name, task in self.task_metrics.items()
            }
        }
    
    def reset(self):
        self.task_metrics = {}
        self.workflow_start_time = None
        self.workflow_end_time = None
        self.total_tokens = 0
        if os.path.exists(self.metrics_file):
            os.remove(self.metrics_file)
