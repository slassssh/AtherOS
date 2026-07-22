import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from backend.app.core.engine import Engine
from backend.app.llm.orchestrator import ModelManager, ModelSpec, RoutingPolicy


def test_model_manager_registration_and_removal():
    mgr = ModelManager()
    custom_spec = ModelSpec("custom-local-mistral", "local", context_window=64000, is_local=True, latency_ms=30.0)
    mgr.register_model(custom_spec)

    health = mgr.health()
    assert "custom-local-mistral" in health
    assert health["custom-local-mistral"] == "HEALTHY"

    assert mgr.remove_model("custom-local-mistral") is True
    assert "custom-local-mistral" not in mgr.health()


def test_model_manager_routing_policies():
    mgr = ModelManager()

    # FASTEST policy selects llama3-8b (latency ~45ms)
    fastest = mgr.select_best_model(RoutingPolicy.FASTEST)
    assert fastest.model_id == "llama3-8b"

    # LOWEST_COST policy selects llama3-8b or deepseek-r1-local (cost 0.0)
    cheapest = mgr.select_best_model(RoutingPolicy.LOWEST_COST)
    assert cheapest.is_local is True or cheapest.cost_per_1k_input == 0.0

    # HIGHEST_QUALITY policy selects claude-3-5-sonnet (quality 9.8)
    best_quality = mgr.select_best_model(RoutingPolicy.HIGHEST_QUALITY)
    assert best_quality.model_id == "claude-3-5-sonnet"

    # SECURITY_ONLY policy selects only local models
    security_model = mgr.select_best_model(RoutingPolicy.SECURITY_ONLY)
    assert security_model.is_local is True


def test_model_manager_route_execution_and_telemetry():
    mgr = ModelManager()

    res = mgr.route(prompt="Hello AtherOS AI Orchestrator!", policy=RoutingPolicy.FASTEST)
    assert res is not None
    assert len(res.text) > 0

    stats = mgr.usage_stats()
    assert stats["total_requests"] == 1
    assert stats["total_tokens"] > 0


def test_model_manager_failover_and_fallback():
    mgr = ModelManager()

    # Simulate failure on gpt-4o and fallback
    res = mgr.fallback(prompt="Test fallback prompt", failed_model_id="gpt-4o")
    assert res is not None
    assert mgr.health()["gpt-4o"] == "UNHEALTHY"


def test_model_manager_benchmark():
    mgr = ModelManager()

    results = mgr.benchmark("llama3-8b")
    assert results["model_id"] == "llama3-8b"
    assert results["status"] == "HEALTHY"


def test_engine_model_manager_capability_integration():
    engine = Engine()
    cap = engine.capability_registry.resolve("ModelManager")
    assert cap is not None
    assert len(cap.health()) >= 6
