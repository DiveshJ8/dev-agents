from __future__ import annotations

from typing import List, Optional
from dev_agents.core.base_agent import BaseAgent
from dev_agents.tools.base import BaseTool
from dev_agents.tools.file_tools import read_file, search_in_files
from dev_agents.tools.git_tools import git_status, git_diff


class ReviewerAgent(BaseAgent):
    """Specialized sub-agent for code review, quality assurance, and security auditing."""

    def __init__(
        self,
        name: str = "CodeReviewer",
        tools: Optional[List[BaseTool]] = None,
        **kwargs,
    ):
        system_prompt = (
            "You are the Code Reviewer and Security QA Lead. Your responsibilities are:\n"
            "1. Audit code for logical bugs, syntax errors, and performance anti-patterns.\n"
            "2. Identify security vulnerabilities (injection, insecure deserialization, credentials leakage).\n"
            "3. Enforce code readability, naming conventions, and PEP 8 / language best practices.\n"
            "4. Provide constructive feedback with code diff suggestions and clear approval status."
        )
        default_tools = tools or [read_file, search_in_files, git_status, git_diff]
        super().__init__(
            name=name,
            role="Security & Quality Assurance Lead",
            system_prompt=system_prompt,
            tools=default_tools,
            **kwargs,
        )
