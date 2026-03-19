"""Simple abstraction for LLM API client (OpenAI)."""

import os
from typing import Optional
from openai import OpenAI


class LLMClient:
    """Simple wrapper around OpenAI client with environment-based configuration."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7
    ):
        """
        Initialize LLM client.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model name (defaults to OPENAI_MODEL env var)
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4")
        self.temperature = temperature
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. "
                "Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )
        
        self.client = OpenAI(api_key=self.api_key)
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 1500) -> str:
        """
        Generate text from a prompt using the LLM.
        
        Args:
            prompt: The main prompt/message
            system_prompt: Optional system message for role-setting
            max_tokens: Maximum tokens in response
        
        Returns: Generated text response
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    def is_configured(self) -> bool:
        """Check if client is properly configured."""
        return bool(self.api_key)


def get_client() -> LLMClient:
    """Factory function to create an LLM client from environment variables."""
    try:
        return LLMClient()
    except ValueError as e:
        raise ValueError(str(e))
