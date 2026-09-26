from __future__ import annotations

import uuid
from typing import Callable, Dict, List, Optional
from rich.console import Console
from dev_agents.core.base_agent import BaseAgent
from dev_agents.core.message import Message, MessageRole
from dev_agents.core.state import SharedState
from dev_agents.llm.base import BaseLLMProvider
from dev_agents.tools.base import BaseTool, tool

console = Console()


class Orchestrator(BaseAgent):
    """Supervisor agent that coordinates sub-agents to achieve end-to-end development goals."""

    def __init__(
        self,
        name: str = "Megatron",
        role: str = "Engineering Supervisor",
        system_prompt: Optional[str] = None,
        subagents: Optional[List[BaseAgent]] = None,
        tools: Optional[List[BaseTool]] = None,
        llm: Optional[BaseLLMProvider] = None,
        workspace_root: str = "./workspace",
    ):
        prompt = system_prompt or (
            "You are Megatron, the Lead Engineering Supervisor. You receive high-level software development tasks.\n"
            "You can delegate sub-tasks to your specialized sub-agents: Starscream (Architect), Shockwave (Coder), Reflector (Reviewer), Brawl (Tester), Soundwave (Researcher), and Astrotrain (Colab).\n"
            "Review outputs from your sub-agents, combine their contributions, and produce a cohesive final deliverable."
        )
        super().__init__(
            name=name,
            role=role,
            system_prompt=prompt,
            tools=tools or [],
            llm=llm,
        )
        self.workspace_root = workspace_root
        self.subagents: Dict[str, BaseAgent] = {}
        if subagents:
            for sa in subagents:
                self.register_subagent(sa)

        # Register delegation tool on the orchestrator
        self._setup_orchestrator_tools()

    def register_subagent(self, subagent: BaseAgent) -> None:
        self.subagents[subagent.name.lower()] = subagent

    def get_subagent(self, name: str) -> Optional[BaseAgent]:
        key = name.lower().strip()
        if key in self.subagents:
            return self.subagents[key]

        aliases = {
            # Starscream / SystemArchitect
            "architect": "starscream",
            "arch": "starscream",
            "systemarchitect": "starscream",
            "starscream": "starscream",
            # Shockwave / SeniorDeveloper / Coder
            "coder": "shockwave",
            "developer": "shockwave",
            "dev": "shockwave",
            "seniordeveloper": "shockwave",
            "shockwave": "shockwave",
            # Reflector / CodeReviewer
            "reviewer": "reflector",
            "review": "reflector",
            "qa": "reflector",
            "codereviewer": "reflector",
            "reflector": "reflector",
            # Brawl / TestEngineer
            "tester": "brawl",
            "test": "brawl",
            "testengineer": "brawl",
            "brawl": "brawl",
            # Soundwave / TechResearcher
            "researcher": "soundwave",
            "research": "soundwave",
            "docs": "soundwave",
            "techresearcher": "soundwave",
            "soundwave": "soundwave",
            # Astrotrain / ColabEngineer
            "colab": "astrotrain",
            "colabengineer": "astrotrain",
            "colabagent": "astrotrain",
            "cloudgpu": "astrotrain",
            "astrotrain": "astrotrain",
        }
        resolved = aliases.get(key, key)
        if resolved in self.subagents:
            return self.subagents[resolved]

        # Reverse fallback if an agent was registered with legacy names
        legacy_reverse = {
            "starscream": "systemarchitect",
            "shockwave": "seniordeveloper",
            "reflector": "codereviewer",
            "brawl": "testengineer",
            "soundwave": "techresearcher",
            "astrotrain": "colabengineer",
        }
        fallback_key = legacy_reverse.get(resolved, resolved)
        return self.subagents.get(fallback_key)

    def _setup_orchestrator_tools(self) -> None:
        """Adds tools allowing the supervisor to delegate work to sub-agents."""
        
        @tool(
            name="delegate_to_subagent",
            description="Delegate a specific technical task to one of your specialized subagents.",
        )
        def delegate_to_subagent(subagent_name: str, task: str) -> str:
            agent = self.get_subagent(subagent_name)
            if not agent:
                available = ", ".join(self.subagents.keys())
                return f"Error: Subagent '{subagent_name}' not found. Available: {available}"
            
            return agent.run(task)

        self.add_tool(delegate_to_subagent)

    def execute_development_pipeline(
        self,
        goal: str,
        on_step_update: Optional[Callable[[str, str], None]] = None,
    ) -> SharedState:
        """Executes a standard end-to-end multi-agent software engineering lifecycle."""
        state = SharedState(
            task_id=str(uuid.uuid4())[:8],
            goal=goal,
            workspace_root=self.workspace_root,
        )

        def notify(stage: str, msg: str) -> None:
            if on_step_update:
                on_step_update(stage, msg)

        # Step 1: Architectural Analysis
        arch_agent = self.get_subagent("starscream") or self.get_subagent("architect") or self.get_subagent("systemarchitect")
        arch_name = arch_agent.name if arch_agent else "Starscream"
        notify("1. System Design", f"{arch_name} is designing the module architecture...")
        arch_output = ""
        if arch_agent:
            arch_output = arch_agent.run(f"Design system architecture and file breakdown for: {goal}")
            state.record_artifact(
                name="architecture_spec.md",
                content=arch_output,
                created_by=arch_agent.name,
                description="System architectural design and technical specifications.",
            )

        # Step 2: Implementation / Code Generation
        coder_agent = self.get_subagent("shockwave") or self.get_subagent("coder") or self.get_subagent("seniordeveloper")
        coder_name = coder_agent.name if coder_agent else "Shockwave"
        notify("2. Implementation", f"{coder_name} is coding the components...")
        coder_output = ""
        if coder_agent:
            coder_prompt = f"Implement the code based on the architecture:\n{arch_output or goal}"
            coder_output = coder_agent.run(coder_prompt)
            state.record_artifact(
                name="implementation_notes.md",
                content=coder_output,
                created_by=coder_agent.name,
                description="Core implementation code and modules.",
            )

        # Step 3: Code Review & Security Audit
        reviewer_agent = self.get_subagent("reflector") or self.get_subagent("reviewer") or self.get_subagent("codereviewer")
        reviewer_name = reviewer_agent.name if reviewer_agent else "Reflector"
        notify("3. Code Review", f"{reviewer_name} is reviewing quality and security...")
        review_output = ""
        if reviewer_agent:
            review_prompt = f"Audit this implementation for security, style, and correctness:\n{coder_output}"
            review_output = reviewer_agent.run(review_prompt)
            state.record_artifact(
                name="code_review.md",
                content=review_output,
                created_by=reviewer_agent.name,
                description="Quality assurance and security audit report.",
            )

        # Step 4: Test Suite Generation & Verification
        tester_agent = self.get_subagent("brawl") or self.get_subagent("tester") or self.get_subagent("testengineer")
        tester_name = tester_agent.name if tester_agent else "Brawl"
        notify("4. Test Automation", f"{tester_name} is generating test suite...")
        test_output = ""
        if tester_agent:
            test_prompt = f"Write unit tests and verification steps for:\n{coder_output}"
            test_output = tester_agent.run(test_prompt)
            state.record_artifact(
                name="test_report.md",
                content=test_output,
                created_by=tester_agent.name,
                description="Automated tests and test execution results.",
            )

        # Step 5: Final Synthesis by Orchestrator
        notify("5. Synthesis", f"{self.name} is finalizing project package...")
        final_summary = (
            f"# Project Deliverable: {goal}\n\n"
            f"## 1. Architecture Overview\n{arch_output}\n\n"
            f"## 2. Implementation\n{coder_output}\n\n"
            f"## 3. QA & Security Review\n{review_output}\n\n"
            f"## 4. Test Verification\n{test_output}\n"
        )
        state.record_artifact(
            name="SUMMARY.md",
            content=final_summary,
            created_by=self.name,
            description="Complete synthesized deliverable across all sub-agents.",
        )

        # Persist deliverables to disk
        state.save_artifacts_to_disk()
        notify("Completed", f"All artifacts saved to {state.workspace_root}/")

        return state
