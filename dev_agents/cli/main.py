from __future__ import annotations

import argparse
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

from dev_agents.core.orchestrator import Orchestrator
from dev_agents.subagents import create_default_agent_team
from dev_agents.tools import DEFAULT_DEV_TOOLS
from dev_agents.llm import get_llm_provider

# Automatically load .env if present
load_dotenv()
console = Console()


def build_system() -> Orchestrator:
    llm = get_llm_provider()
    subagents = create_default_agent_team(llm=llm)
    orchestrator = Orchestrator(
        name="LeadArchitect",
        subagents=subagents,
        tools=DEFAULT_DEV_TOOLS,
        llm=llm,
    )
    return orchestrator


def cmd_list(args: argparse.Namespace) -> None:
    orchestrator = build_system()
    
    # Subagents Table
    table_agents = Table(title="[bold green]Available Specialized Sub-Agents[/bold green]")
    table_agents.add_column("Agent Name", style="cyan", no_wrap=True)
    table_agents.add_column("Specialty / Role", style="magenta")
    table_agents.add_column("Tools Count", style="yellow")
    
    table_agents.add_row(orchestrator.name, f"[bold]{orchestrator.role} (Supervisor)[/bold]", str(len(orchestrator.tools)))
    for sa in orchestrator.subagents.values():
        table_agents.add_row(sa.name, sa.role, str(len(sa.tools)))
    
    console.print(table_agents)

    # Tools Table
    table_tools = Table(title="\n[bold cyan]Standard Developer Tools[/bold cyan]")
    table_tools.add_column("Tool Name", style="bold yellow")
    table_tools.add_column("Description", style="white")
    for t in DEFAULT_DEV_TOOLS:
        table_tools.add_row(t.name, t.description)
    console.print(table_tools)


def cmd_run(args: argparse.Namespace) -> None:
    orchestrator = build_system()
    agent_name = args.agent.lower()
    
    target_agent = orchestrator if agent_name in ("leadarchitect", "orchestrator", "supervisor") else orchestrator.get_subagent(agent_name)
    if not target_agent:
        console.print(f"[bold red]Error:[/bold red] Subagent '{args.agent}' not found.")
        console.print(f"Available agents: leadarchitect, {', '.join(orchestrator.subagents.keys())}")
        sys.exit(1)

    console.print(Panel(f"[bold cyan]Agent:[/bold cyan] {target_agent.name} ({target_agent.role})\n[bold cyan]Task:[/bold cyan] {args.prompt}", title="Task Dispatch"))
    
    with console.status(f"[bold green]{target_agent.name} is working...[/bold green]"):
        result = target_agent.run(args.prompt)

    console.print(Panel(Markdown(result), title=f"[bold green]Response from {target_agent.name}[/bold green]"))


if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def cmd_pipeline(args: argparse.Namespace) -> None:
    orchestrator = build_system()
    
    console.print(Panel(
        f"[bold yellow]Goal:[/bold yellow] {args.goal}\n"
        f"[bold yellow]Workspace:[/bold yellow] {orchestrator.workspace_root}",
        title="[bold green]Multi-Agent Autonomous Pipeline[/bold green]",
    ))

    def on_step(stage: str, msg: str) -> None:
        console.print(f"[bold cyan]>> {stage}:[/bold cyan] {msg}")

    state = orchestrator.execute_development_pipeline(args.goal, on_step_update=on_step)
    
    console.print("\n[bold green][SUCCESS] Pipeline Completed Successfully![/bold green]")
    console.print(f"Artifacts generated: [bold cyan]{len(state.artifacts)} files[/bold cyan] saved in [bold]{state.workspace_root}/[/bold]")
    for name, art in state.artifacts.items():
        console.print(f"  * [green]{name}[/green] ({art.description})")


def cli_entrypoint() -> None:
    parser = argparse.ArgumentParser(
        prog="dev-agents",
        description="Dev-Agents: Multi-Agent Software Engineering Platform",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # List command
    subparsers.add_parser("list", help="List registered sub-agents and tools")

    # Run single agent command
    p_run = subparsers.add_parser("run", help="Run a specific sub-agent on a prompt")
    p_run.add_argument("agent", help="Name of subagent (architect, coder, reviewer, tester, researcher)")
    p_run.add_argument("prompt", help="Task description or prompt")

    # Full pipeline command
    p_pipe = subparsers.add_parser("pipeline", help="Run end-to-end multi-agent development workflow")
    p_pipe.add_argument("goal", help="Engineering goal or feature to design, code, review, and test")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "list":
        cmd_list(args)
    elif args.command == "run":
        cmd_run(args)
    elif args.command == "pipeline":
        cmd_pipeline(args)


if __name__ == "__main__":
    cli_entrypoint()
