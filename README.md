# Dev-Agents 🤖🛠️

A modular, extensible multi-agent orchestration platform designed for autonomous software engineering, architecture, code generation, testing, code review, and **Google Colab Cloud GPU Execution**.

---

## 🎯 Project Overview

**Dev-Agents** provides a robust, decoupled framework where a supervisor orchestrator (`LeadArchitect`) collaborates with specialized sub-agents to take high-level software requirements and turn them into validated, production-grade code and cloud-deployable applications.

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
        Orchestrator -->|Cloud Execution & App Deploy| Colab[ColabEngineer]
    end

    subgraph Tooling Layer
        Tools[(Developer Tools)]
        Tools -.-> ReadFile[read_file]
        Tools -.-> WriteFile[write_file]
        Tools -.-> Shell[execute_command]
        Tools -.-> Git[git_status / git_diff]
        Tools -.-> ColabTools[Colab Tools & MCP]
    end

    subgraph Colab Cloud Execution
        ColabTools -->|1-Click Launch| ColabWeb["Google Colab (GPU: T4 / A100 / TPU)"]
        ColabTools -->|Localtunnel / Gradio / ngrok| PublicURL[Live Web App URL]
        ColabTools -->|Cross-Origin Bridge| LocalRuntime[Local Jupyter Runtime Bridge]
    end

    Architect -.-> Tools
    Coder -.-> Tools
    Reviewer -.-> Tools
    Tester -.-> Tools
    Colab -.-> Tools

    Orchestrator -->|Synthesized Deliverables| Artifacts[workspace/ Artifacts]
```

---

## 📁 Project Structure

```
D:\Work\dev-agents\
├── config/
│   └── default_config.yaml         # System, subagents, and MCP server configuration
├── dev_agents/
│   ├── core/                       # Core agent engine
│   │   ├── base_agent.py           # BaseAgent lifecycle, tools loop, & memory
│   │   ├── orchestrator.py         # Supervisor multi-agent orchestrator
│   │   ├── message.py              # Pydantic message & tool call models
│   │   ├── state.py                # Shared state context & artifact persistence
│   │   └── registry.py             # Dynamic agent & tool registries
│   ├── llm/                        # Pluggable LLM provider abstraction
│   │   ├── base.py                 # Abstract LLM provider interface
│   │   ├── gemini_provider.py      # Google Gemini (google-genai) provider
│   │   └── mock_provider.py        # Deterministic mock provider for dry runs & tests
│   ├── subagents/                  # Specialized domain sub-agents
│   │   ├── architect.py            # System architecture & interface designer
│   │   ├── coder.py                # Implementation & code generation engineer
│   │   ├── reviewer.py             # Code quality & security auditor
│   │   ├── tester.py               # Unit/integration test engineer
│   │   ├── researcher.py           # Technical research & documentation
│   │   └── colab_agent.py          # Google Colab & Cloud Execution specialist
│   ├── tools/                      # Developer tools
│   │   ├── base.py                 # @tool decorator & schema generator
│   │   ├── file_tools.py           # File read, write, list, search
│   │   ├── shell_tools.py          # Sandboxed command execution
│   │   ├── git_tools.py            # Git status and diff inspection
│   │   └── colab_tools.py          # Google Colab notebook & tunneling tools
│   ├── mcp/                        # Model Context Protocol (MCP) servers
│   │   └── colab_server.py         # Standalone Google Colab MCP Server
│   └── cli/
│       └── main.py                 # Rich interactive CLI interface
├── examples/
│   ├── basic_agent_run.py          # Single sub-agent quickstart
│   ├── multi_agent_team.py         # Full multi-agent team demonstration
│   └── colab_app_deployment.py    # Packaging & running an app on Google Colab
├── tests/                          # Pytest test suite (13 unit tests, 100% passing)
│   ├── test_base_agent.py
│   ├── test_orchestrator.py
│   ├── test_tools.py
│   └── test_colab.py
├── .env.example                    # Environment variables template
├── pyproject.toml                  # Build & dependency metadata
└── README.md
```

---

## 👥 Specialized Sub-Agents

| Agent | Role | Capabilities | Default Tools |
| :--- | :--- | :--- | :--- |
| **`LeadArchitect`** | Engineering Supervisor | Decomposes goals, routes tasks, aggregates artifacts | `delegate_to_subagent`, full standard toolset |
| **`ColabEngineer`** | Colab Cloud Execution | Packages apps, provisions GPU/TPU notebooks, sets up public tunnels | `package_app_for_colab`, `create_colab_notebook`, `generate_colab_link`, `open_colab_in_browser`, `get_colab_local_runtime_command` |
| **`SystemArchitect`** | Architecture Specialist | Modular boundaries, file breakdown, API contracts | `read_file`, `list_directory`, `search_in_files` |
| **`SeniorDeveloper`** | Implementation Engineer | Production code generation, bug fixing, refactoring | `read_file`, `write_file`, `list_directory`, `execute_command` |
| **`CodeReviewer`** | QA & Security Auditor | Vulnerability scanning, code style, logic checking | `read_file`, `search_in_files`, `git_status`, `git_diff` |
| **`TestEngineer`** | Verification Engineer | Unit & integration tests, test running, coverage | `read_file`, `write_file`, `list_directory`, `execute_command` |
| **`TechResearcher`** | Technical Researcher | Library evaluation, documentation, API guides | `read_file`, `list_directory`, `search_in_files` |

---

## ⚡ Google Colab Integration & App Execution

The platform enables any sub-agent or user to package applications and execute them in the cloud via **[Google Colab](https://colab.research.google.com/)**:

### 1. Package Python Apps into Colab Notebooks
Supports Streamlit, Gradio, FastAPI, and PyTorch apps with automated dependency installation and public tunneling:

```powershell
python -m dev_agents.cli.main run colab "Package my Gradio computer vision app to execute on Colab GPU with a public web tunnel"
```

### 2. Direct 1-Click Launch Links
Generates official GitHub-linked URLs that immediately open in Colab:
```
https://colab.research.google.com/github/DiveshJ8/dev-agents/blob/main/notebooks/sentiment_colab.ipynb
```

### 3. Connect Colab Web UI to Local Runtime
Bridge Google Colab's notebook UI directly to your local workstation:
```powershell
jupyter notebook --NotebookApp.allow_origin='https://colab.research.google.com' --port=8888 --NotebookApp.port_retries=0
```

---

## 🔌 Google Colab MCP Server (Model Context Protocol)

A dedicated, standard-compliant MCP server is included at `dev_agents/mcp/colab_server.py`.

### Exposed Tools
* `colab_create_notebook`: Creates valid `.ipynb` notebooks with GPU/TPU accelerators and Colab badges.
* `colab_generate_link`: Produces instant 1-click launch URLs for GitHub and Google Drive.
* `colab_package_app`: Packages any Python script (Streamlit, Gradio, FastAPI) into a tunneled notebook.
* `colab_connect_local_runtime`: Generates local/remote Jupyter runtime bridge commands.
* `colab_open_in_browser`: Opens notebook URLs directly in your browser.

### Running the MCP Server
```powershell
# Run over stdio (standard for MCP clients)
python -m dev_agents.mcp.colab_server --transport stdio

# Run over Server-Sent Events (SSE)
python -m dev_agents.mcp.colab_server --transport sse --port 8000
```

### Configuring in MCP Clients (Antigravity, Claude Desktop, Cursor)
Add to your `mcp_config.json` or client settings:
```json
{
  "mcpServers": {
    "colab-dev-agent": {
      "command": "D:/Work/dev-agents/.venv/Scripts/python.exe",
      "args": ["-m", "dev_agents.mcp.colab_server", "--transport", "stdio"],
      "cwd": "D:/Work/dev-agents"
    }
  }
}
```

---

## 🚀 Quickstart

### 1. Activate Environment
```powershell
cd D:\Work\dev-agents
.\.venv\Scripts\Activate.ps1
```

### 2. Run the Test Suite
```powershell
python -m pytest -v
```
*(All 13 unit tests pass)*

### 3. List Agents and Tools
```powershell
python -m dev_agents.cli.main list
```

### 4. Dispatch a Task to a Single Sub-Agent
```powershell
python -m dev_agents.cli.main run architect "Design a high-throughput rate limiter"
python -m dev_agents.cli.main run colab "Prepare a PyTorch fine-tuning notebook for Colab A100 GPU"
```

### 5. Run the Autonomous Multi-Agent Pipeline
```powershell
python -m dev_agents.cli.main pipeline "Build a thread-safe LRU Cache in Python with TTL expiration"
```

---

## ⚙️ Configuring LLM Backends

By default, the platform runs in `mock` mode for instant, deterministic, zero-cost execution and testing.

### Switching to Google Gemini:
1. Edit `.env`:
   ```ini
   AGENT_MODE=gemini
   DEFAULT_MODEL=gemini-2.5-flash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
2. Run any command: the agents will invoke live Gemini models.
