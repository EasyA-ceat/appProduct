from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class WorkflowContext:
    user_idea: str = ""
    research_report: str = ""
    prd_document: str = ""
    research_product_report: str = ""
    design_document: str = ""
    architecture_document: str = ""
    development_output: Dict[str, Any] = field(default_factory=dict)
    testing_report: str = ""
    deployment_output: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)
    
    def set(self, key: str, value: Any):
        setattr(self, key, value)
