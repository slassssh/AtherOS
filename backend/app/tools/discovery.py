"""
AtherOS Tool Discovery

Automatically discovers tools.
"""


class ToolDiscovery:


    def __init__(
        self
    ):

        self.discovered = []


    def discover(
        self,
        tools
    ):


        for tool in tools:


            if hasattr(
                tool,
                "metadata"
            ):


                self.discovered.append(
                    tool
                )


        return self.discovered