"""
AtherOS Memory Aware Reasoning

Uses memories during reasoning.
"""


class MemoryAwareReasoning:


    def think(
        self,
        memory,
        task
    ):

        return {
            "memory": memory,
            "task": task,
            "used_memory": True
        }