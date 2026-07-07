from backend.app.developer.metrics import DeveloperMetrics
from backend.app.developer.security import DeveloperSecurity



class DeveloperIntegration:


    def __init__(self):

        self.metrics = DeveloperMetrics()
        self.security = DeveloperSecurity()



    def launch(self):

        self.metrics.record(
            "developer",
            "active"
        )


        return {
            "running": True,
            "secure": self.security.verify()["developer_secure"]
        }