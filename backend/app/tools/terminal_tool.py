from pathlib import Path
import shlex
import subprocess
from typing import Optional

from backend.app.config.config import settings
from backend.app.tools.base import BaseTool
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission, permission_manager
from backend.app.tools.result import ToolResult
from backend.app.tools.sandbox import log_security_audit
from backend.app.utils.exceptions import SecurityError

ALLOWED_EXECUTABLES = {
    "git", "python", "python3", "pip", "pytest", "echo",
    "dir", "ls", "cat", "mkdir", "find", "type", "whoami", "ver"
}


class TerminalTool(BaseTool):
    metadata = ToolMetadata(
        name="terminal",
        description="Execute tokenized terminal commands safely",
        category="system",
        permissions=[
            ToolPermission.RUN_TERMINAL
        ]
    )

    def execute(
        self,
        command: str,
        session_id: Optional[str] = None,
        timeout: int = 10,
        **kwargs
    ) -> ToolResult:

        # 1. Permission Check
        try:
            permission_manager.check_permission(ToolPermission.RUN_TERMINAL, session_id)
        except Exception as err:
            log_security_audit("terminal", "RUN_TERMINAL", "DENIED", str(err), session_id)
            return ToolResult(success=False, error=str(err))

        if not command or not command.strip():
            return ToolResult(success=False, error="Empty command string.")

        # 2. Reject shell injection operators before tokenization
        raw_cmd = command.strip()
        for char in ("&", ";", "|", ">", "<", "`"):
            if char in raw_cmd:
                reason = f"Shell injection operator '{char}' detected in command '{command}'."
                log_security_audit("terminal", "RUN_TERMINAL", "BLOCKED", reason, session_id)
                return ToolResult(success=False, error=reason)

        try:
            # 3. Tokenize command safely
            args = shlex.split(raw_cmd)
            executable = Path(args[0]).name.lower().replace(".exe", "")

            # 4. Check executable against allowlist
            if executable not in ALLOWED_EXECUTABLES:
                reason = f"Executable '{executable}' is not in the allowed terminal execution list."
                log_security_audit("terminal", "RUN_TERMINAL", "BLOCKED", reason, session_id)
                return ToolResult(success=False, error=reason)

            # 5. Execute without shell=True
            result = subprocess.run(
                args,
                cwd=settings.workspace_root,
                capture_output=True,
                text=True,
                shell=False,
                timeout=timeout
            )

            if result.returncode == 0:
                log_security_audit("terminal", "RUN_TERMINAL", "SUCCESS", f"Executed {args[0]}", session_id)
                return ToolResult(success=True, output=result.stdout.strip())

            log_security_audit("terminal", "RUN_TERMINAL", "FAILED", result.stderr.strip(), session_id)
            return ToolResult(success=False, error=result.stderr.strip() or f"Command failed with exit code {result.returncode}")

        except subprocess.TimeoutExpired:
            reason = f"Terminal command '{command}' timed out after {timeout} seconds."
            log_security_audit("terminal", "RUN_TERMINAL", "TIMEOUT", reason, session_id)
            return ToolResult(success=False, error=reason)
        except Exception as error:
            reason = f"Terminal execution error: {error}"
            log_security_audit("terminal", "RUN_TERMINAL", "ERROR", reason, session_id)
            return ToolResult(success=False, error=reason)