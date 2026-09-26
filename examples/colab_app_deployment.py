"""Example: Packaging an application for Google Colab and generating 1-click execution links."""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dev_agents.subagents.colab_agent import ColabAgent
from dev_agents.tools.colab_tools import (
    package_app_for_colab,
    generate_colab_link,
    get_colab_local_runtime_command,
)
from dev_agents.llm.mock_provider import MockLLMProvider


def main():
    print("=== Google Colab App Packaging & Execution Demo ===\n")

    # 1. Create a sample Gradio app script for testing
    workspace_dir = Path("./workspace_demo")
    workspace_dir.mkdir(parents=True, exist_ok=True)
    sample_app = workspace_dir / "sentiment_app.py"
    sample_app.write_text(
        'import gradio as gr\n\n'
        'def analyze_sentiment(text):\n'
        '    return f"Input: {text} | Sentiment: Positive (Cloud GPU Accelerated)"\n\n'
        'demo = gr.Interface(fn=analyze_sentiment, inputs="text", outputs="text")\n'
        'if __name__ == "__main__":\n'
        '    demo.launch(share=True)\n',
        encoding="utf-8",
    )
    print(f"[1] Created sample application at: {sample_app}")

    # 2. Package into a Colab notebook
    output_notebook = workspace_dir / "sentiment_colab.ipynb"
    result = package_app_for_colab.run(
        app_filepath=str(sample_app),
        output_notebook_path=str(output_notebook),
        app_type="gradio",
        github_repo="DiveshJ8/dev-agents",
    )
    print(f"[2] Packaging Result:\n{result}\n")

    # 3. Direct 1-Click Launch Link
    colab_url = generate_colab_link.run(
        github_repo="DiveshJ8/dev-agents",
        path="notebooks/sentiment_colab.ipynb",
    )
    print(f"[3] Direct 1-Click Colab URL:\n    {colab_url}\n")

    # 4. Colab Local Runtime Command
    runtime_info = get_colab_local_runtime_command.run(port=8888)
    print(f"[4] Local Runtime Bridge:\n{runtime_info}\n")

    # 5. Dispatch task to the specialized Colab subagent
    colab_agent = ColabAgent(llm=MockLLMProvider())
    print(f"[5] Dispatching task to {colab_agent.name} ({colab_agent.role})...")
    agent_response = colab_agent.run(
        "Package sentiment_app.py to run on Colab GPU with a public web tunnel"
    )
    print(f"Colab Agent Response:\n{agent_response}")


if __name__ == "__main__":
    main()
