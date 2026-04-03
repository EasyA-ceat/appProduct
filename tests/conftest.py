"""
测试配置和 fixtures
"""
import os
import tempfile
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def temp_dir():
    """创建临时目录 fixture"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_agents_config():
    """示例 Agent 配置"""
    return {
        "agents": {
            "research_agent": {
                "llm_provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000
            }
        }
    }


@pytest.fixture
def sample_output_config():
    """示例输出配置"""
    return {
        "output": {
            "max_total_size": "500MB",
            "max_file_size": "50MB",
            "allowed_file_types": [".py", ".md"],
            "output_dir": "./output",
            "logs_dir": "./logs"
        }
    }


@pytest.fixture
def mock_llm():
    """Mock LLM 实例"""
    mock = MagicMock()
    mock.invoke.return_value = "Mock LLM response"
    return mock


@pytest.fixture
def env_setup():
    """设置测试环境变量"""
    original_env = dict(os.environ)
    os.environ["OPENAI_API_KEY"] = "test-key-123"
    os.environ["OPENAI_API_BASE"] = "https://api.test.com"
    yield
    os.environ.clear()
    os.environ.update(original_env)
