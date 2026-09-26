import pytest
from pathlib import Path
from dev_agents.tools.base import tool, BaseTool
from dev_agents.tools.file_tools import read_file, write_file, list_directory
from dev_agents.tools.shell_tools import execute_command


def test_tool_decorator():
    @tool(name="calculator", description="Adds two numbers")
    def add(a: int, b: int) -> int:
        return a + b

    assert isinstance(add, BaseTool)
    assert add.name == "calculator"
    assert add.description == "Adds two numbers"
    assert add.run(a=2, b=3) == 5


def test_file_tools(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    write_res = write_file(filepath=str(test_file), content="Hello Agents!")
    assert "Successfully wrote" in write_res
    assert test_file.exists()

    content = read_file(filepath=str(test_file))
    assert content == "Hello Agents!"

    list_res = list_directory(directory=str(tmp_path))
    assert "test.txt" in list_res


def test_shell_tools():
    # Echo test cross-platform
    res = execute_command(command="echo agent_test")
    assert "agent_test" in res
    assert "Exit Code: 0" in res
