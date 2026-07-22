from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4


class NodeType(str, Enum):
    USER = "USER"
    PROJECT = "PROJECT"
    GOAL = "GOAL"
    TASK = "TASK"
    MEMORY = "MEMORY"
    TOOL = "TOOL"
    PLAN = "PLAN"
    SESSION = "SESSION"
    EVENT = "EVENT"
    FILE = "FILE"
    FOLDER = "FOLDER"
    REPOSITORY = "REPOSITORY"
    AGENT = "AGENT"
    MODEL = "MODEL"
    PLUGIN = "PLUGIN"


class RelationType(str, Enum):
    OWNS = "OWNS"
    CREATED = "CREATED"
    USES = "USES"
    DEPENDS_ON = "DEPENDS_ON"
    GENERATED = "GENERATED"
    MODIFIED = "MODIFIED"
    EXECUTED = "EXECUTED"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"
    RELATED_TO = "RELATED_TO"
    CHILD_OF = "CHILD_OF"
    PARENT_OF = "PARENT_OF"
    REFERENCES = "REFERENCES"
    BELONGS_TO = "BELONGS_TO"


@dataclass
class GraphNode:
    node_type: NodeType
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)
    node_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value if hasattr(self.node_type, "value") else str(self.node_type),
            "label": self.label,
            "properties": self.properties,
            "created_at": self.created_at.isoformat() if hasattr(self.created_at, "isoformat") else str(self.created_at),
        }


@dataclass
class GraphEdge:
    source_id: str
    target_id: str
    relation_type: RelationType
    weight: int = 1
    properties: Dict[str, Any] = field(default_factory=dict)
    edge_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation_type": self.relation_type.value if hasattr(self.relation_type, "value") else str(self.relation_type),
            "weight": self.weight,
            "properties": self.properties,
            "created_at": self.created_at.isoformat() if hasattr(self.created_at, "isoformat") else str(self.created_at),
        }
