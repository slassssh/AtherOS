"""
AtherOS Tool Sandbox

Controls unsafe operations.
"""


class ToolSandbox:


    def __init__(
        self
    ):

        self.blocked_tools = []


    def block(
        self,
        tool_name: str
    ):

        self.blocked_tools.append(
            tool_name
        )


    def allowed(
        self,
        tool_name: str
    ):

        return (
            tool_name
            not in self.blocked_tools
        )