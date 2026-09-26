"""Specialized engineering subagents."""

from dev_agents.subagents.architect import ArchitectAgent
from dev_agents.subagents.coder import CoderAgent
from dev_agents.subagents.reviewer import ReviewerAgent
from dev_agents.subagents.tester import TesterAgent
from dev_agents.subagents.researcher import ResearcherAgent
from dev_agents.subagents.colab_agent import ColabAgent


def create_default_agent_team(llm=None):
    """Creates a full team of specialized development sub-agents."""
    return [
        ArchitectAgent(llm=llm),
        CoderAgent(llm=llm),
        ReviewerAgent(llm=llm),
        TesterAgent(llm=llm),
        ResearcherAgent(llm=llm),
        ColabAgent(llm=llm),
    ]


__all__ = [
    "ArchitectAgent",
    "CoderAgent",
    "ReviewerAgent",
    "TesterAgent",
    "ResearcherAgent",
    "ColabAgent",
    "create_default_agent_team",
]
