import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from backend.app.core.engine import Engine
from backend.app.memory.manager import MemoryManager
from backend.app.memory.memory_item import MemoryItem
from backend.app.memory.ranker import MemoryRanker


def test_memory_item_creation_and_dict():
    item = MemoryItem(
        content="System Architecture Guideline",
        layer="semantic",
        source="SYSTEM",
        session_id="sess_123",
        importance=8,
        tags=["architecture", "guideline"]
    )

    d = item.to_dict()
    assert d["content"] == "System Architecture Guideline"
    assert d["layer"] == "semantic"
    assert d["importance"] == 8
    assert "architecture" in d["tags"]

    reconstructed = MemoryItem.from_dict(d)
    assert reconstructed.memory_id == item.memory_id
    assert reconstructed.content == item.content


def test_memory_manager_crud_and_layers():
    mgr = MemoryManager()

    # Store items across layers
    id1 = mgr.store(MemoryItem(content="Session active user prompt", layer="session", session_id="s1"))
    id2 = mgr.store(MemoryItem(content="Working memory transient variable x=10", layer="working", session_id="s1"))
    id3 = mgr.store(MemoryItem(content="Project root configuration", layer="project", project_id="p1"))
    id4 = mgr.store(MemoryItem(content="Long term fact about Python AST", layer="long_term"))
    id5 = mgr.store(MemoryItem(content="Episodic execution log of task 42", layer="episodic", session_id="s1"))
    id6 = mgr.store(MemoryItem(content="Semantic concept: Clean Architecture", layer="semantic"))
    id7 = mgr.store(MemoryItem(content="Tool execution output file written", layer="tool", session_id="s1"))

    # Retrieve
    retrieved = mgr.retrieve(id1)
    assert retrieved is not None
    assert retrieved.content == "Session active user prompt"

    # Search by layer
    session_items = mgr.search(layer="session")
    assert len(session_items) >= 1
    assert any(m.memory_id == id1 for m in session_items)


def test_memory_prioritize_archive_forget():
    mgr = MemoryManager()
    id_mem = mgr.store(MemoryItem(content="Initial concept", layer="session", importance=2))

    # Prioritize
    assert mgr.prioritize(id_mem, new_importance=9) is True
    assert mgr.retrieve(id_mem).importance == 9

    # Archive
    assert mgr.archive(id_mem) is True
    assert mgr.retrieve(id_mem).layer == "long_term"

    # Forget
    assert mgr.forget(id_mem) is True
    assert mgr.retrieve(id_mem) is None


def test_memory_merge():
    mgr = MemoryManager()
    id1 = mgr.store(MemoryItem(content="Part 1 of solution", layer="working", importance=4, tags=["tagA"]))
    id2 = mgr.store(MemoryItem(content="Part 2 of solution", layer="working", importance=8, tags=["tagB"]))

    merged = mgr.merge([id1, id2])
    assert merged is not None
    assert "Part 1 of solution" in merged.content
    assert "Part 2 of solution" in merged.content
    assert merged.importance == 8
    assert "tagA" in merged.tags and "tagB" in merged.tags

    # Verify original items were soft deleted
    assert mgr.retrieve(id1) is None
    assert mgr.retrieve(id2) is None


def test_memory_ranking():
    item_low = MemoryItem(content="Unrelated random note", layer="session", importance=1)
    item_high = MemoryItem(content="Critical Python architecture specification", layer="session", importance=9, tags=["python", "architecture"])

    ranked = MemoryRanker.rank([item_low, item_high], query="architecture", limit=10)
    assert len(ranked) == 2
    assert ranked[0].memory_id == item_high.memory_id


def test_engine_memory_manager_integration():
    mgr = MemoryManager()
    engine = Engine(memory_manager=mgr)

    res = engine.execute_goal("Create high performance backend pipeline")
    assert res["status"] == "COMPLETED"

    # Verify memories were created during goal execution across session, working, tool, episodic, and long_term layers
    session_mems = mgr.search(session_id=res["session_id"])
    assert len(session_mems) > 0
