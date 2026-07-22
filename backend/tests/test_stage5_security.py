import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from backend.app.tools.file_tool import FileTool
from backend.app.tools.python_tool import PythonTool
from backend.app.tools.terminal_tool import TerminalTool
from backend.app.tools.permissions import ToolPermission, permission_manager
from backend.app.tools.sandbox import validate_workspace_path, audit_log, ToolSandbox
from backend.app.utils.exceptions import SecurityError, PermissionDeniedError


def test_unix_directory_traversal_rejected():
    file_tool = FileTool()
    res = file_tool.execute(action="read", path="../../../etc/passwd")

    assert res.success is False
    assert "Directory traversal detected" in res.error or "escapes workspace" in res.error


def test_windows_directory_traversal_rejected():
    file_tool = FileTool()
    res = file_tool.execute(action="read", path="..\\..\\Windows\\System32\\cmd.exe")

    assert res.success is False
    assert "traversal" in res.error.lower() or "escapes" in res.error.lower()


def test_permission_denied_enforcement():
    session_id = "test_session_restricted"
    # Revoke READ_FILE permission for session
    permission_manager.revoke_permission(ToolPermission.READ_FILE, session_id=session_id)

    file_tool = FileTool()
    res = file_tool.execute(action="read", path="sample.log", session_id=session_id)

    assert res.success is False
    assert "Permission" in res.error and "denied" in res.error

    # Restore permission
    permission_manager.grant_permission(ToolPermission.READ_FILE, session_id=session_id)


def test_blocked_shell_injection():
    terminal_tool = TerminalTool()
    res = terminal_tool.execute(command="echo hello && del /f /s /q *")

    assert res.success is False
    assert "Shell injection operator" in res.error


def test_blocked_unallowed_executable():
    terminal_tool = TerminalTool()
    res = terminal_tool.execute(command="powershell -Command Get-Process")

    assert res.success is False
    assert "not in the allowed terminal execution list" in res.error


def test_blocked_python_imports_and_builtins():
    python_tool = PythonTool()

    # 1. Blocked import os
    res1 = python_tool.execute(code="import os\nos.system('echo hacked')")
    assert res1.success is False
    assert "Forbidden import 'os'" in res1.error

    # 2. Blocked import subprocess
    res2 = python_tool.execute(code="import subprocess\nsubprocess.run(['dir'])")
    assert res2.success is False
    assert "Forbidden import 'subprocess'" in res2.error

    # 3. Blocked eval call
    res3 = python_tool.execute(code="eval('1 + 1')")
    assert res3.success is False
    assert "Forbidden builtin function 'eval'" in res3.error


def test_valid_python_sandboxed_execution():
    python_tool = PythonTool()
    res = python_tool.execute(code="x = [i * 2 for i in range(5)]\nprint(x)")

    assert res.success is True
    assert "[0, 2, 4, 6, 8]" in res.output


def test_python_sandbox_timeout():
    sandbox = ToolSandbox(timeout=1)
    python_tool = PythonTool(sandbox=sandbox)
    # Busy loop exceeding timeout
    res = python_tool.execute(code="while True: pass")

    assert res.success is False
    assert "timed out" in res.error


def test_security_audit_log_recorded():
    initial_count = len(audit_log)
    file_tool = FileTool()
    file_tool.execute(action="read", path="../../../etc/passwd")

    assert len(audit_log) > initial_count
    latest = audit_log[-1]
    assert latest["tool"] == "file"
    assert latest["result"] in ("DENIED", "FAILED", "BLOCKED")
