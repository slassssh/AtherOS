"""AtherOS Benchmark Reporter — Exports results to JSON + Markdown."""
from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path
from typing import List

from backend.benchmarks.suite import BenchmarkResult


class BenchmarkReporter:
    """Exports benchmark results to JSON and Markdown formats."""

    def __init__(self, output_dir: Path = Path(".")) -> None:
        self._output_dir = output_dir
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, results: List[BenchmarkResult]) -> dict:
        """Export results to benchmark_report.json and benchmark_report.md. Returns JSON dict."""
        try:
            from backend.app.config.config import settings
            version = settings.version
        except Exception:
            version = "1.0.0-rc1"

        report = {
            "atheros_version": version,
            "generated_at": datetime.now(UTC).isoformat(),
            "results": [r.to_dict() for r in results],
        }

        json_path = self._output_dir / "benchmark_report.json"
        json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

        md_path = self._output_dir / "benchmark_report.md"
        md_path.write_text(self._render_markdown(report), encoding="utf-8")

        return report

    @staticmethod
    def _render_markdown(report: dict) -> str:
        lines = [
            f"# AtherOS Benchmark Report",
            f"",
            f"**Version**: `{report['atheros_version']}`  ",
            f"**Generated**: {report['generated_at']}",
            f"",
            f"| Benchmark | Iterations | Avg (ms) | P95 (ms) | P99 (ms) | Ops/s | Error |",
            f"|-----------|-----------|----------|----------|----------|-------|-------|",
        ]
        for r in report["results"]:
            err = r["error"] or ""
            lines.append(
                f"| {r['name']} | {r['iterations']} | {r['avg_ms']} | {r['p95_ms']} | "
                f"{r['p99_ms']} | {r['ops_per_second']} | {err} |"
            )
        return "\n".join(lines) + "\n"
