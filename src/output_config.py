import os
import yaml
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class OutputConfig:
    max_total_size: str = "500MB"
    max_file_size: str = "50MB"
    allowed_file_types: List[str] = None
    output_dir: str = "./output"
    logs_dir: str = "./logs"
    space_limit_strategy: str = "warn"
    compress_output: bool = False
    
    def __post_init__(self):
        if self.allowed_file_types is None:
            self.allowed_file_types = [
                ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css",
                ".json", ".yaml", ".yml", ".md", ".txt", ".gitignore",
                ".env.example", "Dockerfile", "docker-compose.yml",
                "package.json", "requirements.txt", "pyproject.toml",
                "setup.py", "README.md", "LICENSE"
            ]


class OutputConfigManager:
    def __init__(self, config_path: str = "config/output.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> OutputConfig:
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data and 'output' in data:
                    return OutputConfig(**data['output'])
        return OutputConfig()
    
    def save_config(self):
        data = {'output': self.config.__dict__}
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True)
    
    def parse_size(self, size_str: str) -> int:
        units = {'KB': 1024, 'MB': 1024*1024, 'GB': 1024*1024*1024}
        size_str = size_str.upper()
        for unit, multiplier in units.items():
            if size_str.endswith(unit):
                return int(float(size_str.replace(unit, '')) * multiplier)
        return int(size_str)
    
    def get_max_total_size_bytes(self) -> int:
        return self.parse_size(self.config.max_total_size)
    
    def get_max_file_size_bytes(self) -> int:
        return self.parse_size(self.config.max_file_size)
