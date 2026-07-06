"""
AtherOS Tool Security

Validates tool permissions before execution.
"""


class ToolSecurity:


    def __init__(
        self,
        allowed_permissions
    ):

        self.allowed_permissions = allowed_permissions


    def check(
        self,
        tool
    ):

        for permission in tool.metadata.permissions:

            if permission not in self.allowed_permissions:

                return False


        return True