from backend.app.workspace.controller import WorkspaceController
from backend.app.workspace.security import WorkspaceSecurity
from backend.app.workspace.metrics import WorkspaceMetrics



class WorkspaceIntegration:


    def __init__(self):

        self.controller = WorkspaceController()
        self.security = WorkspaceSecurity()
        self.metrics = WorkspaceMetrics()



    def launch(self):

        self.controller.start()

        self.metrics.record(
            "status",
            "running"
        )


        return {
            "running": self.controller.running,
            "secure": self.security.verify()["secure"]
        }