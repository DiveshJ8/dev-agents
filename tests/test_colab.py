import json
import pytest
from pathlib import Path
from dev_agents.tools.colab_tools import (
    generate_colab_link,
    create_colab_notebook,
    package_app_for_colab,
    get_colab_local_runtime_command,
)
from dev_agents.subagents.colab_agent import ColabAgent
from dev_agents.mcp.colab_server import create_colab_mcp_server
from dev_agents.llm.mock_provider import MockLLMProvider


def test_generate_colab_link():
    link = generate_colab_link.run(
        github_repo="DiveshJ8/dev-agents",
        path="notebooks/test.ipynb",
        branch="main",
    )
    assert link == "https://colab.research.google.com/github/DiveshJ8/dev-agents/blob/main/notebooks/test.ipynb"

    gist_link = generate_colab_link.run(gist_id="abcd1234efgh")
    assert gist_link == "https://colab.research.google.com/gist/abcd1234efgh"

    drive_link = generate_colab_link.run(drive_id="1xyz_sample_id")
    assert drive_link == "https://colab.research.google.com/drive/1xyz_sample_id"


def test_create_colab_notebook(tmp_path: Path):
    nb_file = tmp_path / "test_colab.ipynb"
    cells = [
        {"type": "markdown", "content": "## Test Header"},
        {"type": "code", "content": "print('Hello from Colab')"},
    ]
    res = create_colab_notebook.run(
        output_path=str(nb_file),
        title="Colab Unit Test",
        cells_json=json.dumps(cells),
        accelerator="GPU",
        gpu_type="T4",
        github_repo="DiveshJ8/dev-agents",
    )
    assert "Successfully created Colab notebook" in res
    assert nb_file.exists()

    # Verify JSON structure
    data = json.loads(nb_file.read_text(encoding="utf-8"))
    assert data["metadata"]["accelerator"] == "GPU"
    assert data["metadata"]["colab"]["gpuType"] == "T4"
    assert len(data["cells"]) == 3  # Badge/Title cell + 2 custom cells


def test_package_app_for_colab(tmp_path: Path):
    app_file = tmp_path / "app.py"
    app_file.write_text("import streamlit as st\nst.write('App')", encoding="utf-8")

    out_nb = tmp_path / "app_colab.ipynb"
    res = package_app_for_colab.run(
        app_filepath=str(app_file),
        output_notebook_path=str(out_nb),
        app_type="streamlit",
        port=8501,
        github_repo="DiveshJ8/dev-agents",
    )
    assert "Successfully created Colab notebook" in res
    assert out_nb.exists()


def test_get_colab_local_runtime_command():
    info = get_colab_local_runtime_command.run(port=9000)
    assert "--NotebookApp.allow_origin='https://colab.research.google.com'" in info
    assert "--port=9000" in info


def test_colab_agent():
    agent = ColabAgent(llm=MockLLMProvider())
    assert agent.name == "Astrotrain"
    assert "generate_colab_link" in agent.tools
    assert "package_app_for_colab" in agent.tools

    resp = agent.run("Package a model inference app for Colab execution")
    assert "Google Colab" in resp or "Colab" in resp


def test_colab_mcp_server_initialization():
    server = create_colab_mcp_server()
    assert server.name == "colab-dev-agent"
