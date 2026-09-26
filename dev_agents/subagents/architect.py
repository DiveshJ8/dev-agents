from __future__ import annotations

from typing import List, Optional
from dev_agents.core.base_agent import BaseAgent
from dev_agents.tools.base import BaseTool
from dev_agents.tools.file_tools import read_file, list_directory, search_in_files


class ArchitectAgent(BaseAgent):
    """Specialized sub-agent for system design, component boundaries, and architecture specs."""

    def __init__(
        self,
        name: str = "SystemArchitect",
        tools: Optional[List[BaseTool]] = None,
        **kwargs,
    ):
        system_prompt = (
            "You are the System Architect. Your responsibilities are:\n"
            "1. Analyze technical requirements and system constraints.\n"
            "2. Define clean architectural boundaries, modular layers, and clear data models.\n"
            "3. Specify directory structures, class contracts, interfaces, and file responsibilities.\n"
            "4. Provide detailed, actionable technical specifications for developers to implement."
        )
        default_tools = tools or [read_file, list_directory, search_in_files]
        super().__init__(
            name=name,
            role="Software Architecture Specialist",
            system_prompt=system_prompt,
            tools=default_tools,
            **kwargs,
        )
