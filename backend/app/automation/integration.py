from backend.app.automation.controller import AutomationController
from backend.app.automation.intelligence import AutomationIntelligence
from backend.app.automation.security import AutomationSecurity



class AutomationIntegration:


    def __init__(self):

        self.controller = AutomationController()
        self.ai = AutomationIntelligence()
        self.security = AutomationSecurity()



    def launch(self):

        self.controller.start()


        return {
            "running": self.controller.active,
            "intelligent": True,
            "secure": self.security.verify()["automation_secure"]
        }