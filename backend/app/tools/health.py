"""
AtherOS Tool Health

Checks tool availability.
"""


class ToolHealth:


    def check(
        self,
        tool
    ):


        required = [
            "metadata",
            "execute"
        ]


        for item in required:


            if not hasattr(
                tool,
                item
            ):

                return False


        return True