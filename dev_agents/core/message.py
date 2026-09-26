from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    SUBAGENT = "subagent"


class ToolCall(BaseModel):
    id: str = Field(description="Unique tool call invocation ID")
    name: str = Field(description="Name of the tool to invoke")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Tool invocation parameters")


class ToolResult(BaseModel):
    tool_call_id: str = Field(description="ID of the tool call being answered")
    name: str = Field(description="Name of the tool that executed")
    content: str = Field(description="Execution result string or serialized data")
    is_error: bool = Field(default=False, description="Whether the tool execution failed")


class Message(BaseModel):
    role: MessageRole
    content: str
    sender: str = "user"
    recipient: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_results: Optional[List[ToolResult]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
