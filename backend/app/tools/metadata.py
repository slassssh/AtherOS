"""
AtherOS Tool Metadata
"""


from dataclasses import dataclass, field

from backend.app.tools.permissions import ToolPermission


@dataclass
class ToolMetadata:

    name: str

    description: str

    category: str

    version: str = "1.0.0"

    permissions: list[ToolPermission] = field(
        default_factory=list
    )

    enabled: bool = True