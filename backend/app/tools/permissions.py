from enum import Enum
from typing import Dict, Set, Optional
from backend.app.utils.exceptions import PermissionDeniedError


class ToolPermission(Enum):
    READ_FILE = "READ_FILE"
    WRITE_FILE = "WRITE_FILE"
    DELETE_FILE = "DELETE_FILE"
    RUN_PYTHON = "RUN_PYTHON"
    RUN_TERMINAL = "RUN_TERMINAL"
    NETWORK_ACCESS = "NETWORK_ACCESS"

    # Backward compatibility aliases
    FILE_ACCESS = "READ_FILE"
    SYSTEM_ACCESS = "RUN_TERMINAL"
    CODE_EXECUTION = "RUN_PYTHON"


class PermissionManager:
    """
    Manages explicit tool execution permissions per session or globally.
    No tool may execute without explicit permission validation.
    """

    def __init__(self):
        # Default granted permissions for system operation
        self._default_permissions: Set[ToolPermission] = {
            ToolPermission.READ_FILE,
            ToolPermission.WRITE_FILE,
            ToolPermission.DELETE_FILE,
            ToolPermission.RUN_PYTHON,
            ToolPermission.RUN_TERMINAL,
            ToolPermission.NETWORK_ACCESS,
        }
        self._session_permissions: Dict[str, Set[ToolPermission]] = {}

    def grant_permission(self, permission: ToolPermission, session_id: Optional[str] = None) -> None:
        if session_id:
            if session_id not in self._session_permissions:
                self._session_permissions[session_id] = set(self._default_permissions)
            self._session_permissions[session_id].add(permission)
        else:
            self._default_permissions.add(permission)

    def revoke_permission(self, permission: ToolPermission, session_id: Optional[str] = None) -> None:
        if session_id:
            if session_id not in self._session_permissions:
                self._session_permissions[session_id] = set(self._default_permissions)
            self._session_permissions[session_id].discard(permission)
        else:
            self._default_permissions.discard(permission)

    def has_permission(self, permission: ToolPermission, session_id: Optional[str] = None) -> bool:
        if session_id and session_id in self._session_permissions:
            return permission in self._session_permissions[session_id]
        return permission in self._default_permissions

    def check_permission(self, permission: ToolPermission, session_id: Optional[str] = None) -> None:
        if not self.has_permission(permission, session_id):
            raise PermissionDeniedError(
                f"Permission '{permission.value}' denied for session '{session_id or 'global'}'."
            )


# Global singleton permission manager
permission_manager = PermissionManager()