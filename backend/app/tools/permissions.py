"""
AtherOS Tool Permissions

Controls what capabilities
each tool requires.
"""


from enum import Enum


class ToolPermission(Enum):

    FILE_ACCESS = "FILE_ACCESS"

    SYSTEM_ACCESS = "SYSTEM_ACCESS"

    CODE_EXECUTION = "CODE_EXECUTION"

    NETWORK_ACCESS = "NETWORK_ACCESS"