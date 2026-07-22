from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class MemoryItem:
    """
    Standardized Enterprise Memory Entity.
    Defines memory metadata across all hierarchical layers.
    """

    content: str
    layer: str  # "session", "working", "project", "long_term", "episodic", "semantic", "tool"
    source: str = "SYSTEM"  # "USER", "TOOL", "ENGINE", "PLANNER", "SYSTEM"
    session_id: Optional[str] = None
    project_id: Optional[str] = None
    importance: int = 1  # 1 (low) to 10 (critical)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding_ready: bool = True
    memory_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "memory_id": self.memory_id,
            "timestamp": self.timestamp.isoformat(),
            "session_id": self.session_id,
            "project_id": self.project_id,
            "importance": self.importance,
            "tags": self.tags,
            "source": self.source,
            "layer": self.layer,
            "content": self.content,
            "embedding_ready": self.embedding_ready,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryItem":
        ts = data.get("timestamp")
        dt = datetime.fromisoformat(ts) if isinstance(ts, str) else datetime.now(UTC)
        return cls(
            memory_id=data.get("memory_id", str(uuid4())),
            timestamp=dt,
            session_id=data.get("session_id"),
            project_id=data.get("project_id"),
            importance=data.get("importance", 1),
            tags=data.get("tags", []),
            source=data.get("source", "SYSTEM"),
            layer=data.get("layer", "session"),
            content=data.get("content", ""),
            embedding_ready=data.get("embedding_ready", True),
            metadata=data.get("metadata", {}),
        )
