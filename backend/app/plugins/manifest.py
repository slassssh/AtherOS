from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PluginManifest:
    """
    Standardized Enterprise Plugin Manifest Metadata.
    Defines identification, capabilities, permissions, and dependencies for a plugin.
    """

    plugin_id: str
    name: str
    version: str
    author: str
    description: str
    license: str = "MIT"
    entry_point: str = "main.py"
    permissions: List[str] = field(default_factory=list)
    required_capabilities: List[str] = field(default_factory=list)
    optional_capabilities: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    minimum_atheros_version: str = "0.1.0"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plugin_id": self.plugin_id,
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "license": self.license,
            "entry_point": self.entry_point,
            "permissions": self.permissions,
            "required_capabilities": self.required_capabilities,
            "optional_capabilities": self.optional_capabilities,
            "dependencies": self.dependencies,
            "minimum_atheros_version": self.minimum_atheros_version,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PluginManifest":
        return cls(
            plugin_id=data["plugin_id"],
            name=data["name"],
            version=data.get("version", "1.0.0"),
            author=data.get("author", "Unknown"),
            description=data.get("description", ""),
            license=data.get("license", "MIT"),
            entry_point=data.get("entry_point", "main.py"),
            permissions=data.get("permissions", []),
            required_capabilities=data.get("required_capabilities", []),
            optional_capabilities=data.get("optional_capabilities", []),
            dependencies=data.get("dependencies", []),
            minimum_atheros_version=data.get("minimum_atheros_version", "0.1.0"),
        )
