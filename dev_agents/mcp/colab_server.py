from __future__ import annotations

import argparse
import sys
from typing import Optional
from mcp.server.mcpserver import MCPServer

from dev_agents.tools.colab_tools import (
    generate_colab_link,
    create_colab_notebook,
    package_app_for_colab,
    get_colab_local_runtime_command,
    open_colab_in_browser,
)


def create_colab_mcp_server() -> MCPServer:
    """Creates and configures the Google Colab Model Context Protocol (MCP) server."""
    server = MCPServer(name="colab-dev-agent")

    @server.tool(
        name="colab_generate_link",
        description="Generate a 1-click Google Colab launch URL from a GitHub repo path, Gist ID, or Drive ID.",
    )
    def tool_generate_link(
        github_repo: str = "DiveshJ8/dev-agents",
        path: Optional[str] = None,
        branch: str = "main",
        gist_id: Optional[str] = None,
        drive_id: Optional[str] = None,
    ) -> str:
        return generate_colab_link(
            github_repo=github_repo,
            path=path,
            branch=branch,
            gist_id=gist_id,
            drive_id=drive_id,
        )

    @server.tool(
        name="colab_create_notebook",
        description="Create an .ipynb notebook optimized for Google Colab with GPU/TPU accelerator and Open-in-Colab badge.",
    )
    def tool_create_notebook(
        output_path: str,
        title: str,
        cells_json: str,
        accelerator: str = "GPU",
        gpu_type: str = "T4",
        github_repo: str = "DiveshJ8/dev-agents",
    ) -> str:
        return create_colab_notebook(
            output_path=output_path,
            title=title,
            cells_json=cells_json,
            accelerator=accelerator,
            gpu_type=gpu_type,
            github_repo=github_repo,
        )

    @server.tool(
        name="colab_package_app",
        description="Package a Python app (Streamlit, Gradio, FastAPI) into a runnable Colab notebook with public tunneling.",
    )
    def tool_package_app(
        app_filepath: str,
        output_notebook_path: str,
        app_type: str = "gradio",
        port: int = 7860,
        github_repo: str = "DiveshJ8/dev-agents",
    ) -> str:
        return package_app_for_colab(
            app_filepath=app_filepath,
            output_notebook_path=output_notebook_path,
            app_type=app_type,
            port=port,
            github_repo=github_repo,
        )

    @server.tool(
        name="colab_connect_local_runtime",
        description="Get exact command and instructions to connect Google Colab's web UI to a local Jupyter runtime.",
    )
    def tool_connect_local_runtime(port: int = 8888) -> str:
        return get_colab_local_runtime_command(port=port)

    @server.tool(
        name="colab_open_in_browser",
        description="Open a Colab notebook URL or GitHub repository file path directly in the web browser.",
    )
    def tool_open_in_browser(url_or_path: str, github_repo: str = "DiveshJ8/dev-agents") -> str:
        return open_colab_in_browser(url_or_path=url_or_path, github_repo=github_repo)

    return server


def run_colab_mcp_server() -> None:
    """Entry point for the Colab MCP Server executable."""
    parser = argparse.ArgumentParser(description="Google Colab MCP Server for Dev-Agents")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport protocol (default: stdio)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE or HTTP transport (default: 8000)",
    )
    args = parser.parse_args()

    server = create_colab_mcp_server()

    if args.transport == "stdio":
        # Windows encoding safety
        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8")
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        server.run(transport="stdio")
    else:
        server.run(transport=args.transport, port=args.port)


if __name__ == "__main__":
    run_colab_mcp_server()
