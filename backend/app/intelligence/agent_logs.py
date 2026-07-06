"""
AtherOS Agent Logs

Stores intelligence events.
"""


class AgentLogs:


    def __init__(self):

        self.logs = []


    def add(
        self,
        message
    ):

        self.logs.append(
            message
        )


    def all(self):

        return self.logs.copy()