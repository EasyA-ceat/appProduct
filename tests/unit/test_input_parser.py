"""
IdeaParser 单元测试
"""
import os
import pytest
from unittest.mock import patch
from src.input.parser import IdeaParser


class TestIdeaParser:

    def test_parse_from_cli_direct_input(self):
        """测试从 CLI 参数直接解析"""
        idea = IdeaParser.parse_from_cli(idea="我想做一个待办事项APP", idea_file=None)
        
        assert idea == "我想做一个待办事项APP"

    def test_parse_from_cli_with_file(self, temp_dir):
        """测试从文件解析"""
        idea_file = os.path.join(temp_dir, "idea.txt")
        with open(idea_file, 'w', encoding='utf-8') as f:
            f.write("我想做一个记账APP")
        
        idea = IdeaParser.parse_from_cli(idea=None, idea_file=idea_file)
        
        assert idea == "我想做一个记账APP"

    def test_parse_from_cli_file_not_exists(self):
        """测试文件不存在时的处理（应进入交互模式）"""
        with patch.object(IdeaParser, '_interactive_input', return_value="交互式输入"):
            idea = IdeaParser.parse_from_cli(idea=None, idea_file="/nonexistent/file.txt")
        
        assert idea == "交互式输入"

    def test_parse_from_cli_both_none(self):
        """测试 idea 和 idea_file 都为 None 时进入交互模式"""
        with patch.object(IdeaParser, '_interactive_input', return_value="默认想法"):
            idea = IdeaParser.parse_from_cli(idea=None, idea_file=None)
        
        assert idea == "默认想法"

    def test_parse_from_cli_trim_whitespace(self):
        """测试去除首尾空格"""
        idea = IdeaParser.parse_from_cli(idea="  带空格的想法  ", idea_file=None)
        
        assert idea == "带空格的想法"

    @patch('builtins.input')
    def test_interactive_input(self, mock_input):
        """测试交互式输入"""
        mock_input.return_value = "交互式想法"
        
        idea = IdeaParser._interactive_input()
        
        assert idea == "交互式想法"

    @patch('builtins.input')
    def test_interactive_input_retry_on_empty(self, mock_input):
        """测试空输入时重试"""
        mock_input.side_effect = ["", "   ", "最终想法"]
        
        idea = IdeaParser._interactive_input()
        
        assert idea == "最终想法"
        assert mock_input.call_count == 3
