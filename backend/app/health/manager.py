"""
AtherOS v1.0.0-rc1 — Health Manager

Provides unified diagnostics across all AtherOS subsystems:
CPU, Memory, Disk, Database, Plugins, Models, Agents, Cluster, API, Desktop.
"""
from __future__ import annotations

import time
from datetime import datetime, UTC
from typing import Any, List, Optional

from backend.app.health.types import ComponentHealth, HealthReport, HealthStatus
from backend.app.utils.logger import logger

try:
    import psutil
    _PSUTIL_AVAILABLE = True
except ImportError:
    _PSUTIL_AVAILABLE = False


class HealthManager:
    """
    Centralized health diagnostics for AtherOS.

    Usage:
        hm = HealthManager(engine=engine)
        report = hm.full_report()
        print(report.overall)  # HEALTHY | DEGRADED | CRITICAL
    """

    def __init__(
        self,
        engine: Any = None,
        database_connection: Any = None,
    ) -> None:
        self._engine = engine
        self._db = database_connection
        self._api_start_time = datetime.now(UTC)

    # ─── Individual checks ────────────────────────────────────────────

    def check_system(self) -> ComponentHealth:
        """CPU, RAM, and Disk utilization check."""
        name = "system"
        if not _PSUTIL_AVAILABLE:
            return ComponentHealth(name=name, status=HealthStatus.UNKNOWN, error="psutil not installed")

        t0 = time.monotonic()
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/") if hasattr(psutil, "disk_usage") else None

            status = HealthStatus.HEALTHY
            if cpu > 90 or mem.percent > 90:
                status = HealthStatus.CRITICAL
            elif cpu > 70 or mem.percent > 75:
                status = HealthStatus.DEGRADED

            details: dict = {
                "cpu_percent": cpu,
                "ram_percent": mem.percent,
                "ram_available_mb": mem.available // (1024 * 1024),
            }
            if disk:
                details["disk_percent"] = disk.percent
                details["disk_free_gb"] = disk.free // (1024 ** 3)

            return ComponentHealth(
                name=name,
                status=status,
                latency_ms=(time.monotonic() - t0) * 1000,
                details=details,
            )
        except Exception as exc:
            return ComponentHealth(name=name, status=HealthStatus.UNKNOWN, error=str(exc))

    def check_database(self) -> ComponentHealth:
        """Database connectivity and query latency check."""
        name = "database"
        t0 = time.monotonic()
        try:
            if self._db is not None:
                self._db.connect()
                latency = (time.monotonic() - t0) * 1000
                return ComponentHealth(
                    name=name,
                    status=HealthStatus.HEALTHY,
                    latency_ms=latency,
                    details={"connected": True},
                )
            # No DB injected — check SQLite file exists
            from pathlib import Path
            db_path = Path("atheros.db")
            latency = (time.monotonic() - t0) * 1000
            if db_path.exists():
                return ComponentHealth(name=name, status=HealthStatus.HEALTHY, latency_ms=latency,
                                       details={"db_file": str(db_path), "size_bytes": db_path.stat().st_size})
            return ComponentHealth(name=name, status=HealthStatus.DEGRADED, latency_ms=latency,
                                   details={"db_file": str(db_path), "exists": False})
        except Exception as exc:
            return ComponentHealth(name=name, status=HealthStatus.CRITICAL, error=str(exc))

    def check_plugins(self) -> ComponentHealth:
        """Plugin manager health — lists installed plugins and any failures."""
        name = "plugins"
        t0 = time.monotonic()
        try:
            if self._engine and hasattr(self._engine, "plugin_manager"):
                plugins = self._engine.plugin_manager.list_plugins()
                failed = [p for p in plugins if p.get("state") in ("FAILED", "ERROR")]
                status = HealthStatus.HEALTHY if not failed else HealthStatus.DEGRADED
                return ComponentHealth(
                    name=name,
                    status=status,
                    latency_ms=(time.monotonic() - t0) * 1000,
                    details={"total": len(plugins), "failed": len(failed)},
                )
            return ComponentHealth(name=name, status=HealthStatus.UNKNOWN, details={"reason": "PluginManager not attached"})
        except Exception as exc:
            return ComponentHealth(name=name, status=HealthStatus.UNKNOWN, error=str(exc))

    def check_models(self) -> ComponentHealth:
        """Model orchestrator health — checks provider availability."""
        name = "models"
        t0 = time.monotonic()
        try:
            if self._engine and hasattr(self._engine, "model_manager"):
                health = self._engine.model_manager.health()
                providers_up = sum(1 for v in health.values() if v.get("available"))
                total = len(health)
                status = HealthStatus.HEALTHY if providers_up > 0 else HealthStatus.CRITICAL
                if providers_up < total:
                    status = HealthStatus.DEGRADED
                return ComponentHealth(
                    name=name,
                    status=status,
                    latency_ms=(time.monotonic() - t0) * 1000,
                    details={"providers_up": providers_up, "total": total, "providers": health},
                )
            return ComponentHealth(name=name, status=HealthStatus.UNKNOWN, details={"reason": "ModelManager not attached"})
        except Exception as exc:
            return ComponentHealth(name=name, status=HealthStatus.UNKNOWN, error=str(exc))

    def check_agents(self) -> ComponentHealth:
        """Agent runtime health — active vs failed agent count."""
        name = "agents"
        t0 = time.monotonic()
        try:
            if self._engine and hasattr(self._engine, "agent_manager"):
                agents = self._engine.agent_manager.monitor_agents()
                total = len(agents)
                active = sum(1 for a in agents if a.get("status") in ("IDLE", "RUNNING"))
                failed = sum(1 for a in agents if a.get("status") == "FAILED")
                status = HealthStatus.CRITICAL if failed > 0 and active == 0 else (
                    HealthStatus.DEGRADED if failed > 0 else HealthStatus.HEALTHY
                )
                return ComponentHealth(
                    name=name,
                    status=status,
                    latency_ms=(time.monotonic() - t0) * 1000,
                    details={"total": total, "active": active, "failed": failed},
                )
            return ComponentHealth(name=name, status=HealthStatus.UNKNOWN, details={"reason": "AgentManager not attached"})
        except Exception as exc:
            return ComponentHealth(name=name, status=HealthStatus.UNKNOWN, error=str(exc))

    def check_cluster(self) -> ComponentHealth:
        """Cluster topology health — node count, leader, failed nodes."""
        name = "cluster"
        t0 = time.monotonic()
        try:
            if self._engine and hasattr(self._engine, "cluster_manager"):
                health = self._engine.cluster_manager.check_cluster_health()
                failed = health.get("failed_nodes", [])
                nodes = health.get("nodes_count", 0)
                status = HealthStatus.CRITICAL if not health.get("leader") else (
                    HealthStatus.DEGRADED if failed else HealthStatus.HEALTHY
                )
                return ComponentHealth(
                    name=name,
                    status=status,
                    latency_ms=(time.monotonic() - t0) * 1000,
                    details={"nodes": nodes, "leader": health.get("leader"), "failed": failed},
                )
            return ComponentHealth(name=name, status=HealthStatus.UNKNOWN, details={"reason": "ClusterManager not attached"})
        except Exception as exc:
            return ComponentHealth(name=name, status=HealthStatus.UNKNOWN, error=str(exc))

    def check_api(self) -> ComponentHealth:
        """API server uptime check."""
        uptime = (datetime.now(UTC) - self._api_start_time).total_seconds()
        return ComponentHealth(
            name="api",
            status=HealthStatus.HEALTHY,
            latency_ms=0.0,
            details={"uptime_seconds": round(uptime, 1), "started_at": self._api_start_time.isoformat()},
        )

    def check_memory_subsystem(self) -> ComponentHealth:
        """Memory manager health — layer counts and total items."""
        name = "memory"
        t0 = time.monotonic()
        try:
            if self._engine and hasattr(self._engine, "memory_manager"):
                stats = self._engine.memory_manager.stats()
                return ComponentHealth(
                    name=name,
                    status=HealthStatus.HEALTHY,
                    latency_ms=(time.monotonic() - t0) * 1000,
                    details=stats,
                )
            return ComponentHealth(name=name, status=HealthStatus.UNKNOWN)
        except Exception as exc:
            return ComponentHealth(name=name, status=HealthStatus.UNKNOWN, error=str(exc))

    # ─── Full report ──────────────────────────────────────────────────

    def full_report(self) -> HealthReport:
        """Run all health checks and return a unified HealthReport."""
        checks = [
            self.check_system,
            self.check_database,
            self.check_plugins,
            self.check_models,
            self.check_agents,
            self.check_cluster,
            self.check_api,
            self.check_memory_subsystem,
        ]

        components: List[ComponentHealth] = []
        for check in checks:
            try:
                result = check()
            except Exception as exc:
                result = ComponentHealth(name=check.__name__, status=HealthStatus.UNKNOWN, error=str(exc))
            components.append(result)

        # Aggregate overall status
        statuses = {c.status for c in components}
        if HealthStatus.CRITICAL in statuses:
            overall = HealthStatus.CRITICAL
        elif HealthStatus.DEGRADED in statuses:
            overall = HealthStatus.DEGRADED
        elif HealthStatus.UNKNOWN in statuses:
            overall = HealthStatus.DEGRADED
        else:
            overall = HealthStatus.HEALTHY

        try:
            from backend.app.config.config import settings
            version = settings.version
        except Exception:
            version = "1.0.0-rc1"

        report = HealthReport(overall=overall, components=components, atheros_version=version)
        logger.info(f"HealthReport generated: overall={overall.value} | {len(components)} components checked")
        return report
