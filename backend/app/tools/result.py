"""
AtherOS Tool Result

Standard output format
for every tool execution.
"""


from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:

    success: bool

    output: Any = None

    error: str | None = None