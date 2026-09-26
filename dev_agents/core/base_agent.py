from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from dev_agents.core.message import Message, MessageRole, ToolCall, ToolResult
from dev_agents.llm.base import BaseLLMProvider
from dev_agents.llm import get_llm_provider
from dev_agents.tools.base import BaseTool

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base autonomous agent class providing lifecycle, memory, and tool execution."""

    def __init__(
        self,
        name: str,
        role: str,
        system_prompt: str,
        tools: Optional[List[BaseTool]] = None,
        llm: Optional[BaseLLMProvider] = None,
        max_iterations: int = 10,
    ):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt.strip()
        self.llm = llm or get_llm_provider()
        self.tools: Dict[str, BaseTool] = {}
        if tools:
            for t in tools:
                self.add_tool(t)
        self.memory: List[Message] = []
        self.max_iterations = max_iterations

    def add_tool(self, tool: BaseTool) -> None:
        self.tools[tool.name] = tool

    def reset_memory(self) -> None:
        self.memory.clear()

    def execute_tool(self, tool_call: ToolCall) -> ToolResult:
        tool = self.tools.get(tool_call.name)
        if not tool:
            return ToolResult(
                tool_call_id=tool_call.id,
                name=tool_call.name,
                content=f"Error: Tool '{tool_call.name}' not found on agent '{self.name}'.",
                is_error=True,
            )

        try:
            result = tool.run(**tool_call.arguments)
            return ToolResult(
                tool_call_id=tool_call.id,
                name=tool_call.name,
                content=str(result),
                is_error=False,
            )
        except Exception as e:
            return ToolResult(
                tool_call_id=tool_call.id,
                name=tool_call.name,
                content=f"Tool execution exception: {str(e)}",
                is_error=True,
            )

    def run(self, prompt: str) -> str:
        """Runs the agent with the user prompt until goal is satisfied or max iterations reached."""
        user_message = Message(
            role=MessageRole.USER,
            content=prompt,
            sender="user",
            recipient=self.name,
        )
        self.memory.append(user_message)

        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1

            # Generate next agent action
            response = self.llm.generate(
                messages=self.memory,
                tools=list(self.tools.values()) if self.tools else None,
                system_instruction=f"Role: {self.role}\n{self.system_prompt}",
            )

            # If agent requested tool execution
            if response.has_tool_calls:
                assistant_msg = Message(
                    role=MessageRole.ASSISTANT,
                    content=response.content or "Calling tools...",
                    sender=self.name,
                    tool_calls=response.tool_calls,
                )
                self.memory.append(assistant_msg)

                tool_results: List[ToolResult] = []
                for tool_call in response.tool_calls:
                    res = self.execute_tool(tool_call)
                    tool_results.append(res)

                # Append tool results back into conversation
                tool_msg = Message(
                    role=MessageRole.TOOL,
                    content="\n\n".join(f"[{r.name}]: {r.content}" for r in tool_results),
                    sender="system",
                    tool_results=tool_results,
                )
                self.memory.append(tool_msg)
            else:
                # Agent completed response
                final_msg = Message(
                    role=MessageRole.ASSISTANT,
                    content=response.content,
                    sender=self.name,
                )
                self.memory.append(final_msg)
                return response.content

        return "Agent reached maximum iteration limit before completing the task."
