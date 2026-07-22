"""AtherOS Health Diagnostics — Type definitions."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum
from typing import Any, Dict, List, Optional


class HealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


@dataclass
class ComponentHealth:
    """Health result for a single AtherOS subsystem component."""
    name: str
    status: HealthStatus
    latency_ms: Optional[float] = None
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    checked_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status.value,
            "latency_ms": self.latency_ms,
            "details": self.details,
            "error": self.error,
            "checked_at": self.checked_at.isoformat(),
        }


@dataclass
class HealthReport:
    """Aggregated health report across all AtherOS components."""
    overall: HealthStatus
    components: List[ComponentHealth] = field(default_factory=list)
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    atheros_version: str = "1.0.0-rc1"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall": self.overall.value,
            "atheros_version": self.atheros_version,
            "generated_at": self.generated_at.isoformat(),
            "components": [c.to_dict() for c in self.components],
            "summary": {
                "total": len(self.components),
                "healthy": sum(1 for c in self.components if c.status == HealthStatus.HEALTHY),
                "degraded": sum(1 for c in self.components if c.status == HealthStatus.DEGRADED),
                "critical": sum(1 for c in self.components if c.status == HealthStatus.CRITICAL),
            },
        }
