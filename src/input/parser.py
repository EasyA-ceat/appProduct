import os
from typing import Optional


class IdeaParser:
    @staticmethod
    def parse_from_cli(idea: Optional[str] = None, idea_file: Optional[str] = None) -> str:
        if idea:
            return idea.strip()
        
        if idea_file and os.path.exists(idea_file):
            with open(idea_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        
        return IdeaParser._interactive_input()
    
    @staticmethod
    def _interactive_input() -> str:
        print("\n请输入您的APP想法：")
        idea = input().strip()
        while not idea:
            print("想法不能为空，请重新输入：")
            idea = input().strip()
        return idea
