from backend.app.security_suite.controller import SecurityController
from backend.app.security_suite.metrics import SecurityMetrics
from backend.app.security_suite.intelligence import SecurityIntelligence



class SecurityIntegration:


    def __init__(self):

        self.controller = SecurityController()
        self.metrics = SecurityMetrics()
        self.ai = SecurityIntelligence()



    def launch(self):

        self.controller.start()

        self.metrics.record(
            "status",
            "protected"
        )


        return {
            "running": True,
            "protected": True,
            "intelligent": self.ai.analyze()["ai_security"]
        }