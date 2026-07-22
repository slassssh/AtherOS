from typing import Any, Dict
from backend.app.plugins.base import BasePlugin
from backend.app.plugins.manifest import PluginManifest


class GitPlugin(BasePlugin):
    def __init__(self):
        manifest = PluginManifest(
            plugin_id="git_plugin",
            name="Git VCS Integration Plugin",
            version="1.0.0",
            author="AtherOS Platform Team",
            description="Version control, commit logging, and git status tools",
            permissions=["READ_FILES", "WRITE_FILES", "TERMINAL"]
        )
        super().__init__(manifest)

    def register(self) -> None:
        if self.context:
            self.context.capability_registry.register("GitPlugin", self)

    def start(self) -> None:
        self.is_active = True

    def stop(self) -> None:
        self.is_active = False


class DockerPlugin(BasePlugin):
    def __init__(self):
        manifest = PluginManifest(
            plugin_id="docker_plugin",
            name="Docker Container Plugin",
            version="1.0.0",
            author="AtherOS Platform Team",
            description="Container isolation and Docker engine orchestration",
            permissions=["TERMINAL", "NETWORK"]
        )
        super().__init__(manifest)

    def register(self) -> None:
        if self.context:
            self.context.capability_registry.register("DockerPlugin", self)

    def start(self) -> None:
        self.is_active = True

    def stop(self) -> None:
        self.is_active = False


class BrowserPlugin(BasePlugin):
    def __init__(self):
        manifest = PluginManifest(
            plugin_id="browser_plugin",
            name="Browser Automation Plugin",
            version="1.0.0",
            author="AtherOS Platform Team",
            description="Web browsing, DOM extraction, and page rendering",
            permissions=["NETWORK", "READ_FILES"]
        )
        super().__init__(manifest)

    def register(self) -> None:
        if self.context:
            self.context.capability_registry.register("BrowserPlugin", self)

    def start(self) -> None:
        self.is_active = True

    def stop(self) -> None:
        self.is_active = False


class LinuxPlugin(BasePlugin):
    def __init__(self):
        manifest = PluginManifest(
            plugin_id="linux_plugin",
            name="Linux OS Utilities Plugin",
            version="1.0.0",
            author="AtherOS Platform Team",
            description="Linux process management, sysfs inspection, and shell tools",
            permissions=["TERMINAL", "READ_FILES"]
        )
        super().__init__(manifest)

    def register(self) -> None:
        if self.context:
            self.context.capability_registry.register("LinuxPlugin", self)

    def start(self) -> None:
        self.is_active = True

    def stop(self) -> None:
        self.is_active = False
