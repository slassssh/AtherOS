from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class NodeRole(str, Enum):
    LEADER = "LEADER"
    WORKER = "WORKER"
    STANDBY = "STANDBY"


class NodeStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"


@dataclass
class NodeSpec:
    """
    Specification & Resource Capacity for an AtherOS Cluster Node.
    """

    node_id: str = field(default_factory=lambda: f"node-{str(uuid4())[:8]}")
    address: str = "127.0.0.1:9090"
    role: NodeRole = NodeRole.WORKER
    status: NodeStatus = NodeStatus.HEALTHY
    cpu_cores: int = 8
    ram_gb: float = 16.0
    has_gpu: bool = True
    installed_models: List[str] = field(default_factory=lambda: ["gpt-4o", "llama3-8b"])
    installed_plugins: List[str] = field(default_factory=lambda: ["git_plugin", "docker_plugin"])
    active_tasks: int = 0
    latency_ms: float = 15.0
    last_heartbeat: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "address": self.address,
            "role": self.role.value,
            "status": self.status.value,
            "cpu_cores": self.cpu_cores,
            "ram_gb": self.ram_gb,
            "has_gpu": self.has_gpu,
            "installed_models": self.installed_models,
            "installed_plugins": self.installed_plugins,
            "active_tasks": self.active_tasks,
            "latency_ms": self.latency_ms,
            "last_heartbeat": self.last_heartbeat.isoformat()
        }
