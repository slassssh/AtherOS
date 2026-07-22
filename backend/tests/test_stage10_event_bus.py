import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from backend.app.api.websocket import WebSocketManager
from backend.app.core.engine import Engine
from backend.app.events.bus import EventBus
from backend.app.events.types import SystemEvent, SystemEventType
from backend.app.registry.capabilities import CapabilityRegistry


def test_immutable_system_event():
    evt = SystemEvent(
        source="TestAgent",
        type=SystemEventType.GOAL_CREATED,
        payload={"goal": "Harden Event Bus"},
        priority=9,
        correlation_id="corr_100"
    )

    d = evt.to_dict()
    assert d["source"] == "TestAgent"
    assert d["type"] == "GOAL_CREATED"
    assert d["correlation_id"] == "corr_100"

    # Verify immutability
    with pytest.raises(Exception):
        evt.source = "ModifiedAgent"  # Frozen dataclass mutation raises exception


def test_event_bus_pub_sub_and_wildcard():
    bus = EventBus()
    received_events = []
    wildcard_events = []

    def handle_goal(evt: SystemEvent):
        received_events.append(evt)

    def handle_wildcard(evt: SystemEvent):
        wildcard_events.append(evt)

    bus.subscribe(SystemEventType.GOAL_CREATED, handle_goal)
    bus.subscribe("*", handle_wildcard)

    evt = SystemEvent(source="TestRunner", type=SystemEventType.GOAL_CREATED, payload={"status": "OK"})
    bus.publish(evt)

    assert len(received_events) == 1
    assert len(wildcard_events) == 1
    assert received_events[0].event_id == evt.event_id

    # Unsubscribe
    bus.unsubscribe(SystemEventType.GOAL_CREATED, handle_goal)
    bus.publish(evt)
    assert len(received_events) == 1  # Unsubscribed, count remains 1
    assert len(wildcard_events) == 2  # Wildcard still receives event


def test_event_bus_history_replay_and_filter():
    bus = EventBus()
    evt1 = SystemEvent(source="Engine", type=SystemEventType.TASK_CREATED, payload={"step": 1}, correlation_id="c1")
    evt2 = SystemEvent(source="Agent", type=SystemEventType.TASK_COMPLETED, payload={"step": 2}, correlation_id="c1")
    evt3 = SystemEvent(source="Security", type=SystemEventType.SECURITY_ALERT, payload={"step": 3}, correlation_id="c2")

    bus.publish(evt1)
    bus.publish(evt2)
    bus.publish(evt3)

    assert len(bus.history()) == 3

    # Replay correlation c1
    replayed = bus.replay("c1")
    assert len(replayed) == 2
    assert replayed[0].event_id == evt1.event_id

    # Filter by source
    sec_events = bus.filter(source="Security")
    assert len(sec_events) == 1
    assert sec_events[0].type == SystemEventType.SECURITY_ALERT


def test_capability_registry_discovery_and_health():
    registry = CapabilityRegistry()
    registry.register("Database", instance=None, metadata={"type": "SQLite"})
    registry.register("Memory", instance=None, metadata={"layers": 7})

    discovered = registry.discover()
    assert len(discovered) == 2
    names = [d["name"] for d in discovered]
    assert "Database" in names and "Memory" in names

    health = registry.health()
    assert health["Database"] == "HEALTHY"

    registry.unregister("Database")
    assert registry.resolve("Database") is None


def test_engine_event_bus_and_registry_integration():
    bus = EventBus()
    registry = CapabilityRegistry()
    engine = Engine(event_bus=bus, capability_registry=registry)

    # Verify capabilities auto-registered
    discovered = registry.discover()
    assert len(discovered) >= 6

    # Create session triggers GOAL_CREATED SystemEvent
    session = engine.create_session("Event-Driven Session", "Testing event bus")
    history = bus.history()
    assert len(history) > 0
    assert history[-1].type == SystemEventType.GOAL_CREATED
