from backend.app.beta.controller import BetaController
from backend.app.beta.analytics import BetaAnalytics
from backend.app.beta.feedback import FeedbackCollector



class BetaIntegration:


    def __init__(self):

        self.controller = BetaController()
        self.analytics = BetaAnalytics()
        self.feedback = FeedbackCollector()



    def launch(self):

        self.controller.start()


        return {
            "running": self.controller.running,
            "analytics": self.analytics.analyze()["analytics_enabled"],
            "feedback": self.feedback.collect()["feedback_collected"]
        }