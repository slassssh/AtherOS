"""
AtherOS Dynamic Priority

Ranks actions dynamically.
"""


class DynamicPriority:


    def prioritize(
        self,
        tasks
    ):

        return sorted(
            tasks,
            reverse=True
        )