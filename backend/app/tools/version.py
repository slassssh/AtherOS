"""
AtherOS Tool Version

Handles tool compatibility checks.
"""


class ToolVersion:


    def __init__(
        self,
        current: str
    ):

        self.current = current


    def compatible(
        self,
        required: str
    ):

        current_parts = self.current.split(".")

        required_parts = required.split(".")


        return (
            current_parts[0]
            ==
            required_parts[0]
        )