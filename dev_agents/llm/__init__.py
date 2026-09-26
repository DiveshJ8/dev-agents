"""LLM providers and factory loader."""

import os
from typing import Optional
from dev_agents.llm.base import BaseLLMProvider, LLMResponse
from dev_agents.llm.mock_provider import MockLLMProvider
from dev_agents.llm.gemini_provider import GeminiProvider


def get_llm_provider(
    provider_name: Optional[str] = None,
    model_name: Optional[str] = None,
    **kwargs,
) -> BaseLLMProvider:
    """Factory helper to obtain an initialized LLM provider."""
    provider = provider_name or os.getenv("AGENT_MODE", "mock").lower()
    model = model_name or os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")

    if provider in ("gemini", "google"):
        return GeminiProvider(model_name=model, **kwargs)
    elif provider in ("mock", "test", "offline"):
        return MockLLMProvider(model_name=model, **kwargs)
    else:
        # Fallback to Mock if unspecified or unknown
        return MockLLMProvider(model_name=model, **kwargs)


__all__ = [
    "BaseLLMProvider",
    "LLMResponse",
    "GeminiProvider",
    "MockLLMProvider",
    "get_llm_provider",
]
