from __future__ import annotations

from typing import List, Optional
from dev_agents.core.base_agent import BaseAgent
from dev_agents.tools.base import BaseTool
from dev_agents.tools.file_tools import read_file, write_file, list_directory
from dev_agents.tools.shell_tools import execute_command


class TesterAgent(BaseAgent):
    """Specialized sub-agent for test generation, test execution, and regression verification."""

    def __init__(
        self,
        name: str = "Brawl",
        tools: Optional[List[BaseTool]] = None,
        **kwargs,
    ):
        system_prompt = (
            "You are Brawl, the Test Automation Engineer. Your responsibilities are:\n"
            "1. Generate thorough unit and integration test suites using pytest or equivalent frameworks.\n"
            "2. Cover boundary conditions, edge cases, error triggers, and valid workflows.\n"
            "3. Execute test runners via shell tools and inspect test failure traces.\n"
            "4. Report pass/fail statuses, coverage figures, and suggest fixes for broken tests."
        )
        default_tools = tools or [read_file, write_file, list_directory, execute_command]
        super().__init__(
            name=name,
            role="Verification & Test Automation Engineer",
            system_prompt=system_prompt,
            tools=default_tools,
            **kwargs,
        )
