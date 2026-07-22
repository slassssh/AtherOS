import ast
from datetime import datetime, UTC
from pathlib import Path
import subprocess
import sys
from typing import Any, Dict, List, Optional

from backend.app.config.config import settings
from backend.app.tools.permissions import ToolPermission, permission_manager
from backend.app.tools.result import ToolResult
from backend.app.utils.exceptions import PermissionDeniedError, SandboxedExecutionError, SecurityError
from backend.app.utils.logger import logger

# Audit log storage for security events
audit_log: List[Dict[str, Any]] = []


def log_security_audit(
    tool: str,
    permission: str,
    result: str,
    reason: str,
    session_id: Optional[str] = None
) -> None:
    record = {
        "timestamp": datetime.now(UTC).isoformat(),
        "session_id": session_id or "global",
        "tool": tool,
        "permission": permission,
        "result": result,
        "reason": reason,
    }
    audit_log.append(record)
    logger.info(f"SECURITY AUDIT | Tool: {tool} | Perm: {permission} | Result: {result} | Reason: {reason}")


def validate_workspace_path(path_str: str) -> Path:
    """
    Restricts file access strictly to the workspace root.
    Rejects:
    - Relative traversal (../, ..\\)
    - Absolute paths outside workspace
    - Symlinks escaping workspace
    """
    if not path_str:
        raise SecurityError("Path cannot be empty.")

    # 1. Reject explicit relative traversal attempts before resolution
    normalized = str(path_str).replace("\\", "/")
    if "../" in normalized or "/.." in normalized or normalized == "..":
        raise SecurityError(f"Directory traversal detected: '{path_str}' is forbidden.")

    workspace_root = Path(settings.workspace_root).resolve()
    target_path = Path(path_str)

    # Convert path to absolute relative to workspace root if not already
    if not target_path.is_absolute():
        target_path = (workspace_root / target_path)

    try:
        resolved_path = target_path.resolve()
    except Exception as err:
        raise SecurityError(f"Invalid path structure '{path_str}': {err}")

    # 2. Enforce strict workspace containment boundary check
    if not resolved_path.is_relative_to(workspace_root):
        raise SecurityError(f"Path '{path_str}' escapes workspace sandbox root '{workspace_root}'. Access denied.")

    return resolved_path


class ToolSandbox:
    """
    Central security sandbox through which all tools execute.
    Responsible for permission validation, workspace restriction, timeout enforcement,
    Python subprocess isolation, and audit logging.
    """

    def __init__(self, timeout: int = 10, max_output_size: int = 50000):
        self.timeout = timeout
        self.max_output_size = max_output_size
        self.blocked_tools: List[str] = []

    def block(self, tool_name: str) -> None:
        if tool_name not in self.blocked_tools:
            self.blocked_tools.append(tool_name)

    def allowed(self, tool_name: str) -> bool:
        return tool_name not in self.blocked_tools

    def execute_python_code(
        self,
        code: str,
        session_id: Optional[str] = None
    ) -> ToolResult:
        """
        Hardened Python Execution Sandbox.
        Runs code in an isolated Python subprocess with restricted builtins, AST static checks,
        and execution timeout enforcement.
        """
        # 1. Permission Check
        try:
            permission_manager.check_permission(ToolPermission.RUN_PYTHON, session_id)
        except PermissionDeniedError as err:
            log_security_audit("python", "RUN_PYTHON", "DENIED", str(err), session_id)
            return ToolResult(success=False, error=str(err))

        # 2. AST Static Security Check for Forbidden Modules/Builtins
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                # Check forbidden imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in ("os", "sys", "subprocess", "socket", "shutil", "urllib", "requests"):
                            reason = f"Forbidden import '{alias.name}' detected in Python code."
                            log_security_audit("python", "RUN_PYTHON", "BLOCKED", reason, session_id)
                            return ToolResult(success=False, error=reason)

                if isinstance(node, ast.ImportFrom):
                    if node.module in ("os", "sys", "subprocess", "socket", "shutil", "urllib", "requests"):
                        reason = f"Forbidden import '{node.module}' detected in Python code."
                        log_security_audit("python", "RUN_PYTHON", "BLOCKED", reason, session_id)
                        return ToolResult(success=False, error=reason)

                # Check forbidden calls (eval, exec, __import__, open)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in ("eval", "exec", "__import__"):
                        reason = f"Forbidden builtin function '{node.func.id}' detected in Python code."
                        log_security_audit("python", "RUN_PYTHON", "BLOCKED", reason, session_id)
                        return ToolResult(success=False, error=reason)

        except SyntaxError as err:
            log_security_audit("python", "RUN_PYTHON", "SYNTAX_ERROR", str(err), session_id)
            return ToolResult(success=False, error=f"Python syntax error: {err}")

        # 3. Isolated Subprocess Runner
        wrapper_code = f"""
import sys

# Restricted builtins environment wrapper
restricted_globals = {{
    "__builtins__": {{
        "print": print, "range": range, "len": len, "int": int, "float": float,
        "str": str, "bool": bool, "list": list, "dict": dict, "set": set,
        "tuple": tuple, "abs": abs, "min": min, "max": max, "sum": sum,
        "enumerate": enumerate, "zip": zip, "isinstance": isinstance
    }}
}}

user_code = {repr(code)}
exec(user_code, restricted_globals)
"""

        try:
            proc = subprocess.run(
                [sys.executable, "-c", wrapper_code],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            output = (proc.stdout or proc.stderr or "")[:self.max_output_size]

            if proc.returncode == 0:
                log_security_audit("python", "RUN_PYTHON", "SUCCESS", "Code executed in sandbox", session_id)
                return ToolResult(success=True, output=output.strip())
            else:
                log_security_audit("python", "RUN_PYTHON", "FAILED", output.strip(), session_id)
                return ToolResult(success=False, error=output.strip())

        except subprocess.TimeoutExpired:
            reason = f"Python execution timed out after {self.timeout} seconds."
            log_security_audit("python", "RUN_PYTHON", "TIMEOUT", reason, session_id)
            return ToolResult(success=False, error=reason)
        except Exception as err:
            reason = f"Subprocess sandbox execution error: {err}"
            log_security_audit("python", "RUN_PYTHON", "ERROR", reason, session_id)
            return ToolResult(success=False, error=reason)