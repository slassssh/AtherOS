from backend.app.cloud.controller import CloudController
from backend.app.cloud.intelligence import CloudIntelligence
from backend.app.cloud.security import SyncSecurity



class CloudIntegration:


    def __init__(self):

        self.controller = CloudController()
        self.ai = CloudIntelligence()
        self.security = SyncSecurity()



    def launch(self):

        self.controller.start()


        return {
            "running": self.controller.running,
            "optimized": self.ai.optimize()["optimized"],
            "secure": self.security.verify()["cloud_secure"]
        }