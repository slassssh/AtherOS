from backend.app.performance.controller import PerformanceController
from backend.app.performance.analytics import PerformanceAnalytics
from backend.app.performance.auto_tuner import AutoTuner



class PerformanceIntegration:


    def __init__(self):

        self.controller = PerformanceController()
        self.analytics = PerformanceAnalytics()
        self.tuner = AutoTuner()



    def launch(self):

        self.controller.start()


        return {
            "running": self.controller.running,
            "analytics": self.analytics.analyze()["analytics"],
            "optimized": self.tuner.tune()["auto_tuned"]
        }