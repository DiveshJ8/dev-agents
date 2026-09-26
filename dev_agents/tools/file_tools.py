from __future__ import annotations

import os
from pathlib import Path
from typing import List
from dev_agents.tools.base import tool


@tool(
    name="read_file",
    description="Read the text content of a file at the given filepath.",
)
def read_file(filepath: str) -> str:
    path = Path(filepath)
    if not path.exists():
        return f"Error: File '{filepath}' does not exist."
    if not path.is_file():
        return f"Error: '{filepath}' is not a regular file."
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading '{filepath}': {str(e)}"


@tool(
    name="write_file",
    description="Write text content to a file at filepath. Creates directories if necessary.",
)
def write_file(filepath: str, content: str, overwrite: bool = True) -> str:
    path = Path(filepath)
    if path.exists() and not overwrite:
        return f"Error: File '{filepath}' already exists and overwrite is set to False."
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Successfully wrote {len(content)} characters to '{filepath}'."
    except Exception as e:
        return f"Error writing to '{filepath}': {str(e)}"


@tool(
    name="list_directory",
    description="List files and directories in a directory with optional recursive glob pattern.",
)
def list_directory(directory: str = ".", pattern: str = "*", recursive: bool = False) -> str:
    dir_path = Path(directory)
    if not dir_path.exists():
        return f"Error: Directory '{directory}' does not exist."
    try:
        if recursive:
            entries = list(dir_path.rglob(pattern))
        else:
            entries = list(dir_path.glob(pattern))
        
        # Limit to 100 entries for display safety
        lines: List[str] = []
        for entry in entries[:100]:
            kind = "DIR " if entry.is_dir() else "FILE"
            rel = entry.relative_to(dir_path) if entry != dir_path else entry.name
            lines.append(f"[{kind}] {rel}")

        result = "\n".join(lines)
        if len(entries) > 100:
            result += f"\n... ({len(entries) - 100} more items omitted)"
        return result or "Directory is empty."
    except Exception as e:
        return f"Error listing directory '{directory}': {str(e)}"


@tool(
    name="search_in_files",
    description="Search for a text query across files in a directory.",
)
def search_in_files(query: str, directory: str = ".", extension: str = "") -> str:
    dir_path = Path(directory)
    if not dir_path.exists():
        return f"Error: Directory '{directory}' does not exist."

    matches: List[str] = []
    pattern = f"*{extension}" if extension else "*"
    for path in dir_path.rglob(pattern):
        if path.is_file() and not any(part.startswith(".") for part in path.parts):
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                for idx, line in enumerate(content.splitlines(), start=1):
                    if query in line:
                        matches.append(f"{path}:{idx}: {line.strip()[:120]}")
                        if len(matches) >= 50:
                            break
            except Exception:
                continue
        if len(matches) >= 50:
            break

    if not matches:
        return f"No matches found for '{query}' in '{directory}'."
    return "\n".join(matches)
