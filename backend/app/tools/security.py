from typing import Optional, List
from backend.app.tools.permissions import ToolPermission, permission_manager


class ToolSecurity:
    """
    Validates tool permissions and safety parameters before execution.
    """

    def __init__(self, allowed_permissions: Optional[List[ToolPermission]] = None):
        self.allowed_permissions = allowed_permissions

    def check(self, tool, session_id: Optional[str] = None) -> bool:
        if not hasattr(tool, "metadata") or not hasattr(tool.metadata, "permissions"):
            return True

        for permission in tool.metadata.permissions:
            if not permission_manager.has_permission(permission, session_id):
                return False

        return True