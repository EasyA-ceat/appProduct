"""
LLMConfig 单元测试
"""
import os
import yaml
import pytest
from unittest.mock import patch, MagicMock
from src.llm_config import LLMConfig


class TestLLMConfig:

    def test_load_config_from_file(self, temp_dir, sample_agents_config):
        """测试从文件加载配置"""
        config_path = os.path.join(temp_dir, "agents.yaml")
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(sample_agents_config, f)
        
        llm_config = LLMConfig(config_path)
        
        assert llm_config.config == sample_agents_config

    def test_load_config_file_not_exists(self):
        """测试配置文件不存在时返回空配置"""
        llm_config = LLMConfig("/nonexistent/path.yaml")
        
        assert llm_config.config == {}

    def test_get_agent_config(self, temp_dir, sample_agents_config):
        """测试获取指定 Agent 配置"""
        config_path = os.path.join(temp_dir, "agents.yaml")
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(sample_agents_config, f)
        
        llm_config = LLMConfig(config_path)
        agent_config = llm_config.get_agent_config("research_agent")
        
        assert agent_config["llm_provider"] == "openai"
        assert agent_config["model"] == "gpt-4"

    def test_get_nonexistent_agent_config(self, temp_dir, sample_agents_config):
        """测试获取不存在的 Agent 配置"""
        config_path = os.path.join(temp_dir, "agents.yaml")
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(sample_agents_config, f)
        
        llm_config = LLMConfig(config_path)
        agent_config = llm_config.get_agent_config("nonexistent_agent")
        
        assert agent_config == {}

    def test_set_agent_config(self, temp_dir, sample_agents_config):
        """测试设置 Agent 配置"""
        config_path = os.path.join(temp_dir, "agents.yaml")
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(sample_agents_config, f)
        
        llm_config = LLMConfig(config_path)
        new_config = {
            "llm_provider": "anthropic",
            "model": "claude-3",
            "temperature": 0.5
        }
        
        llm_config.set_agent_config("research_agent", new_config)
        
        # 重新加载验证
        llm_config2 = LLMConfig(config_path)
        assert llm_config2.get_agent_config("research_agent")["llm_provider"] == "anthropic"

    @patch('src.llm_config.ChatOpenAI')
    def test_create_openai_llm(self, mock_chat_openai, temp_dir, sample_agents_config, env_setup):
        """测试创建 OpenAI LLM"""
        mock_instance = MagicMock()
        mock_chat_openai.return_value = mock_instance
        
        config_path = os.path.join(temp_dir, "agents.yaml")
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(sample_agents_config, f)
        
        llm_config = LLMConfig(config_path)
        llm = llm_config.create_llm("research_agent")
        
        mock_chat_openai.assert_called_once()
        assert llm == mock_instance

    @patch('src.llm_config.ChatAnthropic')
    def test_create_anthropic_llm(self, temp_dir, env_setup):
        """测试创建 Anthropic LLM"""
        mock_instance = MagicMock()
        mock_chat_anthropic = MagicMock(return_value=mock_instance)
        
        config_path = os.path.join(temp_dir, "agents.yaml")
        config_data = {
            "agents": {
                "test_agent": {
                    "llm_provider": "anthropic",
                    "model": "claude-3-opus",
                    "temperature": 0.7
                }
            }
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        llm_config = LLMConfig(config_path)
        
        with patch('src.llm_config.ChatAnthropic', mock_chat_anthropic):
            llm = llm_config.create_llm("test_agent")
        
        mock_chat_anthropic.assert_called_once()
        assert llm == mock_instance

    def test_create_unknown_provider_llm(self, temp_dir):
        """测试创建未知 Provider 时抛出异常"""
        config_path = os.path.join(temp_dir, "agents.yaml")
        config_data = {
            "agents": {
                "test_agent": {
                    "llm_provider": "unknown_provider",
                    "model": "test-model"
                }
            }
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        llm_config = LLMConfig(config_path)
        
        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            llm_config.create_llm("test_agent")
