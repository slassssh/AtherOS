"""
AtherOS Code Tool

Understands and edits code files.
"""


from pathlib import Path


from backend.app.tools.base import BaseTool
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission
from backend.app.tools.schema import ToolSchema


class CodeTool(BaseTool):

    metadata = ToolMetadata(
        name="code",
        description="Analyze and modify source code",
        category="development",
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
        path: str,
        **kwargs
    ) -> ToolResult:


        try:

            file_path = Path(path)


            if action == "analyze":

                content = file_path.read_text()


                return ToolResult(
                    True,
                    {
                        "lines": len(
                            content.splitlines()
                        ),

                        "characters": len(
                            content
                        )
                    }
                )


            if action == "append":

                with open(
                    file_path,
                    "a"
                ) as file:

                    file.write(
                        kwargs.get(
                            "content",
                            ""
                        )
                    )


                return ToolResult(
                    True,
                    "Code updated"
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