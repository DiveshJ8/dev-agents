from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from dev_agents.core.message import Message


class TaskArtifact(BaseModel):
    name: str
    path: Optional[str] = None
    content: str
    created_by: str
    description: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SharedState(BaseModel):
    task_id: str
    goal: str
    workspace_root: str = "./workspace"
    artifacts: Dict[str, TaskArtifact] = Field(default_factory=dict)
    conversation: List[Message] = Field(default_factory=list)
    subagent_history: Dict[str, List[Message]] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_message(self, message: Message) -> None:
        self.conversation.append(message)
        if message.sender not in self.subagent_history:
            self.subagent_history[message.sender] = []
        self.subagent_history[message.sender].append(message)

    def record_artifact(self, name: str, content: str, created_by: str, description: str = "", path: Optional[str] = None) -> TaskArtifact:
        artifact = TaskArtifact(
            name=name,
            content=content,
            created_by=created_by,
            description=description,
            path=path
        )
        self.artifacts[name] = artifact
        return artifact

    def get_artifact(self, name: str) -> Optional[TaskArtifact]:
        return self.artifacts.get(name)

    def save_artifacts_to_disk(self, target_dir: Optional[str] = None) -> List[Path]:
        out_dir = Path(target_dir or self.workspace_root)
        out_dir.mkdir(parents=True, exist_ok=True)
        saved_paths: List[Path] = []

        for name, artifact in self.artifacts.items():
            file_path = out_dir / (artifact.path or name)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(artifact.content, encoding="utf-8")
            saved_paths.append(file_path)

        return saved_paths
