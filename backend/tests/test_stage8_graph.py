import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from backend.app.context.manager import ContextManager
from backend.app.context.types import NodeType, RelationType
from backend.app.core.engine import Engine


def test_node_and_edge_creation():
    ctx = ContextManager()

    # 1. Create nodes
    proj = ctx.create_node(NodeType.PROJECT, "HealixShield", properties={"lang": "Python"})
    goal = ctx.create_node(NodeType.GOAL, "Harden Auth Security", properties={"priority": 1})

    assert proj.label == "HealixShield"
    assert goal.label == "Harden Auth Security"

    # 2. Create edge
    edge = ctx.create_edge(proj.node_id, goal.node_id, RelationType.OWNS)
    assert edge.source_id == proj.node_id
    assert edge.target_id == goal.node_id
    assert edge.relation_type == RelationType.OWNS

    # 3. Duplicate edge prevention
    edge_dup = ctx.create_edge(proj.node_id, goal.node_id, RelationType.OWNS)
    assert edge_dup.edge_id == edge.edge_id


def test_graph_neighbors_and_query():
    ctx = ContextManager()
    user = ctx.create_node(NodeType.USER, "Lead Architect")
    proj1 = ctx.create_node(NodeType.PROJECT, "AtherOS")
    proj2 = ctx.create_node(NodeType.PROJECT, "HealixShield")

    ctx.create_edge(user.node_id, proj1.node_id, RelationType.OWNS)
    ctx.create_edge(user.node_id, proj2.node_id, RelationType.OWNS)

    # Neighbors
    user_neighbors = ctx.neighbors(user.node_id, direction="outgoing")
    assert len(user_neighbors) == 2
    assert any(n.label == "AtherOS" for n in user_neighbors)
    assert any(n.label == "HealixShield" for n in user_neighbors)

    # Query
    projects = ctx.query(node_type=NodeType.PROJECT)
    assert len(projects) >= 2


def test_bfs_dfs_traversal_and_shortest_path():
    ctx = ContextManager()
    n1 = ctx.create_node(NodeType.PROJECT, "Root")
    n2 = ctx.create_node(NodeType.GOAL, "Goal A")
    n3 = ctx.create_node(NodeType.PLAN, "Plan A")
    n4 = ctx.create_node(NodeType.TASK, "Task A1")

    ctx.create_edge(n1.node_id, n2.node_id, RelationType.CREATED)
    ctx.create_edge(n2.node_id, n3.node_id, RelationType.GENERATED)
    ctx.create_edge(n3.node_id, n4.node_id, RelationType.CHILD_OF)

    # BFS Traversal
    bfs_nodes = ctx.traverse(n1.node_id, max_depth=3, strategy="BFS")
    assert len(bfs_nodes) == 3

    # DFS Traversal
    dfs_nodes = ctx.traverse(n1.node_id, max_depth=3, strategy="DFS")
    assert len(dfs_nodes) == 3

    # Shortest Path
    path = ctx.shortest_path(n1.node_id, n4.node_id)
    assert path == [n1.node_id, n2.node_id, n3.node_id, n4.node_id]


def test_context_summarization():
    ctx = ContextManager()
    proj = ctx.create_node(NodeType.PROJECT, "HealixShield")
    goal = ctx.create_node(NodeType.GOAL, "Security Audit")
    ctx.create_edge(proj.node_id, goal.node_id, RelationType.CREATED)

    summary = ctx.summarize_context(proj.node_id)
    assert summary["root"]["label"] == "HealixShield"
    assert summary["outgoing_relationship_count"] == 1
    assert summary["total_connected_neighbors"] == 1


def test_engine_context_manager_integration():
    ctx = ContextManager()
    engine = Engine(context_manager=ctx)

    res = engine.execute_goal("Harden authentication microservice security")
    assert res["status"] == "COMPLETED"

    # Verify Knowledge Graph automatically connected Session -> Goal -> Plan -> Tasks -> Tools
    sess_node = ctx.get_node(res["session_id"])
    assert sess_node is not None

    session_neighbors = ctx.neighbors(res["session_id"], direction="outgoing")
    assert len(session_neighbors) > 0
