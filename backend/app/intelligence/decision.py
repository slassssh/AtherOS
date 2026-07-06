"""
AtherOS Decision Engine

Chooses best action.
"""


class DecisionEngine:


    def decide(
        self,
        options
    ):


        if not options:

            return None


        return options[0]