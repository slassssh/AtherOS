from pathlib import Path
import shutil

from backend.app.tools.base import BaseTool
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission, permission_manager
from backend.app.tools.result import ToolResult
from backend.app.tools.sandbox import validate_workspace_path, log_security_audit
from backend.app.tools.schema import ToolSchema


class FileTool(BaseTool):

    metadata = ToolMetadata(
        name="file",
        description="Advanced sandboxed filesystem operations",
        category="filesystem",
        permissions=[
            ToolPermission.READ_FILE,
            ToolPermission.WRITE_FILE,
            ToolPermission.DELETE_FILE
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
        session_id: str = None,
        **kwargs
    ) -> ToolResult:

        try:
            # 1. Validate & Canonicalize Path against Workspace Root Sandbox
            file_path = validate_workspace_path(path)

            # 2. Action-level Permission Checks & Execution
            if action in ("read", "list", "search"):
                permission_manager.check_permission(ToolPermission.READ_FILE, session_id)

                if action == "read":
                    content = file_path.read_text(encoding="utf-8", errors="replace")
                    log_security_audit("file", "READ_FILE", "SUCCESS", f"Read file {file_path}", session_id)
                    return ToolResult(True, content)

                if action == "list":
                    if not file_path.exists():
                        return ToolResult(False, error=f"Path '{path}' does not exist.")
                    items = [item.name for item in file_path.iterdir()] if file_path.is_dir() else [file_path.name]
                    log_security_audit("file", "READ_FILE", "SUCCESS", f"Listed path {file_path}", session_id)
                    return ToolResult(True, items)

                if action == "search":
                    pattern = kwargs.get("pattern", "*")
                    matches = [str(item) for item in file_path.rglob(pattern)]
                    log_security_audit("file", "READ_FILE", "SUCCESS", f"Searched {file_path} pattern {pattern}", session_id)
                    return ToolResult(True, matches)

            if action in ("write", "mkdir", "move"):
                permission_manager.check_permission(ToolPermission.WRITE_FILE, session_id)

                if action == "write":
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    content = kwargs.get("content", "")
                    file_path.write_text(content, encoding="utf-8")
                    log_security_audit("file", "WRITE_FILE", "SUCCESS", f"Wrote to {file_path}", session_id)
                    return ToolResult(True, f"File written successfully to {file_path.name}")

                if action == "mkdir":
                    file_path.mkdir(parents=True, exist_ok=True)
                    log_security_audit("file", "WRITE_FILE", "SUCCESS", f"Created directory {file_path}", session_id)
                    return ToolResult(True, f"Folder created at {file_path.name}")

                if action == "move":
                    dest_str = kwargs.get("destination", "")
                    dest_path = validate_workspace_path(dest_str)
                    shutil.move(str(file_path), str(dest_path))
                    log_security_audit("file", "WRITE_FILE", "SUCCESS", f"Moved {file_path} to {dest_path}", session_id)
                    return ToolResult(True, "File moved successfully")

            if action == "delete":
                permission_manager.check_permission(ToolPermission.DELETE_FILE, session_id)
                if file_path.is_dir():
                    shutil.rmtree(file_path)
                else:
                    file_path.unlink()
                log_security_audit("file", "DELETE_FILE", "SUCCESS", f"Deleted {file_path}", session_id)
                return ToolResult(True, f"Deleted {file_path.name}")

            return ToolResult(False, error=f"Unknown action '{action}'")

        except Exception as error:
            log_security_audit("file", "SECURITY_VIOLATION", "DENIED", str(error), session_id)
            return ToolResult(False, error=str(error))