"""AtherOS Benchmark CLI entry point: python -m backend.benchmarks"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo root is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.app.core.engine import Engine
from backend.benchmarks.suite import BenchmarkSuite
from backend.benchmarks.reporter import BenchmarkReporter


def main() -> None:
    print("\n🚀 AtherOS v1.0.0-rc1 — Benchmark Suite\n" + "=" * 50)

    engine = Engine()
    suite = BenchmarkSuite(engine=engine, iterations=10)
    results = suite.run_all()

    reporter = BenchmarkReporter(output_dir=Path("."))
    report = reporter.export(results)

    print(f"\n{'Benchmark':<40} {'Avg ms':>8} {'P95 ms':>8} {'Ops/s':>10}")
    print("-" * 70)
    for r in report["results"]:
        err = f" ⚠ {r['error']}" if r["error"] else ""
        print(f"{r['name']:<40} {r['avg_ms']:>8.2f} {r['p95_ms']:>8.2f} {r['ops_per_second']:>10.1f}{err}")

    print(f"\n✅ Reports saved: benchmark_report.json | benchmark_report.md\n")


if __name__ == "__main__":
    main()
