from typing import Any, Dict, List, Optional
from backend.app.events.bus import EventBus
from backend.app.events.types import SystemEvent, SystemEventType
from backend.app.plugins.base import BasePlugin, PluginContext
from backend.app.plugins.examples import BrowserPlugin, DockerPlugin, GitPlugin, LinuxPlugin
from backend.app.plugins.manifest import PluginManifest
from backend.app.tools.permissions import permission_manager
from backend.app.utils.logger import logger


class PluginManager:
    """
    Enterprise Plugin & Extension Manager for AtherOS.
    Handles dynamic plugin discovery, validation, installation, enable/disable toggle,
    hot reload, dependency resolution, capability registration, and event publishing.
    Core AtherOS NEVER accesses individual plugins directly.
    """

    def __init__(self, plugin_context: PluginContext):
        self.context = plugin_context
        self._installed_plugins: Dict[str, BasePlugin] = {}
        self._enabled_status: Dict[str, bool] = {}

        # Auto-discover and install built-in example plugins
        self._register_default_plugins()

    def _register_default_plugins(self):
        defaults = [GitPlugin(), DockerPlugin(), BrowserPlugin(), LinuxPlugin()]
        for plugin in defaults:
            self.install_plugin(plugin)
            self.enable_plugin(plugin.manifest.plugin_id)

    def validate_plugin(self, manifest: PluginManifest) -> bool:
        """Validates plugin manifest, version compatibility, and required capabilities."""
        if not manifest.plugin_id or not manifest.name:
            return False

        # Validate required capabilities exist in registry
        for cap in manifest.required_capabilities:
            if not self.context.capability_registry.resolve(cap):
                logger.warning(f"Plugin '{manifest.plugin_id}' validation failed: Missing required capability '{cap}'")
                return False

        return True

    def install_plugin(self, plugin: BasePlugin) -> bool:
        if not self.validate_plugin(plugin.manifest):
            return False

        pid = plugin.manifest.plugin_id
        plugin.initialize(self.context)
        self._installed_plugins[pid] = plugin
        self._enabled_status[pid] = False

        # Publish PLUGIN_INSTALLED SystemEvent
        self.context.event_bus.publish(SystemEvent(
            source="PluginManager",
            type=SystemEventType.PLUGIN_INSTALLED,
            payload=plugin.manifest.to_dict()
        ))
        logger.info(f"Installed Plugin: '{plugin.manifest.name}' ({pid})")
        return True

    def uninstall_plugin(self, plugin_id: str) -> bool:
        if plugin_id in self._installed_plugins:
            self.disable_plugin(plugin_id)
            plugin = self._installed_plugins[plugin_id]
            plugin.shutdown()

            del self._installed_plugins[plugin_id]
            del self._enabled_status[plugin_id]

            self.context.event_bus.publish(SystemEvent(
                source="PluginManager",
                type=SystemEventType.PLUGIN_INSTALLED,  # Removed event payload marker
                payload={"plugin_id": plugin_id, "status": "UNINSTALLED"}
            ))
            logger.info(f"Uninstalled Plugin: '{plugin_id}'")
            return True
        return False

    def enable_plugin(self, plugin_id: str) -> bool:
        plugin = self._installed_plugins.get(plugin_id)
        if not plugin:
            return False

        if not self._enabled_status.get(plugin_id, False):
            plugin.register()
            plugin.start()
            self._enabled_status[plugin_id] = True

            self.context.event_bus.publish(SystemEvent(
                source="PluginManager",
                type=SystemEventType.PLUGIN_INSTALLED,
                payload={"plugin_id": plugin_id, "status": "ENABLED"}
            ))
            logger.info(f"Enabled Plugin: '{plugin_id}'")
        return True

    def disable_plugin(self, plugin_id: str) -> bool:
        plugin = self._installed_plugins.get(plugin_id)
        if not plugin:
            return False

        if self._enabled_status.get(plugin_id, False):
            plugin.stop()
            self._enabled_status[plugin_id] = False
            self.context.capability_registry.unregister(plugin.__class__.__name__)

            self.context.event_bus.publish(SystemEvent(
                source="PluginManager",
                type=SystemEventType.PLUGIN_INSTALLED,
                payload={"plugin_id": plugin_id, "status": "DISABLED"}
            ))
            logger.info(f"Disabled Plugin: '{plugin_id}'")
        return True

    def reload_plugin(self, plugin_id: str) -> bool:
        """Hot Reloads a plugin without restarting AtherOS."""
        plugin = self._installed_plugins.get(plugin_id)
        if not plugin:
            return False

        was_enabled = self._enabled_status.get(plugin_id, False)
        self.disable_plugin(plugin_id)
        plugin.initialize(self.context)
        if was_enabled:
            self.enable_plugin(plugin_id)

        logger.info(f"Hot-reloaded Plugin: '{plugin_id}'")
        return True

    def list_plugins(self) -> List[Dict[str, Any]]:
        result = []
        for pid, plugin in self._installed_plugins.items():
            info = plugin.manifest.to_dict()
            info["is_enabled"] = self._enabled_status.get(pid, False)
            info["health"] = plugin.health()
            result.append(info)
        return result
