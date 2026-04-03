import json
import os
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskState:
    task_name: str
    status: TaskStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    error: Optional[str] = None


class StateTracker:
    def __init__(self, state_file: str = "logs/workflow_state.json"):
        self.state_file = state_file
        self.tasks: Dict[str, TaskState] = {}
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self._ensure_log_dir()
        self._load_state()
    
    def _ensure_log_dir(self):
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
    
    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.start_time = datetime.fromisoformat(data['start_time']) if data.get('start_time') else None
                    self.end_time = datetime.fromisoformat(data['end_time']) if data.get('end_time') else None
                    for task_name, task_data in data.get('tasks', {}).items():
                        self.tasks[task_name] = TaskState(
                            task_name=task_data['task_name'],
                            status=TaskStatus(task_data['status']),
                            start_time=datetime.fromisoformat(task_data['start_time']) if task_data.get('start_time') else None,
                            end_time=datetime.fromisoformat(task_data['end_time']) if task_data.get('end_time') else None,
                            duration_seconds=task_data.get('duration_seconds', 0.0),
                            error=task_data.get('error')
                        )
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                pass
    
    def _save_state(self):
        data = {
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'tasks': {
                task_name: {
                    'task_name': task.task_name,
                    'status': task.status.value,
                    'start_time': task.start_time.isoformat() if task.start_time else None,
                    'end_time': task.end_time.isoformat() if task.end_time else None,
                    'duration_seconds': task.duration_seconds,
                    'error': task.error
                }
                for task_name, task in self.tasks.items()
            }
        }
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def start_workflow(self):
        self.start_time = datetime.now()
        self._save_state()
    
    def end_workflow(self):
        self.end_time = datetime.now()
        self._save_state()
    
    def init_task(self, task_name: str):
        self.tasks[task_name] = TaskState(
            task_name=task_name,
            status=TaskStatus.PENDING
        )
        self._save_state()
    
    def start_task(self, task_name: str):
        if task_name not in self.tasks:
            self.init_task(task_name)
        self.tasks[task_name].status = TaskStatus.IN_PROGRESS
        self.tasks[task_name].start_time = datetime.now()
        self._save_state()
    
    def complete_task(self, task_name: str):
        if task_name in self.tasks:
            self.tasks[task_name].status = TaskStatus.COMPLETED
            self.tasks[task_name].end_time = datetime.now()
            if self.tasks[task_name].start_time:
                self.tasks[task_name].duration_seconds = (
                    self.tasks[task_name].end_time - self.tasks[task_name].start_time
                ).total_seconds()
            self._save_state()
    
    def fail_task(self, task_name: str, error: str):
        if task_name in self.tasks:
            self.tasks[task_name].status = TaskStatus.FAILED
            self.tasks[task_name].end_time = datetime.now()
            self.tasks[task_name].error = error
            if self.tasks[task_name].start_time:
                self.tasks[task_name].duration_seconds = (
                    self.tasks[task_name].end_time - self.tasks[task_name].start_time
                ).total_seconds()
            self._save_state()
    
    def get_progress(self) -> float:
        if not self.tasks:
            return 0.0
        completed = sum(1 for task in self.tasks.values() if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED])
        return (completed / len(self.tasks)) * 100
    
    def get_total_duration(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        elif self.start_time:
            return (datetime.now() - self.start_time).total_seconds()
        return 0.0
    
    def reset(self):
        self.tasks = {}
        self.start_time = None
        self.end_time = None
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
