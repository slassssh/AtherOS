"""
AtherOS Tool Selector

Chooses required tools.
"""


class ToolSelector:


    def select_tool(
        self,
        task
    ):


        if "code" in task.lower():

            return "python"


        if "file" in task.lower():

            return "file"


        return "general"