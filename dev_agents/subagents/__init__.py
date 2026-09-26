"""Specialized engineering subagents."""

from dev_agents.subagents.architect import ArchitectAgent
from dev_agents.subagents.coder import CoderAgent
from dev_agents.subagents.reviewer import ReviewerAgent
from dev_agents.subagents.tester import TesterAgent
from dev_agents.subagents.researcher import ResearcherAgent
from dev_agents.subagents.colab_agent import ColabAgent


# Decepticon Nomenclature Aliases
StarscreamAgent = ArchitectAgent
ShockwaveAgent = CoderAgent
ReflectorAgent = ReviewerAgent
BrawlAgent = TesterAgent
SoundwaveAgent = ResearcherAgent
AstrotrainAgent = ColabAgent


def create_default_agent_team(llm=None):
    """Creates a full team of specialized development sub-agents."""
    return [
        StarscreamAgent(llm=llm),
        ShockwaveAgent(llm=llm),
        ReflectorAgent(llm=llm),
        BrawlAgent(llm=llm),
        SoundwaveAgent(llm=llm),
        AstrotrainAgent(llm=llm),
    ]


__all__ = [
    "ArchitectAgent",
    "CoderAgent",
    "ReviewerAgent",
    "TesterAgent",
    "ResearcherAgent",
    "ColabAgent",
    "StarscreamAgent",
    "ShockwaveAgent",
    "ReflectorAgent",
    "BrawlAgent",
    "SoundwaveAgent",
    "AstrotrainAgent",
    "create_default_agent_team",
]
