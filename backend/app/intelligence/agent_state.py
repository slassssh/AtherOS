"""
AtherOS Agent State

Tracks current agent condition.
"""


class AgentState:


    def __init__(self):

        self.status = "idle"


    def update(
        self,
        status
    ):

        self.status = status


    def get(self):

        return self.status