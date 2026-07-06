"""
AtherOS Advanced File Tool

Complete filesystem operations.
"""


from pathlib import Path
import shutil


from backend.app.tools.base import BaseTool
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission
from backend.app.tools.schema import ToolSchema


class FileTool(BaseTool):

    metadata = ToolMetadata(
        name="file",
        description="Advanced filesystem operations",
        category="filesystem",
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


            if action == "read":

                return ToolResult(
                    True,
                    file_path.read_text()
                )


            if action == "write":

                file_path.write_text(
                    kwargs.get(
                        "content",
                        ""
                    )
                )

                return ToolResult(
                    True,
                    "File written"
                )


            if action == "delete":

                file_path.unlink()

                return ToolResult(
                    True,
                    "Deleted"
                )


            if action == "mkdir":

                file_path.mkdir(
                    exist_ok=True
                )

                return ToolResult(
                    True,
                    "Folder created"
                )


            if action == "list":

                return ToolResult(
                    True,
                    [
                        item.name
                        for item in file_path.iterdir()
                    ]
                )


            if action == "move":

                shutil.move(
                    str(file_path),
                    kwargs["destination"]
                )

                return ToolResult(
                    True,
                    "Moved"
                )

            if action == "search":

                pattern = kwargs.get(
                    "pattern",
                    "*"
                )


                matches = [
                    str(item)
                    for item in file_path.rglob(
                        pattern
                    )
                ]


                return ToolResult(
                    True,
                    matches
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