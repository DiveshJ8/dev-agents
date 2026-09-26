from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from dev_agents.core.message import Message, ToolCall
from dev_agents.tools.base import BaseTool


class LLMResponse(BaseModel):
    content: str
    tool_calls: List[ToolCall] = Field(default_factory=list)
    model: str = "unknown"
    usage: Dict[str, Any] = Field(default_factory=dict)

    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0


class BaseLLMProvider(ABC):
    """Abstract interface for LLM backends."""

    def __init__(self, model_name: str, temperature: float = 0.2):
        self.model_name = model_name
        self.temperature = temperature

    @abstractmethod
    def generate(
        self,
        messages: List[Message],
        tools: Optional[List[BaseTool]] = None,
        system_instruction: Optional[str] = None,
    ) -> LLMResponse:
        """Generates a response from the LLM given conversation messages and optional tools."""
        pass
