import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Config:
    """Application configuration"""
    default_model: str = "ollama/llama3"
    ollama_base_url: str = "http://localhost:11434"
    max_tokens: int = 2000
    temperature: float = 0.7
    api_keys: Dict[str, str] = None
    
    def __post_init__(self):
        if self.api_keys is None:
            self.api_keys = {}
        
        # Load API keys from environment
        self.api_keys.update({
            "openai": os.getenv("OPENAI_API_KEY", ""),
            "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
            "google": os.getenv("GOOGLE_API_KEY", ""),
        })
        
        # Override Ollama base URL if set in environment
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", self.ollama_base_url)

def load_config() -> Config:
    """Load configuration from environment and defaults"""
    return Config()