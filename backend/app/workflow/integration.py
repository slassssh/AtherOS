from app.workflow.controller import WorkflowController
from app.workflow.metrics import WorkflowMetrics
from app.workflow.logs import WorkflowLogs
from app.workflow.security import WorkflowSecurity


class WorkflowIntegration:


    def __init__(self):

        self.controller = WorkflowController()
        self.metrics = WorkflowMetrics()
        self.logs = WorkflowLogs()
        self.security = WorkflowSecurity()


    def launch(self):

        self.controller.start()

        self.metrics.record(
            "workflow_engine",
            True
        )

        self.logs.add(
            "workflow engine launched"
        )


        return {
            "running": self.controller.status(),
            "secure": True
        }