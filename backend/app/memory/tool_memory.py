"""
AtherOS Tool Memory

Stores tool execution memories.
"""


class ToolMemory:


    def __init__(
        self
    ):

        self.tools = {}


    def remember_tool(
        self,
        name: str,
        data: dict
    ):


        self.tools[
            name
        ] = data


    def recall_tool(
        self,
        name: str
    ):


        return self.tools.get(
            name
        )