from __future__ import annotations

from typing import List, Optional
from dev_agents.core.base_agent import BaseAgent
from dev_agents.tools.base import BaseTool
from dev_agents.tools.file_tools import read_file, write_file, list_directory
from dev_agents.tools.shell_tools import execute_command
from dev_agents.tools.colab_tools import (
    generate_colab_link,
    create_colab_notebook,
    package_app_for_colab,
    get_colab_local_runtime_command,
    open_colab_in_browser,
)


class ColabAgent(BaseAgent):
    """
    Specialized sub-agent for Google Colab integration, cloud GPU execution,
    notebook generation, app packaging, and runtime bridging.
    """

    def __init__(
        self,
        name: str = "Astrotrain",
        tools: Optional[List[BaseTool]] = None,
        **kwargs,
    ):
        system_prompt = (
            "You are Astrotrain, the Google Colab & Cloud Execution Specialist. Your responsibilities are:\n"
            "1. Connect and interface with Google Colab (https://colab.research.google.com/).\n"
            "2. Convert Python applications (Streamlit, Gradio, FastAPI, PyTorch training scripts) into self-contained Colab executable notebooks.\n"
            "3. Configure GPU (T4, A100) or TPU hardware accelerators and environment dependencies for cloud training/inference.\n"
            "4. Configure public tunneling (e.g. Gradio share=True, localtunnel, ngrok) so apps running in Colab can be accessed over the web.\n"
            "5. Generate 1-click 'Open in Colab' links and launch them directly in the browser when requested.\n"
            "6. Guide and configure local runtime bridges (jupyter notebook with allow_origin for Colab)."
        )
        default_tools = tools or [
            generate_colab_link,
            create_colab_notebook,
            package_app_for_colab,
            get_colab_local_runtime_command,
            open_colab_in_browser,
            read_file,
            write_file,
            list_directory,
            execute_command,
        ]
        super().__init__(
            name=name,
            role="Google Colab & Cloud Execution Specialist",
            system_prompt=system_prompt,
            tools=default_tools,
            **kwargs,
        )
