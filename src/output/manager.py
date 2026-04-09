import os
from typing import Optional
from datetime import datetime


class OutputManager:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_project_dir(self, project_name: Optional[str] = None) -> str:
        if not project_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project_name = f"project_{timestamp}"
        else:
            project_name = os.path.basename(project_name)
        
        project_dir = os.path.join(self.output_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)
        return project_dir
    
    def save_file(self, project_dir: str, filename: str, content: str):
        filename = os.path.basename(filename)
        filepath = os.path.join(project_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def save_research_report(self, project_dir: str, content: str):
        return self.save_file(project_dir, "01_research_report.md", content)
    
    def save_prd_document(self, project_dir: str, content: str):
        return self.save_file(project_dir, "02_prd_document.md", content)
    
    def save_research_product_report(self, project_dir: str, content: str):
        return self.save_file(project_dir, "03_research_product_report.md", content)
    
    def save_design_document(self, project_dir: str, content: str):
        return self.save_file(project_dir, "04_design_document.md", content)
    
    def save_architecture_document(self, project_dir: str, content: str):
        return self.save_file(project_dir, "05_architecture_document.md", content)
    
    def save_testing_report(self, project_dir: str, content: str):
        return self.save_file(project_dir, "07_testing_report.md", content)
    
    def save_deployment_output(self, project_dir: str, content: str):
        return self.save_file(project_dir, "08_deployment_output.md", content)
