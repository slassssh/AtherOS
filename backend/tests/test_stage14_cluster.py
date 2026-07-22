import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from backend.app.cluster.manager import ClusterManager
from backend.app.cluster.types import NodeRole, NodeSpec, NodeStatus
from backend.app.core.engine import Engine


def test_cluster_node_registration_and_heartbeat():
    cm = ClusterManager()
    new_node = NodeSpec(node_id="worker-99", address="10.0.0.99:9090", role=NodeRole.WORKER)
    cm.node_manager.register_node(new_node)

    assert cm.heartbeat("worker-99") is True
    assert cm.node_manager.get_node("worker-99").status == NodeStatus.HEALTHY


def test_distributed_scheduler_selection():
    cm = ClusterManager()

    # Schedule task requiring claude-3-5-sonnet
    target = cm.scheduler.schedule_task(
        list(cm.node_manager._nodes.values()),
        required_model="claude-3-5-sonnet"
    )
    assert target.node_id == "node-worker-03"


from datetime import datetime, timedelta, UTC

def test_heartbeat_timeout_and_leader_election():
    cm = ClusterManager()
    leader = cm.leader_node
    assert leader is not None

    # Simulate leader heartbeat timeout (15 seconds in the past)
    leader.last_heartbeat = datetime.now(UTC) - timedelta(seconds=15)
    health = cm.check_cluster_health()

    assert health["leader"] != leader.node_id
    assert health["leader"] is not None
    assert cm.leader_node.role == NodeRole.LEADER


def test_remote_execution():
    cm = ClusterManager()

    res = cm.schedule_and_execute_remote_task("task-100", required_model="llama3-8b")
    assert res["status"] == "COMPLETED"
    assert res["executed_by"] in ["node-leader-01", "node-worker-02"]


def test_semantic_memory_replication():
    cm = ClusterManager()

    item = cm.replicate_semantic_memory("Global Security Compliance Rule #42", source_node_id="node-worker-02")
    assert item is not None
    assert item.layer == "semantic"
    assert "[ClusterReplicated from node-worker-02]" in item.content


def test_engine_cluster_manager_capability_integration():
    engine = Engine()
    cap = engine.capability_registry.resolve("ClusterManager")
    assert cap is not None
    health = cap.check_cluster_health()
    assert health["nodes_count"] >= 3
