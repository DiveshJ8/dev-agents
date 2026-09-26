from __future__ import annotations

from typing import List, Optional
from dev_agents.core.base_agent import BaseAgent
from dev_agents.tools.base import BaseTool
from dev_agents.tools.file_tools import read_file, list_directory, search_in_files


class ResearcherAgent(BaseAgent):
    """Specialized sub-agent for technical research, documentation, and codebase analysis."""

    def __init__(
        self,
        name: str = "TechResearcher",
        tools: Optional[List[BaseTool]] = None,
        **kwargs,
    ):
        system_prompt = (
            "You are the Technical Researcher & Documentation Specialist. Your responsibilities are:\n"
            "1. Deeply analyze existing codebases, dependency configurations, and third-party APIs.\n"
            "2. Identify technical tradeoffs between architectural approaches and libraries.\n"
            "3. Draft clear, comprehensive developer documentation, API references, and quickstarts.\n"
            "4. Provide synthesized technical answers to engineering questions."
        )
        default_tools = tools or [read_file, list_directory, search_in_files]
        super().__init__(
            name=name,
            role="Documentation & Technical Intelligence",
            system_prompt=system_prompt,
            tools=default_tools,
            **kwargs,
        )
