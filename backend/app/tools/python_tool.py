"""
AtherOS Python Tool

Executes Python code snippets.
"""


import io
import contextlib

from backend.app.tools.base import BaseTool
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission
from backend.app.tools.schema import ToolSchema


class PythonTool(BaseTool):

    metadata = ToolMetadata(
        name="python",
        description="Execute Python code",
        category="execution",
        permissions=[
            ToolPermission.CODE_EXECUTION
        ]
    )
    schema = ToolSchema(
    required=[
        "code"
    ]
)


    def execute(
        self,
        code: str
    ) -> ToolResult:


        try:

            output = io.StringIO()


            with contextlib.redirect_stdout(output):

                exec(
                    code,
                    {}
                )


            return ToolResult(
                success=True,
                output=output.getvalue()
            )


        except Exception as error:

            return ToolResult(
                success=False,
                error=str(error)
            )