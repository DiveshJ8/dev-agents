"""Comprehensive live verification of all agents, sub-agents, and tools."""

import sys
import json
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dev_agents.core.orchestrator import Orchestrator
from dev_agents.subagents import (
    ArchitectAgent,
    CoderAgent,
    ReviewerAgent,
    TesterAgent,
    ResearcherAgent,
    ColabAgent,
    create_default_agent_team,
)
from dev_agents.tools import DEFAULT_DEV_TOOLS
from dev_agents.llm.mock_provider import MockLLMProvider


def test_individual_subagents():
    print("\n" + "=" * 60)
    print("PHASE 1: INDIVIDUAL SUB-AGENT VERIFICATION")
    print("=" * 60)

    mock_llm = MockLLMProvider()
    agents = [
        ("SystemArchitect", ArchitectAgent(llm=mock_llm), "Design high-performance WebSocket proxy"),
        ("SeniorDeveloper", CoderAgent(llm=mock_llm), "Implement WebSocket connection pool in Python"),
        ("CodeReviewer", ReviewerAgent(llm=mock_llm), "Review connection pool for resource leaks and concurrency bugs"),
        ("TestEngineer", TesterAgent(llm=mock_llm), "Write unit and stress tests for WebSocket pool"),
        ("TechResearcher", ResearcherAgent(llm=mock_llm), "Research best practices for ASGI WebSocket connection scaling"),
        ("ColabEngineer", ColabAgent(llm=mock_llm), "Package WebSocket monitoring dashboard for Google Colab GPU"),
    ]

    results = {}
    for name, agent, prompt in agents:
        print(f"\n[Testing Subagent: {name}]")
        print(f"  Role: {agent.role}")
        print(f"  Tools Attached: {len(agent.tools)} ({', '.join(agent.tools.keys())})")
        print(f"  Prompt: '{prompt}'")
        
        response = agent.run(prompt)
        assert len(response) > 0, f"Empty response from {name}"
        assert len(agent.memory) >= 2, f"Memory not updated in {name}"
        
        print(f"  Status: PASSED (Received {len(response)} characters)")
        first_line = response.strip().splitlines()[0]
        print(f"  Response Preview: {first_line[:80]}")
        results[name] = True

    return results


def test_colab_packaging_and_linking(workspace_dir: Path):
    print("\n" + "=" * 60)
    print("PHASE 2: GOOGLE COLAB APP PACKAGING & LINKING VERIFICATION")
    print("=" * 60)

    # 1. Create a dummy Python app
    app_file = workspace_dir / "test_app.py"
    app_file.write_text(
        "import gradio as gr\n"
        "demo = gr.Interface(lambda x: x.upper(), 'text', 'text')\n"
        "if __name__ == '__main__': demo.launch(share=True)\n",
        encoding="utf-8",
    )
    print(f"  [+] Created test app at: {app_file}")

    # 2. Package into Colab notebook using ColabEngineer
    colab_agent = ColabAgent(llm=MockLLMProvider())
    out_notebook = workspace_dir / "test_app_colab.ipynb"
    
    pkg_tool = colab_agent.tools["package_app_for_colab"]
    pkg_res = pkg_tool.run(
        app_filepath=str(app_file),
        output_notebook_path=str(out_notebook),
        app_type="gradio",
        github_repo="DiveshJ8/dev-agents",
    )
    assert out_notebook.exists(), "Colab notebook was not generated!"
    print(f"  [+] Colab Notebook Generated: {out_notebook} ({out_notebook.stat().st_size} bytes)")

    # 3. Verify Colab notebook content
    nb_content = json.loads(out_notebook.read_text(encoding="utf-8"))
    assert nb_content["metadata"]["accelerator"] == "GPU"
    assert "colab" in nb_content["metadata"]
    print(f"  [+] Colab GPU Metadata Verified: {nb_content['metadata']['accelerator']} ({nb_content['metadata']['colab'].get('gpuType')})")

    # 4. Generate 1-click Colab URL
    link_tool = colab_agent.tools["generate_colab_link"]
    colab_url = link_tool.run(
        github_repo="DiveshJ8/dev-agents",
        path="workspace/test_app_colab.ipynb",
    )
    assert colab_url.startswith("https://colab.research.google.com/github/DiveshJ8/dev-agents/blob/main/")
    print(f"  [+] 1-Click Launch URL: {colab_url}")
    print("  Status: PASSED")


def test_full_pipeline_orchestration(workspace_dir: Path):
    print("\n" + "=" * 60)
    print("PHASE 3: FULL MULTI-AGENT SUPERVISOR PIPELINE VERIFICATION")
    print("=" * 60)

    mock_llm = MockLLMProvider()
    team = create_default_agent_team(llm=mock_llm)
    pipeline_workspace = workspace_dir / "pipeline_run"
    
    orchestrator = Orchestrator(
        name="LeadArchitect",
        subagents=team,
        tools=DEFAULT_DEV_TOOLS,
        llm=mock_llm,
        workspace_root=str(pipeline_workspace),
    )

    goal = "Build a real-time event streaming pipeline with in-memory caching and Colab analytics"
    print(f"  Supervisor: {orchestrator.name} ({orchestrator.role})")
    print(f"  Subagents in Team: {len(orchestrator.subagents)}")
    print(f"  Goal: '{goal}'")
    print(f"  Workspace: {pipeline_workspace}\n")

    steps_executed = []
    def track_step(stage: str, msg: str):
        steps_executed.append(stage)
        print(f"    >> [{stage}] {msg}")

    state = orchestrator.execute_development_pipeline(goal, on_step_update=track_step)

    # Verifications
    expected_artifacts = [
        "architecture_spec.md",
        "implementation_notes.md",
        "code_review.md",
        "test_report.md",
        "SUMMARY.md",
    ]

    print("\n  Verifying Artifact Generation:")
    for art_name in expected_artifacts:
        assert art_name in state.artifacts, f"Missing artifact: {art_name}"
        file_path = pipeline_workspace / art_name
        assert file_path.exists(), f"File not persisted: {file_path}"
        size = file_path.stat().st_size
        print(f"    * {art_name} -> {size} bytes [EXISTS & PERSISTED]")

    print(f"\n  Pipeline Stages Executed: {len(steps_executed)} stages")
    print("  Status: PASSED")


def main():
    print("############################################################")
    print("###      DEV-AGENTS SYSTEM & SUB-AGENTS VERIFICATION     ###")
    print("############################################################")

    tmp_workspace = Path("./workspace_test_run")
    tmp_workspace.mkdir(parents=True, exist_ok=True)

    try:
        test_individual_subagents()
        test_colab_packaging_and_linking(tmp_workspace)
        test_full_pipeline_orchestration(tmp_workspace)

        print("\n" + "#" * 60)
        print("### ALL 3 VERIFICATION PHASES COMPLETED WITH 100% SUCCESS! ###")
        print("#" * 60)
    finally:
        # Cleanup temporary test files
        import shutil
        shutil.rmtree(tmp_workspace, ignore_errors=True)


if __name__ == "__main__":
    main()
