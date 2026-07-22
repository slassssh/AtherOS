from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from backend.app.agents.manager import AgentManager
from backend.app.context.manager import ContextManager
from backend.app.core.journal import Journal
from backend.app.events.bus import EventBus
from backend.app.memory.manager import MemoryManager
from backend.app.plugins.manifest import PluginManifest
from backend.app.registry.capabilities import CapabilityRegistry


class PluginContext:
    """
    Public Plugin Context API Gateway.
    Plugins access ONLY these public interfaces and never internal implementation details.
    """

    def __init__(
        self,
        memory_manager: MemoryManager,
        context_manager: ContextManager,
        agent_manager: AgentManager,
        capability_registry: CapabilityRegistry,
        event_bus: EventBus,
        journal: Journal,
    ):
        self.memory_manager = memory_manager
        self.context_manager = context_manager
        self.agent_manager = agent_manager
        self.capability_registry = capability_registry
        self.event_bus = event_bus
        self.journal = journal


class BasePlugin(ABC):
    """
    Abstract Base Class for all AtherOS Extensions.
    Plugins implement initialize, register, start, stop, shutdown, and health.
    """

    def __init__(self, manifest: PluginManifest):
        self.manifest = manifest
        self.context: Optional[PluginContext] = None
        self.is_active = False

    def initialize(self, plugin_context: PluginContext) -> None:
        self.context = plugin_context

    @abstractmethod
    def register(self) -> None:
        """Registers plugin capabilities with CapabilityRegistry."""
        pass

    @abstractmethod
    def start(self) -> None:
        """Starts plugin execution routines."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stops plugin execution routines."""
        pass

    def shutdown(self) -> None:
        """Cleans up plugin resources upon uninstallation."""
        self.stop()

    def health(self) -> Dict[str, str]:
        return {
            "plugin_id": self.manifest.plugin_id,
            "status": "ACTIVE" if self.is_active else "INACTIVE",
            "version": self.manifest.version
        }
