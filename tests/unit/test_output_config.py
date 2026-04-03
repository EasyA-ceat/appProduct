"""
OutputConfig 单元测试
"""
import os
import yaml
import pytest
from src.output_config import OutputConfig, OutputConfigManager


class TestOutputConfig:

    def test_default_config(self):
        """测试默认配置"""
        config = OutputConfig()
        
        assert config.max_total_size == "500MB"
        assert config.max_file_size == "50MB"
        assert ".py" in config.allowed_file_types
        assert config.output_dir == "./output"

    def test_custom_config(self):
        """测试自定义配置"""
        config = OutputConfig(
            max_total_size="1GB",
            max_file_size="100MB",
            output_dir="/custom/output"
        )
        
        assert config.max_total_size == "1GB"
        assert config.max_file_size == "100MB"
        assert config.output_dir == "/custom/output"


class TestOutputConfigManager:

    def test_load_config_from_file(self, temp_dir, sample_output_config):
        """测试从文件加载配置"""
        config_path = os.path.join(temp_dir, "output.yaml")
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(sample_output_config, f)
        
        manager = OutputConfigManager(config_path)
        
        assert manager.config.max_total_size == "500MB"
        assert manager.config.max_file_size == "50MB"

    def test_load_config_file_not_exists(self):
        """测试配置文件不存在时使用默认配置"""
        manager = OutputConfigManager("/nonexistent/path.yaml")
        
        assert manager.config.max_total_size == "500MB"

    def test_save_config(self, temp_dir):
        """测试保存配置"""
        config_path = os.path.join(temp_dir, "output.yaml")
        manager = OutputConfigManager(config_path)
        
        manager.config.max_total_size = "1TB"
        manager.config.max_file_size = "200MB"
        manager.save_config()
        
        # 重新加载验证
        manager2 = OutputConfigManager(config_path)
        assert manager2.config.max_total_size == "1TB"
        assert manager2.config.max_file_size == "200MB"

    def test_parse_size_mb(self):
        """测试解析 MB 单位"""
        manager = OutputConfigManager()
        
        assert manager.parse_size("500MB") == 500 * 1024 * 1024
        assert manager.parse_size("1MB") == 1024 * 1024

    def test_parse_size_kb(self):
        """测试解析 KB 单位"""
        manager = OutputConfigManager()
        
        assert manager.parse_size("1024KB") == 1024 * 1024
        assert manager.parse_size("1KB") == 1024

    def test_parse_size_gb(self):
        """测试解析 GB 单位"""
        manager = OutputConfigManager()
        
        assert manager.parse_size("1GB") == 1024 * 1024 * 1024

    def test_parse_size_plain_number(self):
        """测试解析纯数字"""
        manager = OutputConfigManager()
        
        assert manager.parse_size("1024") == 1024
        assert manager.parse_size("2048") == 2048

    def test_parse_size_case_insensitive(self):
        """测试大小写不敏感"""
        manager = OutputConfigManager()
        
        assert manager.parse_size("500mb") == 500 * 1024 * 1024
        assert manager.parse_size("100kB") == 100 * 1024

    def test_get_max_total_size_bytes(self):
        """测试获取最大总空间字节数"""
        manager = OutputConfigManager()
        manager.config.max_total_size = "100MB"
        
        assert manager.get_max_total_size_bytes() == 100 * 1024 * 1024

    def test_get_max_file_size_bytes(self):
        """测试获取最大单文件字节数"""
        manager = OutputConfigManager()
        manager.config.max_file_size = "10MB"
        
        assert manager.get_max_file_size_bytes() == 10 * 1024 * 1024
