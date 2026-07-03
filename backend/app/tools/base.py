"""
AtherOS Base Tool
"""


from abc import ABC, abstractmethod

from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.schema import ToolSchema


class BaseTool(ABC):

    metadata: ToolMetadata
    schema: ToolSchema | None = None

    @abstractmethod
    def execute(
        self,
        **kwargs
    ) -> ToolResult:

        pass