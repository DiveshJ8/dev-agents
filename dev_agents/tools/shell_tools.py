from __future__ import annotations

import subprocess
import sys
from typing import Optional
from dev_agents.tools.base import tool


@tool(
    name="execute_command",
    description="Execute a shell command with a timeout and return stdout and stderr.",
)
def execute_command(command: str, cwd: Optional[str] = None, timeout: int = 30) -> str:
    """Executes a command safely and returns combined output."""
    try:
        is_windows = sys.platform == "win32"
        res = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = []
        if res.stdout:
            output.append(f"STDOUT:\n{res.stdout.strip()}")
        if res.stderr:
            output.append(f"STDERR:\n{res.stderr.strip()}")
        output.append(f"Exit Code: {res.returncode}")
        return "\n\n".join(output) if output else "Command executed with no output."
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"
