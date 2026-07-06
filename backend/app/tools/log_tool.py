"""
AtherOS Log Tool

Analyzes application logs.
"""


from pathlib import Path


from backend.app.tools.base import BaseTool
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission
from backend.app.tools.schema import ToolSchema


class LogTool(BaseTool):

    metadata = ToolMetadata(
        name="log",
        description="Analyze log files",
        category="monitoring",
        permissions=[
            ToolPermission.FILE_ACCESS
        ]
    )


    schema = ToolSchema(
        required=[
            "action",
            "path"
        ]
    )


    def execute(
        self,
        action: str,
        path: str
    ) -> ToolResult:


        try:

            log_path = Path(path)


            if action == "analyze":

                content = log_path.read_text()


                errors = content.lower().count(
                    "error"
                )

                warnings = content.lower().count(
                    "warning"
                )


                return ToolResult(
                    True,
                    {
                        "errors": errors,
                        "warnings": warnings
                    }
                )


            return ToolResult(
                False,
                error="Unknown action"
            )


        except Exception as error:

            return ToolResult(
                False,
                error=str(error)
            )