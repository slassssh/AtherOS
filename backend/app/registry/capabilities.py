from datetime import datetime, UTC
from typing import Any, Dict, List, Optional
from backend.app.utils.logger import logger


class CapabilityRegistry:
    """
    Central Capability Registry for AtherOS.
    Allows all core subsystems (Engine, Planner, Memory, Context, Security, Database, LLM, Agents, Plugins, API, Desktop)
    to register, discover, resolve, and report health status.
    """

    def __init__(self):
        self._capabilities: Dict[str, Dict[str, Any]] = {}

    def register(self, capability_name: str, instance: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        self._capabilities[capability_name] = {
            "name": capability_name,
            "instance": instance,
            "metadata": metadata or {},
            "registered_at": datetime.now(UTC).isoformat(),
            "status": "HEALTHY"
        }
        logger.info(f"Registered Subsystem Capability: {capability_name}")

    def unregister(self, capability_name: str) -> bool:
        if capability_name in self._capabilities:
            del self._capabilities[capability_name]
            logger.info(f"Unregistered Subsystem Capability: {capability_name}")
            return True
        return False

    def resolve(self, capability_name: str) -> Optional[Any]:
        cap = self._capabilities.get(capability_name)
        return cap["instance"] if cap else None

    def discover(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": info["name"],
                "metadata": info["metadata"],
                "registered_at": info["registered_at"],
                "status": info["status"]
            }
            for info in self._capabilities.values()
        ]

    def health(self) -> Dict[str, str]:
        health_report = {}
        for name, info in self._capabilities.items():
            inst = info["instance"]
            # Check if instance exposes a custom health status
            status = "HEALTHY"
            if hasattr(inst, "status"):
                status = str(getattr(inst, "status"))
            health_report[name] = status
        return health_report
