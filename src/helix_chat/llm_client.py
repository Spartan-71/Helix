import asyncio
import litellm
from typing import List, Dict, Optional, AsyncGenerator
from .config import Config

class LLMClient:
    """LLM client using LiteLLM with Ollama support"""
    
    def __init__(self, config: Config):
        self.config = config
        self._setup_litellm()
    
    def _setup_litellm(self) -> None:
        """Setup LiteLLM configuration"""
        
        # Configure LiteLLM for Ollama
        import os
        
        # Set Ollama base URL for LiteLLM
        os.environ["OLLAMA_BASE_URL"] = self.config.ollama_base_url
        
        # Set other API keys if available
        for provider, key in self.config.api_keys.items():
            if key:
                if provider == "openai":
                    os.environ["OPENAI_API_KEY"] = key
                elif provider == "anthropic":
                    os.environ["ANTHROPIC_API_KEY"] = key
                elif provider == "google":
                    os.environ["GOOGLE_API_KEY"] = key
    
    async def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.config.ollama_base_url}/api/version", timeout=5) as response:
                    return response.status == 200
        except:
            try:
                # Fallback check using litellm
                test_response = await litellm.acompletion(
                    model="ollama/llama3",
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1,
                    api_base=self.config.ollama_base_url
                )
                return True
            except:
                return False
    
    async def get_response(self, messages: List[Dict[str, str]], model: str = None) -> str:
        """Get response from LLM"""
        
        model = model or self.config.default_model
        
        # Check Ollama connection for Ollama models
        if model.startswith("ollama/"):
            ollama_connected = await self.check_ollama_connection()
            if not ollama_connected:
                return f"❌ Cannot connect to Ollama at {self.config.ollama_base_url}\n\nMake sure Ollama is running:\n```bash\n# Start Ollama server\nollama serve\n\n# Pull llama3 model (if not already installed)\nollama pull llama3\n```"
        
        try:
            # Real LiteLLM call with Ollama
            response = await litellm.acompletion(
                model=model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                api_base=self.config.ollama_base_url if model.startswith("ollama/") else None
            )
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = str(e)
            
            # Provide helpful error messages for common Ollama issues
            if "Connection refused" in error_msg or "ConnectError" in error_msg:
                return f"❌ Cannot connect to Ollama server at {self.config.ollama_base_url}\n\nTry:\n1. Start Ollama: `ollama serve`\n2. Check if port 11434 is available\n3. Verify Ollama installation"
            elif "model not found" in error_msg.lower() or "404" in error_msg:
                return f"❌ Model 'llama3' not found in Ollama\n\nInstall it with:\n```bash\nollama pull llama3\n```\n\nOr try other available models:\n```bash\nollama list\n```"
            else:
                return f"❌ Error getting response: {error_msg}"
    
    async def stream_response(self, messages: List[Dict[str, str]], model: str = None) -> AsyncGenerator[str, None]:
        """Stream response from LLM"""
        model = model or self.config.default_model
        
        try:
            # For Ollama streaming
            response = await litellm.acompletion(
                model=model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                stream=True,
                api_base=self.config.ollama_base_url if model.startswith("ollama/") else None
            )
            
            # Stream the response
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"❌ Streaming error: {str(e)}"
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        models = [
            "ollama/llama3",
            "ollama/llama3:8b",
            "ollama/mistral",
            "ollama/phi3",
        ]
        
        # Add cloud models if API keys are available
        if self.config.api_keys.get("openai"):
            models.extend([
                "gpt-3.5-turbo",
                "gpt-4",
                "gpt-4-turbo"
            ])
        
        if self.config.api_keys.get("anthropic"):
            models.extend([
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ])
        
        return models
