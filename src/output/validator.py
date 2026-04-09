import os
from typing import List, Tuple


class OutputValidator:
    def __init__(self, max_total_size: int, max_file_size: int, allowed_file_types: List[str]):
        self.max_total_size = max_total_size
        self.max_file_size = max_file_size
        self.allowed_file_types = allowed_file_types
    
    def validate_file_type(self, filename: str) -> Tuple[bool, str]:
        file_ext = os.path.splitext(filename)[1].lower()
        for allowed_type in self.allowed_file_types:
            allowed_ext = allowed_type.lower()
            if file_ext == allowed_ext or filename == allowed_ext:
                return True, ""
        return False, f"文件类型不允许: {filename}"
    
    def validate_file_size(self, filepath: str) -> Tuple[bool, str]:
        if not os.path.exists(filepath):
            return True, ""
        
        file_size = os.path.getsize(filepath)
        if file_size > self.max_file_size:
            return False, f"文件大小超过限制: {filepath} ({file_size} bytes > {self.max_file_size} bytes)"
        return True, ""
    
    def validate_total_size(self, dir_path: str) -> Tuple[bool, str]:
        if not os.path.exists(dir_path):
            return True, ""
        
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        
        if total_size > self.max_total_size:
            return False, f"总空间超过限制: {total_size} bytes > {self.max_total_size} bytes"
        return True, ""
    
    def get_dir_size(self, dir_path: str) -> int:
        if not os.path.exists(dir_path):
            return 0
        
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        return total_size
