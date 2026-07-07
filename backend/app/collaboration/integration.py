from backend.app.collaboration.controller import CollaborationController
from backend.app.collaboration.intelligence import TeamIntelligence
from backend.app.collaboration.metrics import CollaborationMetrics



class CollaborationIntegration:


    def __init__(self):

        self.controller = CollaborationController()
        self.ai = TeamIntelligence()
        self.metrics = CollaborationMetrics()



    def launch(self):

        self.controller.start()

        self.metrics.record(
            "members",
            1
        )


        return {
            "running": self.controller.running,
            "intelligent": self.ai.analyze()["team_ai"],
            "tracked": True
        }