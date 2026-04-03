import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

load_dotenv()


class LLMConfig:
    def __init__(self, config_path: str = "config/agents.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def save_config(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True)
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        return self.config.get('agents', {}).get(agent_name, {})
    
    def set_agent_config(self, agent_name: str, config: Dict[str, Any]):
        if 'agents' not in self.config:
            self.config['agents'] = {}
        self.config['agents'][agent_name] = config
        self.save_config()
    
    def create_llm(self, agent_name: str):
        agent_config = self.get_agent_config(agent_name)
        provider = agent_config.get('llm_provider', 'openai')
        model = agent_config.get('model', 'gpt-4')
        temperature = agent_config.get('temperature', 0.7)
        max_tokens = agent_config.get('max_tokens', 2000)
        
        if provider == 'openai':
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=os.getenv('OPENAI_API_KEY'),
                base_url=os.getenv('OPENAI_API_BASE')
            )
        elif provider == 'anthropic':
            return ChatAnthropic(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=os.getenv('ANTHROPIC_API_KEY')
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
