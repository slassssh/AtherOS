from backend.app.testing.controller import TestingController
from backend.app.testing.ai_assistant import AITestAssistant
from backend.app.testing.security import SecurityTesting



class TestingIntegration:


    def __init__(self):

        self.controller = TestingController()
        self.ai = AITestAssistant()
        self.security = SecurityTesting()



    def launch(self):

        self.controller.start()


        return {
            "running": self.controller.running,
            "ai_enabled": self.ai.analyze()["ai_testing"],
            "secure": self.security.scan()["security_passed"]
        }