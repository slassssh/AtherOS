"""
AtherOS v1.0.0-rc1 — Crash Reporter

Captures unhandled exceptions and writes structured crash dumps to disk.
Crash dumps include: exception info, platform metadata, AtherOS version,
recent EventBus history, recent agent activity, and memory statistics.
"""
from __future__ import annotations

import json
import platform
import sys
import traceback
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4


class CrashReporter:
    """
    Global crash handler for AtherOS.

    Usage:
        reporter = CrashReporter()
        reporter.install_global_handler()
    """

    def __init__(self, crash_dir: Optional[Path] = None) -> None:
        self._crash_dir = crash_dir or Path("logs") / "crashes"
        self._crash_dir.mkdir(parents=True, exist_ok=True)
        self._recent_dumps: List[Path] = []

        # Optional live subsystem references (injected at runtime)
        self._event_bus: Any = None
        self._agent_manager: Any = None
        self._memory_manager: Any = None

    def attach_subsystems(
        self,
        event_bus: Any = None,
        agent_manager: Any = None,
        memory_manager: Any = None,
    ) -> None:
        """Attach live subsystem references for richer crash dumps."""
        self._event_bus = event_bus
        self._agent_manager = agent_manager
        self._memory_manager = memory_manager

    def install_global_handler(self) -> None:
        """
        Register as sys.excepthook so all unhandled exceptions are captured.
        The original excepthook is called after the crash dump is written.
        """
        original_hook = sys.excepthook

        def _handler(exc_type, exc_value, exc_tb):
            try:
                dump_path = self.generate_crash_dump(exc_value, exc_tb)
                print(  # noqa: T201
                    f"\n[AtherOS CrashReporter] Crash dump written to: {dump_path}\n",
                    file=sys.stderr,
                )
            except Exception as dump_err:
                print(f"[AtherOS CrashReporter] Failed to write crash dump: {dump_err}", file=sys.stderr)
            original_hook(exc_type, exc_value, exc_tb)

        sys.excepthook = _handler

    def generate_crash_dump(self, exc: BaseException, tb=None) -> Path:
        """
        Write a structured JSON crash dump and return its path.
        """
        crash_id = str(uuid4())[:8]
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        dump_path = self._crash_dir / f"crash_{timestamp}_{crash_id}.json"

        tb_str = traceback.format_tb(tb) if tb else traceback.format_exception(type(exc), exc, exc.__traceback__)

        dump: Dict[str, Any] = {
            "crash_id": crash_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "atheros_version": self._get_atheros_version(),
            "exception": {
                "type": type(exc).__name__,
                "message": str(exc),
                "traceback": tb_str,
            },
            "platform": self._collect_platform_info(),
            "recent_events": self._collect_recent_events(),
            "recent_agent_activity": self._collect_agent_activity(),
            "memory_stats": self._collect_memory_stats(),
        }

        try:
            with dump_path.open("w", encoding="utf-8") as fh:
                json.dump(dump, fh, indent=2, default=str)
            self._recent_dumps.append(dump_path)
        except OSError:
            pass

        return dump_path

    def get_recent_dumps(self, n: int = 5) -> List[Path]:
        """Return the N most recent crash dump paths (in-memory list, not disk scan)."""
        return self._recent_dumps[-n:]

    def scan_crash_dumps(self) -> List[Path]:
        """Scan crash dump directory and return all .json files sorted by mtime."""
        dumps = sorted(self._crash_dir.glob("crash_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        return dumps

    # ─── Private collectors ───────────────────────────────────────────

    @staticmethod
    def _get_atheros_version() -> str:
        try:
            from backend.app.config.config import settings
            return settings.version
        except Exception:
            return "unknown"

    @staticmethod
    def _collect_platform_info() -> Dict[str, Any]:
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "python_version": sys.version,
            "executable": sys.executable,
        }

    def _collect_recent_events(self, limit: int = 50) -> List[Dict]:
        if self._event_bus is None:
            return []
        try:
            events = self._event_bus.history(limit=limit)
            return [
                {
                    "type": e.type.value if hasattr(e.type, "value") else str(e.type),
                    "source": e.source,
                    "timestamp": e.timestamp.isoformat() if hasattr(e, "timestamp") else None,
                }
                for e in events
            ]
        except Exception:
            return []

    def _collect_agent_activity(self, limit: int = 10) -> List[Dict]:
        if self._agent_manager is None:
            return []
        try:
            agents = self._agent_manager.monitor_agents()
            return agents[:limit] if isinstance(agents, list) else []
        except Exception:
            return []

    def _collect_memory_stats(self) -> Dict[str, Any]:
        if self._memory_manager is None:
            return {}
        try:
            return self._memory_manager.stats()
        except Exception:
            return {}


# Module-level singleton
crash_reporter = CrashReporter()
