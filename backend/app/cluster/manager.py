from datetime import datetime, UTC
from typing import Any, Dict, List, Optional
from backend.app.cluster.types import NodeRole, NodeSpec, NodeStatus
from backend.app.events.bus import EventBus
from backend.app.events.types import SystemEvent, SystemEventType
from backend.app.memory.manager import MemoryManager
from backend.app.memory.memory_item import MemoryItem
from backend.app.utils.logger import logger


class NodeManager:
    """Manages cluster topology, node specifications, and discovery."""

    def __init__(self):
        self._nodes: Dict[str, NodeSpec] = {}

    def register_node(self, spec: NodeSpec) -> None:
        self._nodes[spec.node_id] = spec
        logger.info(f"Registered Cluster Node: {spec.node_id} ({spec.role.value}) at {spec.address}")

    def unregister_node(self, node_id: str) -> bool:
        if node_id in self._nodes:
            del self._nodes[node_id]
            logger.info(f"Unregistered Cluster Node: {node_id}")
            return True
        return False

    def get_node(self, node_id: str) -> Optional[NodeSpec]:
        return self._nodes.get(node_id)

    def list_nodes(self) -> List[Dict[str, Any]]:
        return [n.to_dict() for n in self._nodes.values()]


class DistributedScheduler:
    """Intelligent Workload Scheduler for AtherOS Clusters."""

    def schedule_task(self, nodes: List[NodeSpec], required_model: Optional[str] = None, require_gpu: bool = False) -> NodeSpec:
        healthy = [n for n in nodes if n.status == NodeStatus.HEALTHY]
        if not healthy:
            raise RuntimeError("No healthy cluster nodes available for distributed scheduling.")

        if required_model:
            healthy = [n for n in healthy if required_model in n.installed_models]
            if not healthy:
                healthy = [n for n in nodes if n.status == NodeStatus.HEALTHY]

        if require_gpu:
            gpu_nodes = [n for n in healthy if n.has_gpu]
            if gpu_nodes:
                healthy = gpu_nodes

        # Sort by least active tasks, lowest latency, and highest RAM
        healthy.sort(key=lambda n: (n.active_tasks, n.latency_ms, -n.ram_gb))
        return healthy[0]


class HeartbeatService:
    """Heartbeat monitoring and Leader Election service for AtherOS Cluster."""

    def check_heartbeats(self, nodes: Dict[str, NodeSpec], max_timeout_seconds: int = 10) -> List[str]:
        now = datetime.now(UTC)
        failed_nodes = []
        for nid, node in list(nodes.items()):
            delta = (now - node.last_heartbeat).total_seconds()
            if delta > max_timeout_seconds:
                node.status = NodeStatus.OFFLINE
                failed_nodes.append(nid)
                logger.warning(f"Cluster Node '{nid}' missed heartbeat ({delta:.1f}s ago). Marked OFFLINE.")

        return failed_nodes

    def elect_leader(self, nodes: Dict[str, NodeSpec]) -> Optional[NodeSpec]:
        """Elects a new Leader node from healthy candidates."""
        healthy_candidates = [n for n in nodes.values() if n.status == NodeStatus.HEALTHY]
        if not healthy_candidates:
            return None

        # Sort by role priority, highest RAM & CPU
        healthy_candidates.sort(key=lambda n: (-n.ram_gb, -n.cpu_cores))
        new_leader = healthy_candidates[0]
        new_leader.role = NodeRole.LEADER
        logger.info(f"Elected NEW Cluster Leader Node: {new_leader.node_id}")
        return new_leader


class RemoteExecutionManager:
    """Manages remote agent task dispatch and migration upon node failure."""

    def __init__(self, scheduler: DistributedScheduler):
        self.scheduler = scheduler
        self.active_remote_tasks: Dict[str, str] = {}  # task_id -> node_id

    def dispatch_remote_task(self, task_id: str, node: NodeSpec, payload: Dict[str, Any]) -> Dict[str, Any]:
        node.active_tasks += 1
        self.active_remote_tasks[task_id] = node.node_id
        logger.info(f"Dispatched Remote Task '{task_id}' to Node '{node.node_id}'")

        # Simulate successful remote execution
        node.active_tasks = max(0, node.active_tasks - 1)
        return {
            "task_id": task_id,
            "executed_by": node.node_id,
            "status": "COMPLETED",
            "result": f"Executed remotely on {node.node_id}"
        }


class ClusterManager:
    """
    Enterprise Cluster Orchestrator for AtherOS.
    Manages multi-node topology, leader election, distributed task scheduling, remote execution,
    distributed memory replication, and event propagation.
    """

    def __init__(self, memory_manager: Optional[MemoryManager] = None, event_bus: Optional[EventBus] = None):
        self.memory_manager = memory_manager or MemoryManager()
        self.event_bus = event_bus or EventBus()

        self.node_manager = NodeManager()
        self.scheduler = DistributedScheduler()
        self.heartbeat_service = HeartbeatService()
        self.remote_executor = RemoteExecutionManager(self.scheduler)

        self.leader_node: Optional[NodeSpec] = None

        # Auto-initialize local leader node and 2 worker nodes
        self._init_default_cluster()

    def _init_default_cluster(self):
        local_leader = NodeSpec(node_id="node-leader-01", address="127.0.0.1:9090", role=NodeRole.LEADER, ram_gb=32.0, cpu_cores=16)
        worker_1 = NodeSpec(node_id="node-worker-02", address="192.168.1.101:9090", role=NodeRole.WORKER, ram_gb=16.0, cpu_cores=8, installed_models=["llama3-8b"])
        worker_2 = NodeSpec(node_id="node-worker-03", address="192.168.1.102:9090", role=NodeRole.WORKER, ram_gb=16.0, cpu_cores=8, installed_models=["claude-3-5-sonnet"])

        self.node_manager.register_node(local_leader)
        self.node_manager.register_node(worker_1)
        self.node_manager.register_node(worker_2)

        self.leader_node = local_leader

    def heartbeat(self, node_id: str) -> bool:
        node = self.node_manager.get_node(node_id)
        if node:
            node.last_heartbeat = datetime.now(UTC)
            node.status = NodeStatus.HEALTHY
            return True
        return False

    def check_cluster_health(self) -> Dict[str, Any]:
        failed = self.heartbeat_service.check_heartbeats(self.node_manager._nodes)
        if self.leader_node and self.leader_node.node_id in failed:
            logger.warning("Leader Node offline! Triggering leader election...")
            self.leader_node = self.heartbeat_service.elect_leader(self.node_manager._nodes)

        return {
            "leader": self.leader_node.node_id if self.leader_node else None,
            "nodes_count": len(self.node_manager._nodes),
            "failed_nodes": failed,
            "topology": self.node_manager.list_nodes()
        }

    def schedule_and_execute_remote_task(self, task_id: str, required_model: Optional[str] = None) -> Dict[str, Any]:
        target_node = self.scheduler.schedule_task(
            list(self.node_manager._nodes.values()),
            required_model=required_model
        )
        return self.remote_executor.dispatch_remote_task(task_id, target_node, {"task_id": task_id})

    def replicate_semantic_memory(self, content: str, source_node_id: str) -> MemoryItem:
        """Replicates semantic memory item across cluster nodes."""
        item = MemoryItem(
            content=f"[ClusterReplicated from {source_node_id}] {content}",
            layer="semantic",
            source=source_node_id,
            importance=8
        )
        self.memory_manager.store(item)

        # Propagate distributed system event via EventBus
        self.event_bus.publish(SystemEvent(
            source="ClusterManager",
            type=SystemEventType.MEMORY_CREATED,
            payload={"memory_id": item.memory_id, "layer": "semantic", "replicated_from": source_node_id}
        ))
        return item
