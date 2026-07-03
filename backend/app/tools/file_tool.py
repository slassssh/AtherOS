"""
AtherOS File Tool

Allows AtherOS to interact
with local files.
"""


from pathlib import Path

from backend.app.tools.base import BaseTool
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission

class FileTool(BaseTool):    
    
    metadata = ToolMetadata(
        name="file",
        description="Read and write files",
        category="filesystem",
        permissions=[
            ToolPermission.FILE_ACCESS
        ]
    )


    def execute(
        self,
        action: str,
        path: str,
        content: str | None = None
    ) -> ToolResult:


        try:

            file_path = Path(path)


            if action == "read":

                data = file_path.read_text()

                return ToolResult(
                    success=True,
                    output=data
                )


            if action == "write":

                file_path.write_text(
                    content or ""
                )

                return ToolResult(
                    success=True,
                    output="File written"
                )


            return ToolResult(
                success=False,
                error="Unknown file action"
            )


        except Exception as error:

            return ToolResult(
                success=False,
                error=str(error)
            )