"""Abstraction for multiple LLM API clients (OpenAI, Claude, Gemini)."""

import os
from typing import Optional, Union
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """Base class for LLM clients with unified interface."""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 1500) -> str:
        """Generate text from a prompt."""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if client is properly configured."""
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI GPT-4 client."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7
    ):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4")
        self.temperature = temperature
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. "
                "Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.provider = "openai"
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 1500) -> str:
        """Generate text using OpenAI API."""
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


class ClaudeClient(BaseLLMClient):
    """Anthropic Claude client."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7
    ):
        """Initialize Claude client."""
        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
        self.temperature = temperature
        
        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. "
                "Set ANTHROPIC_API_KEY environment variable or pass api_key parameter."
            )
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.provider = "claude"
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 1500) -> str:
        """Generate text using Claude API."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt or "",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    
    def is_configured(self) -> bool:
        """Check if client is properly configured."""
        return bool(self.api_key)


class GeminiClient(BaseLLMClient):
    """Google Gemini client."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7
    ):
        """Initialize Gemini client."""
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
        
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model = model or os.getenv("GEMINI_MODEL") or os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")
        self.temperature = temperature
        
        if not self.api_key:
            raise ValueError(
                "Google API key not found. "
                "Set GEMINI_API_KEY (or GOOGLE_API_KEY) environment variable or pass api_key parameter."
            )
        
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)
        self.provider = "gemini"
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 1500) -> str:
        """Generate text using Gemini API."""
        # Combine system and user prompt for Gemini
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        response = self.client.generate_content(
            full_prompt,
            generation_config={
                "max_output_tokens": max_tokens,
                "temperature": self.temperature
            }
        )
        
        return response.text
    
    def is_configured(self) -> bool:
        """Check if client is properly configured."""
        return bool(self.api_key)


def get_client(provider: Optional[str] = None, **kwargs) -> BaseLLMClient:
    """
    Factory function to get an LLM client.
    
    Args:
        provider: "openai", "claude", or "gemini" (defaults to LLM_PROVIDER env var or "openai")
        **kwargs: Additional arguments passed to client (api_key, model, temperature)
    
    Returns: Configured LLM client instance
    
    Raises: ValueError if provider not available or not configured
    """
    provider = provider or os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "openai":
        return OpenAIClient(**kwargs)
    elif provider == "claude":
        return ClaudeClient(**kwargs)
    elif provider == "gemini":
        return GeminiClient(**kwargs)
    else:
        raise ValueError(
            f"Unknown LLM provider: {provider}. "
            f"Supported providers: openai, claude, gemini"
        )


def list_providers() -> list[str]:
    """List all available LLM providers."""
    return ["openai", "claude", "gemini"]
