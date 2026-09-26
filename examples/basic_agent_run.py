"""Example: Creating and running a single specialized sub-agent."""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dev_agents.subagents.architect import ArchitectAgent
from dev_agents.llm.mock_provider import MockLLMProvider


def main():
    print("=== Basic Agent Execution ===")
    
    # 1. Initialize agent with mock LLM (or leave default for configured LLM)
    architect = ArchitectAgent(llm=MockLLMProvider())
    
    print(f"Agent Name: {architect.name}")
    print(f"Agent Role: {architect.role}")
    print(f"Available Tools: {list(architect.tools.keys())}")
    
    # 2. Run agent on a task
    prompt = "Design a scalable WebSocket connection manager for real-time notifications."
    print(f"\nTask: {prompt}\n")
    
    response = architect.run(prompt)
    print("Agent Response:")
    print("-" * 50)
    print(response)
    print("-" * 50)


if __name__ == "__main__":
    main()
