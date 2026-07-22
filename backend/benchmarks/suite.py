"""
AtherOS v1.0.0-rc1 — Benchmark Suite

Measures latency and throughput for all core AtherOS subsystems.
Each benchmark runs N iterations and reports min/max/avg/p95/p99.
"""
from __future__ import annotations

import statistics
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class BenchmarkResult:
    """Result for a single benchmark run."""
    name: str
    iterations: int
    times_ms: List[float] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def min_ms(self) -> float:
        return min(self.times_ms) if self.times_ms else 0.0

    @property
    def max_ms(self) -> float:
        return max(self.times_ms) if self.times_ms else 0.0

    @property
    def avg_ms(self) -> float:
        return statistics.mean(self.times_ms) if self.times_ms else 0.0

    @property
    def p95_ms(self) -> float:
        if not self.times_ms:
            return 0.0
        sorted_t = sorted(self.times_ms)
        idx = max(0, int(len(sorted_t) * 0.95) - 1)
        return sorted_t[idx]

    @property
    def p99_ms(self) -> float:
        if not self.times_ms:
            return 0.0
        sorted_t = sorted(self.times_ms)
        idx = max(0, int(len(sorted_t) * 0.99) - 1)
        return sorted_t[idx]

    @property
    def ops_per_second(self) -> float:
        total_s = sum(self.times_ms) / 1000.0
        return self.iterations / total_s if total_s > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "iterations": self.iterations,
            "min_ms": round(self.min_ms, 3),
            "max_ms": round(self.max_ms, 3),
            "avg_ms": round(self.avg_ms, 3),
            "p95_ms": round(self.p95_ms, 3),
            "p99_ms": round(self.p99_ms, 3),
            "ops_per_second": round(self.ops_per_second, 2),
            "error": self.error,
        }


class BenchmarkSuite:
    """
    AtherOS production benchmark suite.

    Usage:
        suite = BenchmarkSuite(engine=engine)
        results = suite.run_all()
    """

    def __init__(self, engine: Any = None, iterations: int = 10) -> None:
        self._engine = engine
        self._iterations = iterations

    def _time_fn(self, name: str, fn: Callable, n: int) -> BenchmarkResult:
        result = BenchmarkResult(name=name, iterations=n)
        for _ in range(n):
            t0 = time.monotonic()
            try:
                fn()
            except Exception as exc:
                result.error = str(exc)
                break
            result.times_ms.append((time.monotonic() - t0) * 1000)
        return result

    # ─── Individual benchmarks ────────────────────────────────────────

    def bench_goal_execution(self) -> BenchmarkResult:
        """Goal execution end-to-end latency."""
        def _run():
            if self._engine:
                self._engine.execute_goal("benchmark test goal")

        return self._time_fn("goal_execution_latency", _run, max(1, self._iterations // 3))

    def bench_memory_retrieval(self) -> BenchmarkResult:
        """Memory retrieval latency — 100 iterations."""
        def _run():
            if self._engine:
                self._engine.memory_manager.retrieve(layer="semantic", limit=10)

        return self._time_fn("memory_retrieval_latency", _run, min(100, self._iterations * 10))

    def bench_graph_traversal(self) -> BenchmarkResult:
        """Knowledge graph BFS traversal latency."""
        def _run():
            if self._engine:
                nodes = list(self._engine.context_manager._graph._nodes.keys())
                if nodes:
                    self._engine.context_manager.traverse(nodes[0], depth=3, mode="bfs")

        return self._time_fn("graph_traversal_latency", _run, min(50, self._iterations * 5))

    def bench_agent_dispatch(self) -> BenchmarkResult:
        """Agent task dispatch throughput."""
        def _run():
            if self._engine:
                self._engine.agent_manager.dispatch_task(
                    "ResearchAgent",
                    {"description": "benchmark task", "tool": None, "tool_input": {}, "depends_on": []}
                )

        return self._time_fn("agent_dispatch_latency", _run, self._iterations)

    def bench_event_bus_throughput(self) -> BenchmarkResult:
        """EventBus publish/subscribe cycle throughput — 1000 events."""
        from backend.app.events.bus import EventBus
        from backend.app.events.types import SystemEvent, SystemEventType

        bus = EventBus()
        received = []
        bus.subscribe(SystemEventType.SYSTEM_READY, lambda e: received.append(e))

        def _run():
            bus.publish(SystemEvent(source="benchmark", type=SystemEventType.SYSTEM_READY, payload={}))

        return self._time_fn("event_bus_throughput", _run, 1000)

    def bench_plugin_loading(self) -> BenchmarkResult:
        """Plugin manager list_plugins latency."""
        def _run():
            if self._engine:
                self._engine.plugin_manager.list_plugins()

        return self._time_fn("plugin_loading_latency", _run, min(20, self._iterations * 2))

    def bench_model_routing(self) -> BenchmarkResult:
        """Model orchestrator route() latency."""
        def _run():
            if self._engine:
                self._engine.model_manager.route("fastest")

        return self._time_fn("model_routing_latency", _run, min(20, self._iterations * 2))

    def bench_cluster_heartbeat(self) -> BenchmarkResult:
        """Cluster heartbeat round-trip latency."""
        def _run():
            if self._engine:
                self._engine.cluster_manager.heartbeat("node-leader-01")

        return self._time_fn("cluster_heartbeat_latency", _run, min(50, self._iterations * 5))

    def bench_memory_store(self) -> BenchmarkResult:
        """Memory store() write throughput."""
        from backend.app.memory.memory_item import MemoryItem

        def _run():
            if self._engine:
                self._engine.memory_manager.store(MemoryItem(
                    content="benchmark semantic fact",
                    layer="semantic",
                    source="BENCHMARK",
                    importance=3,
                ))

        return self._time_fn("memory_store_throughput", _run, min(50, self._iterations * 5))

    # ─── Run all ──────────────────────────────────────────────────────

    def run_all(self) -> List[BenchmarkResult]:
        """Run the full benchmark suite and return all results."""
        benchmarks = [
            self.bench_goal_execution,
            self.bench_memory_retrieval,
            self.bench_memory_store,
            self.bench_graph_traversal,
            self.bench_agent_dispatch,
            self.bench_event_bus_throughput,
            self.bench_plugin_loading,
            self.bench_model_routing,
            self.bench_cluster_heartbeat,
        ]
        results = []
        for bench_fn in benchmarks:
            try:
                result = bench_fn()
            except Exception as exc:
                result = BenchmarkResult(name=bench_fn.__name__, iterations=0, error=str(exc))
            results.append(result)
        return results
