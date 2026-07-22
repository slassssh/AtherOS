# AtherOS v1.0.0-rc1 — Plugin SDK Guide

## Overview

AtherOS plugins are self-contained Python packages that extend the system with new capabilities. The engine discovers and loads them dynamically via `PluginManager` — the core system **never** imports individual plugins directly.

---

## Plugin Manifest

Every plugin must define a `PluginManifest`:

```python
from backend.app.plugins.manifest import PluginManifest

manifest = PluginManifest(
    plugin_id="my_plugin",
    name="My Plugin",
    version="1.0.0",
    author="Your Name",
    description="What this plugin does.",
    license="MIT",
    entry_point="my_plugin.plugin.MyPlugin",
    permissions=["memory:read", "memory:write"],
    required_capabilities=["MemoryManager"],
    optional_capabilities=["ModelManager"],
    dependencies=[],
    minimum_atheros_version="1.0.0",
)
```

---

## BasePlugin Interface

```python
from backend.app.plugins.base import BasePlugin, PluginContext

class MyPlugin(BasePlugin):
    
    @property
    def manifest(self) -> PluginManifest:
        return manifest  # defined above
    
    def on_load(self, context: PluginContext) -> None:
        """Called when plugin is first loaded. Store context."""
        self._context = context
        self._memory = context.memory_manager
    
    def on_enable(self) -> None:
        """Called when plugin is enabled. Start background tasks here."""
        pass
    
    def on_disable(self) -> None:
        """Called when plugin is disabled. Pause operations."""
        pass
    
    def on_unload(self) -> None:
        """Called when plugin is unloaded. Clean up resources."""
        pass
    
    def execute(self, action: str, payload: dict) -> dict:
        """Main execution entrypoint called by the engine."""
        return {"status": "ok", "action": action}
    
    def health(self) -> dict:
        """Return plugin health status."""
        return {"status": "HEALTHY"}
```

---

## PluginContext

The `PluginContext` provides access to core AtherOS subsystems:

```python
context.memory_manager     # MemoryManager — store/retrieve memory
context.context_manager    # ContextManager — knowledge graph
context.agent_manager      # AgentManager — dispatch tasks to agents
context.capability_registry # CapabilityRegistry — discover subsystems
context.event_bus          # EventBus — publish/subscribe events
context.journal            # Journal — log events
```

---

## Plugin Lifecycle

```
install_plugin() → validate_plugin() → load_plugin() → enable_plugin()
                                                              ↓
disable_plugin() ← unload_plugin() ← uninstall_plugin() ←──┘
                        ↑
                  reload_plugin()
```

---

## Permissions

Plugins declare required permissions in their manifest:

| Permission | Access |
|------------|--------|
| `memory:read` | Read from any memory layer |
| `memory:write` | Write to any memory layer |
| `graph:read` | Query the knowledge graph |
| `graph:write` | Modify the knowledge graph |
| `tools:execute` | Invoke registered tools |
| `events:publish` | Publish system events |
| `agents:dispatch` | Dispatch tasks to agents |

---

## Installing a Plugin

```python
from backend.app.plugins.manager import PluginManager
from backend.app.plugins.base import PluginContext

context = PluginContext(...)
pm = PluginManager(context)

# Install and enable
pm.install_plugin(manifest)
pm.enable_plugin("my_plugin")

# List installed plugins
plugins = pm.list_plugins()

# Disable / uninstall
pm.disable_plugin("my_plugin")
pm.uninstall_plugin("my_plugin")
```
