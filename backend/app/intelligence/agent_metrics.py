"""
AtherOS Agent Metrics

Tracks agent performance.
"""


class AgentMetrics:


    def __init__(self):

        self.tasks = 0
        self.success = 0


    def record(
        self,
        success
    ):

        self.tasks += 1


        if success:

            self.success += 1


    def stats(self):

        return {
            "tasks": self.tasks,
            "success": self.success
        }