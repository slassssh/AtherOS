import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from backend.app.core.engine import Engine
from backend.app.events.types import SystemEventType
from backend.app.plugins.examples import BrowserPlugin, DockerPlugin, GitPlugin, LinuxPlugin
from backend.app.plugins.manager import PluginManager
from backend.app.plugins.manifest import PluginManifest


def test_plugin_manifest_dict():
    manifest = PluginManifest(
        plugin_id="test_plug",
        name="Test Plugin",
        version="2.0.0",
        author="Tester",
        description="Testing plugin manifest",
        permissions=["READ_FILES"]
    )

    d = manifest.to_dict()
    assert d["plugin_id"] == "test_plug"
    assert d["version"] == "2.0.0"

    reconstructed = PluginManifest.from_dict(d)
    assert reconstructed.name == "Test Plugin"


def test_plugin_manager_install_enable_disable_uninstall():
    engine = Engine()
    mgr = engine.plugin_manager

    # 4 default plugins installed and enabled
    plugins = mgr.list_plugins()
    assert len(plugins) == 4

    pids = [p["plugin_id"] for p in plugins]
    assert "git_plugin" in pids
    assert "docker_plugin" in pids

    # Disable plugin
    assert mgr.disable_plugin("git_plugin") is True
    assert mgr._enabled_status["git_plugin"] is False

    # Enable plugin
    assert mgr.enable_plugin("git_plugin") is True
    assert mgr._enabled_status["git_plugin"] is True

    # Hot reload plugin
    assert mgr.reload_plugin("git_plugin") is True

    # Uninstall plugin
    assert mgr.uninstall_plugin("git_plugin") is True
    assert len(mgr.list_plugins()) == 3


def test_plugin_validation_failed_for_missing_required_capability():
    engine = Engine()
    mgr = engine.plugin_manager

    invalid_manifest = PluginManifest(
        plugin_id="invalid_plug",
        name="Invalid Plugin",
        version="1.0.0",
        author="Tester",
        description="Requires missing capability",
        required_capabilities=["NonExistentCapability123"]
    )

    class CustomPlugin(GitPlugin):
        def __init__(self):
            super().__init__()
            self.manifest = invalid_manifest

    plug = CustomPlugin()
    assert mgr.install_plugin(plug) is False


def test_engine_plugin_manager_integration():
    engine = Engine()
    mgr = engine.plugin_manager

    # Verify CapabilityRegistry resolves GitPlugin and DockerPlugin
    git_cap = engine.capability_registry.resolve("GitPlugin")
    assert git_cap is not None
    assert git_cap.manifest.name == "Git VCS Integration Plugin"

    docker_cap = engine.capability_registry.resolve("DockerPlugin")
    assert docker_cap is not None
