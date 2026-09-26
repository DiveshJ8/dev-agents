from __future__ import annotations

import re
from typing import Any, Dict, List, Optional
from dev_agents.core.message import Message, ToolCall
from dev_agents.llm.base import BaseLLMProvider, LLMResponse
from dev_agents.tools.base import BaseTool


class MockLLMProvider(BaseLLMProvider):
    """Deterministic mock provider for testing, offline execution, and development demonstration."""

    def __init__(self, model_name: str = "mock-dev-llm", temperature: float = 0.0):
        super().__init__(model_name=model_name, temperature=temperature)
        self.call_count = 0

    def generate(
        self,
        messages: List[Message],
        tools: Optional[List[BaseTool]] = None,
        system_instruction: Optional[str] = None,
    ) -> LLMResponse:
        self.call_count += 1
        last_msg = messages[-1].content if messages else ""
        system = system_instruction or ""

        # Check if caller is requesting a specific subagent role
        if "Architect" in system or "SystemArchitect" in system:
            return LLMResponse(
                content=(
                    "### Architecture Blueprint\n"
                    "1. **Core Module**: High-cohesion abstract classes for state and lifecycle management.\n"
                    "2. **Interface Contract**: Strict input/output validation with Pydantic.\n"
                    "3. **Extensibility**: Pluggable sub-agent registry and dynamic tool dispatch.\n"
                    "4. **Execution Flow**: Supervisor -> Task Decomposition -> Parallel/Sequential Sub-agents -> Review -> Deliverable."
                ),
                model=self.model_name,
            )

        elif "SeniorDeveloper" in system or "Coder" in system:
            return LLMResponse(
                content=(
                    "### Implementation Completed\n"
                    "```python\n"
                    "# Verified clean implementation with typing and error handling\n"
                    "def execute_task(task_spec: dict) -> dict:\n"
                    "    return {'status': 'success', 'data': task_spec}\n"
                    "```\n"
                    "All requested functions have been implemented according to architectural specifications."
                ),
                model=self.model_name,
            )

        elif "CodeReviewer" in system or "Reviewer" in system:
            return LLMResponse(
                content=(
                    "### QA & Code Review Findings\n"
                    "- **Security**: No hardcoded credentials or unescaped shell inputs detected. Passed.\n"
                    "- **Performance**: Asynchronous execution paths and bounded retries verified. Passed.\n"
                    "- **Typing & Cleanliness**: PEP 8 compliance and strict type annotations adhered to. Passed.\n"
                    "Status: **APPROVED FOR MERGE**."
                ),
                model=self.model_name,
            )

        elif "TestEngineer" in system or "Tester" in system:
            return LLMResponse(
                content=(
                    "### Test Verification Report\n"
                    "Generated unit tests covering edge cases, invalid inputs, and happy paths.\n"
                    "- `test_initialization`: PASSED\n"
                    "- `test_tool_execution`: PASSED\n"
                    "- `test_subagent_delegation`: PASSED\n"
                    "Coverage: **96%**. All assertions passed."
                ),
                model=self.model_name,
            )

        elif "TechResearcher" in system or "Researcher" in system:
            return LLMResponse(
                content=(
                    "### Technical Research Summary\n"
                    "- **Ecosystem Analysis**: Multi-agent systems benefit from decoupled message passing and isolated state.\n"
                    "- **Best Practices**: Provide each subagent a constrained toolset and strict task specification.\n"
                    "- **Recommended Follow-up**: Add persistent SQLite/PostgreSQL state storage for long-running workflows."
                ),
                model=self.model_name,
            )

        elif "ColabEngineer" in system or "Colab" in system:
            return LLMResponse(
                content=(
                    "### Google Colab Cloud Deployment Ready\n"
                    "- **Target Platform**: [Google Colab (GPU: T4)](https://colab.research.google.com/)\n"
                    "- **Open-in-Colab Link**: https://colab.research.google.com/github/DiveshJ8/dev-agents/blob/main/notebooks/colab_app.ipynb\n"
                    "- **Environment Provisioning**: Automatic GPU accelerator selection and dependency installation.\n"
                    "- **Tunneling & Public URL**: Configured with live web tunnel for remote UI execution.\n"
                    "Status: **Notebook generated and ready for 1-click execution in Colab.**"
                ),
                model=self.model_name,
            )

        # Default fallback response
        return LLMResponse(
            content=f"Synthesized analysis for query: '{last_msg[:60]}...'. All tasks orchestrated successfully.",
            model=self.model_name,
        )
