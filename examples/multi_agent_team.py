"""Example: Running the complete multi-subagent engineering pipeline."""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dev_agents.core.orchestrator import Orchestrator
from dev_agents.subagents import create_default_agent_team
from dev_agents.tools import DEFAULT_DEV_TOOLS
from dev_agents.llm.mock_provider import MockLLMProvider


def main():
    print("=== Multi-Subagent Engineering Pipeline Demo ===")
    
    # 1. Setup mock LLM for rapid local execution
    mock_llm = MockLLMProvider()
    
    # 2. Instantiate team of subagents
    subagents = create_default_agent_team(llm=mock_llm)
    
    # 3. Instantiate Orchestrator (Lead Architect)
    workspace = "./workspace_demo"
    orchestrator = Orchestrator(
        name="LeadArchitect",
        subagents=subagents,
        tools=DEFAULT_DEV_TOOLS,
        llm=mock_llm,
        workspace_root=workspace,
    )
    
    goal = "Create a robust Token Bucket Rate Limiter with Redis backend and in-memory fallback"
    print(f"Goal: {goal}")
    print(f"Workspace Directory: {workspace}")
    print("\nExecuting autonomous development lifecycle...")
    
    def on_step(stage: str, msg: str):
        print(f"  [+] {stage}: {msg}")

    state = orchestrator.execute_development_pipeline(goal, on_step_update=on_step)
    
    print("\nPipeline Finished!")
    print(f"Total Artifacts Created: {len(state.artifacts)}")
    for name, artifact in state.artifacts.items():
        print(f"  - {name}: {len(artifact.content)} bytes ({artifact.created_by})")


if __name__ == "__main__":
    main()
