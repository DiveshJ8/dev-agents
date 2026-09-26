"""Developer tools registry and standard toolkit."""

from dev_agents.tools.base import BaseTool, tool
from dev_agents.tools.file_tools import read_file, write_file, list_directory, search_in_files
from dev_agents.tools.shell_tools import execute_command
from dev_agents.tools.git_tools import git_status, git_diff
from dev_agents.tools.colab_tools import (
    generate_colab_link,
    create_colab_notebook,
    package_app_for_colab,
    get_colab_local_runtime_command,
    open_colab_in_browser,
)

COLAB_TOOLS = [
    generate_colab_link,
    create_colab_notebook,
    package_app_for_colab,
    get_colab_local_runtime_command,
    open_colab_in_browser,
]

DEFAULT_DEV_TOOLS = [
    read_file,
    write_file,
    list_directory,
    search_in_files,
    execute_command,
    git_status,
    git_diff,
    *COLAB_TOOLS,
]

__all__ = [
    "BaseTool",
    "tool",
    "read_file",
    "write_file",
    "list_directory",
    "search_in_files",
    "execute_command",
    "git_status",
    "git_diff",
    "generate_colab_link",
    "create_colab_notebook",
    "package_app_for_colab",
    "get_colab_local_runtime_command",
    "open_colab_in_browser",
    "COLAB_TOOLS",
    "DEFAULT_DEV_TOOLS",
]
