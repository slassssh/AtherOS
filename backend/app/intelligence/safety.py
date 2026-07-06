"""
AtherOS Agent Safety

Validates agent actions.
"""


class AgentSafety:


    def allow(
        self,
        action
    ):


        blocked = [
            "dangerous"
        ]


        return action not in blocked