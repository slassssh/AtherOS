"""
AtherOS Context Planner

Creates plans using context.
"""


class ContextPlanner:


    def plan(
        self,
        context
    ):

        return [
            f"Analyze {context}",
            f"Execute {context}"
        ]