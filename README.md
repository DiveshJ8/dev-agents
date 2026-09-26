# Dev-Agents 🤖🛠️

A modular, extensible multi-agent orchestration platform designed for autonomous software engineering, architecture, code generation, testing, and review.

---

## 🎯 Project Overview

**Dev-Agents** provides a robust, decoupled framework where a supervisor orchestrator (`LeadArchitect`) collaborates with specialized sub-agents to take high-level software requirements and turn them into validated, production-grade code.

### Architecture

```mermaid
flowchart TD
    User([Developer / User]) -->|Task / Goal| Orchestrator[LeadArchitect (Orchestrator)]
    
    subgraph Multi-Agent Workspace
        Orchestrator -->|1. Design Specs| Architect[SystemArchitect]
        Architect -->|Architecture Specs| Coder[SeniorDeveloper]
        Coder -->|Implementation Code| Reviewer[CodeReviewer]
        Reviewer -->|QA & Audit| Tester[TestEngineer]
        Tester -->|Verification & Tests| Researcher[TechResearcher]
    end

    subgraph Tooling Layer
        Tools[(Developer Tools)]
        Tools -.-> ReadFile[read_file]
        Tools -.-> WriteFile[write_file]
        Tools -.-> Shell[execute_command]
        Tools -.-> Git[git_status / git_diff]
    end

    Architect -.-> Tools
    Coder -.-> Tools
    Reviewer -.-> Tools
    Tester -.-> Tools

    Orchestrator -->|Synthesized Deliverables| Artifacts[workspace/ Artifacts]
```

---

## 📁 Project Structure

```
D:\Work\dev-agents\
├── config/
│   └── default_config.yaml     # System & agent configuration
├── dev_agents/
│   ├── core/                   # Core agent engine
│   │   ├── base_agent.py       # BaseAgent lifecycle, tools loop, & memory
│   │   ├── orchestrator.py     # Supervisor multi-agent orchestrator
│   │   ├── message.py          # Pydantic message & tool call models
│   │   ├── state.py            # Shared state context & artifact persistence
│   │   └── registry.py         # Dynamic agent & tool registries
│   ├── llm/                    # Pluggable LLM provider abstraction
│   │   ├── base.py             # Abstract LLM provider interface
│   │   ├── gemini_provider.py  # Google Gemini (google-genai) provider
│   │   └── mock_provider.py    # Deterministic mock provider for dry runs & tests
│   ├── subagents/              # Specialized domain sub-agents
│   │   ├── architect.py        # System architecture & interface designer
│   │   ├── coder.py            # Implementation & code generation engineer
│   │   ├── reviewer.py         # Code quality & security auditor
│   │   ├── tester.py           # Unit/integration test engineer
│   │   └── researcher.py       # Technical research & documentation
│   ├── tools/                  # Developer tools
│   │   ├── base.py             # @tool decorator & schema generator
│   │   ├── file_tools.py       # File read, write, list, search
│   │   ├── shell_tools.py      # Sandboxed command execution
│   │   └── git_tools.py        # Git status and diff inspection
│   └── cli/
│       └── main.py             # Rich CLI interface
├── examples/
│   ├── basic_agent_run.py      # Single sub-agent quickstart
│   └── multi_agent_team.py     # Full multi-agent team demonstration
├── tests/                      # Pytest test suite
│   ├── test_base_agent.py
│   ├── test_orchestrator.py
│   └── test_tools.py
├── .env.example                # Environment variables template
├── pyproject.toml              # Build & dependency metadata
└── README.md
```

---

## 👥 Specialized Sub-Agents

| Agent | Role | Capabilities | Default Tools |
| :--- | :--- | :--- | :--- |
| **`LeadArchitect`** | Engineering Supervisor | Decomposes goals, routes tasks, aggregates artifacts | `delegate_to_subagent`, standard toolset |
| **`SystemArchitect`** | Architecture Specialist | Modular boundaries, file breakdown, API contracts | `read_file`, `list_directory`, `search_in_files` |
| **`SeniorDeveloper`** | Implementation Engineer | Production code generation, bug fixing, refactoring | `read_file`, `write_file`, `list_directory`, `execute_command` |
| **`CodeReviewer`** | QA & Security Auditor | Vulnerability scanning, code style, logic checking | `read_file`, `search_in_files`, `git_status`, `git_diff` |
| **`TestEngineer`** | Verification Engineer | Unit & integration tests, test running, coverage | `read_file`, `write_file`, `list_directory`, `execute_command` |
| **`TechResearcher`** | Technical Researcher | Library evaluation, documentation, API guides | `read_file`, `list_directory`, `search_in_files` |

---

## 🚀 Quickstart

### 1. Activate Environment
The virtual environment is ready at `.venv`:
```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

### 2. Run the Test Suite
Verify that all unit tests pass:
```powershell
python -m pytest -v
```

### 3. List Agents and Tools
```powershell
python -m dev_agents.cli.main list
```

### 4. Dispatch a Task to a Single Sub-Agent
```powershell
python -m dev_agents.cli.main run architect "Design a high-throughput rate limiter"
```

### 5. Run the Autonomous Multi-Agent Pipeline
```powershell
python -m dev_agents.cli.main pipeline "Build a thread-safe LRU Cache in Python with TTL expiration"
```
Deliverables are automatically saved to `./workspace/`:
- `architecture_spec.md`
- `implementation_notes.md`
- `code_review.md`
- `test_report.md`
- `SUMMARY.md`

---

## ⚙️ Configuring LLM Backends

By default, the platform runs in `mock` mode for instant, deterministic, zero-cost execution and testing.

### Switching to Google Gemini:
1. Copy `.env.example` to `.env` (or edit existing `.env`):
   ```ini
   AGENT_MODE=gemini
   DEFAULT_MODEL=gemini-2.5-flash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
2. Run any command: the agents will seamlessly invoke Gemini.

---

## 🧩 Adding a Custom Sub-Agent

Creating a new sub-agent takes just a few lines:

```python
from dev_agents.core.base_agent import BaseAgent
from dev_agents.tools.file_tools import read_file, write_file

class DevOpsAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="DevOpsAgent",
            role="CI/CD & Infrastructure Engineer",
            system_prompt=(
                "You are the DevOps Engineer. You write Dockerfiles, GitHub Actions workflows, "
                "Kubernetes manifests, and deployment scripts."
            ),
            tools=[read_file, write_file],
            **kwargs,
        )
```

Register it with the orchestrator:
```python
orchestrator.register_subagent(DevOpsAgent())
```

---

## 🔧 Adding Custom Tools

Define a Python function and decorate it with `@tool`:

```python
from dev_agents.tools.base import tool

@tool(name="database_query", description="Execute read-only SQL query against database.")
def database_query(query: str) -> str:
    # Query logic here
    return "query results"

# Attach to any agent
agent.add_tool(database_query)
```
