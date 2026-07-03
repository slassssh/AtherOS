"""
AtherOS Tool Schema

Validates tool inputs.
"""


class ToolSchema:


    def __init__(
        self,
        required: list[str]
    ):

        self.required = required


    def validate(
        self,
        data: dict
    ):

        missing = []


        for field in self.required:

            if field not in data:

                missing.append(field)


        if missing:

            return False, missing


        return True, []