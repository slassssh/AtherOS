from app.execution.controller import ExecutionController
from app.execution.metrics import ExecutionMetrics
from app.execution.logs import ExecutionLogs
from app.execution.security import ExecutionSecurity


class ExecutionIntegration:


    def __init__(self):

        self.controller = ExecutionController()
        self.metrics = ExecutionMetrics()
        self.logs = ExecutionLogs()
        self.security = ExecutionSecurity()


    def launch(self):

        self.controller.enable()

        self.metrics.record(
            "execution_layer",
            True
        )

        self.logs.add(
            "execution layer online"
        )

        return {
            "running": self.controller.status(),
            "secure": True
        }