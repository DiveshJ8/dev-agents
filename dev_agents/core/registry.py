from __future__ import annotations

from typing import Dict, List, Optional
from dev_agents.core.base_agent import BaseAgent
from dev_agents.tools.base import BaseTool


class AgentRegistry:
    """Central registry for discovering, registering, and retrieving agents."""

    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        self._agents[agent.name.lower()] = agent

    def get(self, name: str) -> Optional[BaseAgent]:
        return self._agents.get(name.lower())

    def list_agents(self) -> List[BaseAgent]:
        return list(self._agents.values())

    def __contains__(self, name: str) -> bool:
        return name.lower() in self._agents


class ToolRegistry:
    """Central registry for developer tools."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def list_tools(self) -> List[BaseTool]:
        return list(self._tools.values())
