import pytest
from dev_agents.core.base_agent import BaseAgent
from dev_agents.core.message import MessageRole, ToolCall
from dev_agents.llm.mock_provider import MockLLMProvider
from dev_agents.tools.base import tool


def test_base_agent_initialization():
    agent = BaseAgent(
        name="Tester",
        role="Test Role",
        system_prompt="Test Prompt",
        llm=MockLLMProvider(),
    )
    assert agent.name == "Tester"
    assert agent.role == "Test Role"
    assert len(agent.memory) == 0


def test_agent_tool_registration_and_execution():
    @tool(name="multiply", description="Multiplies numbers")
    def multiply(x: int, y: int) -> int:
        return x * y

    agent = BaseAgent(
        name="MathAgent",
        role="Math Specialist",
        system_prompt="Math Prompt",
        tools=[multiply],
        llm=MockLLMProvider(),
    )
    assert "multiply" in agent.tools

    # Execute tool call
    call = ToolCall(id="call_1", name="multiply", arguments={"x": 6, "y": 7})
    result = agent.execute_tool(call)
    assert not result.is_error
    assert result.content == "42"


def test_agent_run_loop():
    agent = BaseAgent(
        name="SeniorDeveloper",
        role="Developer",
        system_prompt="Developer instructions",
        llm=MockLLMProvider(),
    )
    response = agent.run("Implement a binary search tree.")
    assert len(response) > 0
    assert len(agent.memory) >= 2  # user msg + assistant msg
    assert agent.memory[0].role == MessageRole.USER
    assert agent.memory[-1].role == MessageRole.ASSISTANT
