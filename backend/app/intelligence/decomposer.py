"""
AtherOS Task Decomposer

Breaks goals into tasks.
"""


class TaskDecomposer:


    def decompose(
        self,
        goal: str
    ):


        return [
            f"Understand {goal}",
            f"Execute {goal}",
            f"Verify {goal}"
        ]