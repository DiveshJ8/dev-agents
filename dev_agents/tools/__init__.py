"""Developer tools registry and standard toolkit."""

from dev_agents.tools.base import BaseTool, tool
from dev_agents.tools.file_tools import read_file, write_file, list_directory, search_in_files
from dev_agents.tools.shell_tools import execute_command
from dev_agents.tools.git_tools import git_status, git_diff

DEFAULT_DEV_TOOLS = [
    read_file,
    write_file,
    list_directory,
    search_in_files,
    execute_command,
    git_status,
    git_diff,
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
    "DEFAULT_DEV_TOOLS",
]
