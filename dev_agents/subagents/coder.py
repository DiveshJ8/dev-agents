from __future__ import annotations

from typing import List, Optional
from dev_agents.core.base_agent import BaseAgent
from dev_agents.tools.base import BaseTool
from dev_agents.tools.file_tools import read_file, write_file, list_directory, search_in_files
from dev_agents.tools.shell_tools import execute_command


class CoderAgent(BaseAgent):
    """Specialized sub-agent for implementation, code generation, refactoring, and file writing."""

    def __init__(
        self,
        name: str = "SeniorDeveloper",
        tools: Optional[List[BaseTool]] = None,
        **kwargs,
    ):
        system_prompt = (
            "You are a Senior Full-Stack Developer. Your responsibilities are:\n"
            "1. Implement clean, idiomatic, fully-typed, production-ready code.\n"
            "2. Write maintainable, self-documenting functions and classes.\n"
            "3. Handle edge cases, exceptions, and input validations gracefully.\n"
            "4. Use file tools to inspect existing source files and write updated code directly to disk."
        )
        default_tools = tools or [read_file, write_file, list_directory, search_in_files, execute_command]
        super().__init__(
            name=name,
            role="Full-Stack Implementation Engineer",
            system_prompt=system_prompt,
            tools=default_tools,
            **kwargs,
        )
