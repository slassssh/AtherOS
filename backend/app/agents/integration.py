from app.agents.controller import MultiAgentController
from app.agents.metrics import MultiAgentMetrics
from app.agents.logs import MultiAgentLogs
from app.agents.security import MultiAgentSecurity


class MultiAgentIntegration:

    def __init__(self):

        self.controller = MultiAgentController()
        self.metrics = MultiAgentMetrics()
        self.logs = MultiAgentLogs()
        self.security = MultiAgentSecurity()


    def launch(self):

        self.controller.start()

        self.metrics.record(
            "agents_online",
            True
        )

        self.logs.add(
            "multi-agent launched"
        )

        return {
            "running": self.controller.status(),
            "secure": True
        }