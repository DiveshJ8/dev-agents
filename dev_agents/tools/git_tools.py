from __future__ import annotations

import subprocess
from typing import Optional
from dev_agents.tools.base import tool


@tool(
    name="git_status",
    description="Get current Git status of the working repository.",
)
def git_status(repo_dir: str = ".") -> str:
    try:
        res = subprocess.run(
            ["git", "status", "--short"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=15,
        )
        if res.returncode != 0:
            return f"Git error: {res.stderr.strip()}"
        return res.stdout.strip() or "Working tree is clean."
    except Exception as e:
        return f"Error executing git status: {str(e)}"


@tool(
    name="git_diff",
    description="Inspect git diff changes in the repository.",
)
def git_diff(repo_dir: str = ".", cached: bool = False) -> str:
    try:
        args = ["git", "diff"]
        if cached:
            args.append("--cached")
        res = subprocess.run(
            args,
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=15,
        )
        if res.returncode != 0:
            return f"Git error: {res.stderr.strip()}"
        diff_text = res.stdout.strip()
        if not diff_text:
            return "No changes detected."
        # Truncate if diff is very long
        if len(diff_text) > 4000:
            return diff_text[:4000] + "\n... (diff truncated)"
        return diff_text
    except Exception as e:
        return f"Error executing git diff: {str(e)}"
