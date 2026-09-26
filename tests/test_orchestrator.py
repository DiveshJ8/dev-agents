import pytest
from pathlib import Path
from dev_agents.core.orchestrator import Orchestrator
from dev_agents.subagents import create_default_agent_team
from dev_agents.llm.mock_provider import MockLLMProvider
from dev_agents.tools.file_tools import read_file, write_file


def test_orchestrator_pipeline_execution(tmp_path: Path):
    mock_llm = MockLLMProvider()
    subagents = create_default_agent_team(llm=mock_llm)
    
    workspace_dir = str(tmp_path / "workspace")
    orchestrator = Orchestrator(
        name="LeadArchitect",
        subagents=subagents,
        tools=[read_file, write_file],
        llm=mock_llm,
        workspace_root=workspace_dir,
    )

    goal = "Build a JSON config parser with schema validation"
    state = orchestrator.execute_development_pipeline(goal)

    assert state.goal == goal
    assert "architecture_spec.md" in state.artifacts
    assert "implementation_notes.md" in state.artifacts
    assert "code_review.md" in state.artifacts
    assert "test_report.md" in state.artifacts
    assert "SUMMARY.md" in state.artifacts

    # Check files written to disk
    assert (tmp_path / "workspace" / "SUMMARY.md").exists()
    assert (tmp_path / "workspace" / "architecture_spec.md").exists()
