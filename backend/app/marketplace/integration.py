from backend.app.marketplace.controller import MarketplaceController
from backend.app.marketplace.intelligence import MarketplaceIntelligence
from backend.app.marketplace.security import MarketplaceSecurity



class MarketplaceIntegration:


    def __init__(self):

        self.controller = MarketplaceController()
        self.ai = MarketplaceIntelligence()
        self.security = MarketplaceSecurity()



    def launch(self):

        self.controller.start()


        return {
            "running": self.controller.running,
            "intelligent": self.ai.recommend()["ai_recommendations"],
            "secure": self.security.scan("package")["secure"]
        }