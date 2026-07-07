from desktop.app.core.desktop_integration import DesktopIntegration
from desktop.app.core.state_persistence import StatePersistence
from desktop.app.core.ui_optimizer import UIOptimizer


class FinalDesktopIntegration:


    def __init__(self):

        self.desktop = DesktopIntegration()
        self.state = StatePersistence()
        self.optimizer = UIOptimizer()



    def launch(self):

        desktop = self.desktop.connect()

        optimized = self.optimizer.optimize()


        return {
            "running": desktop["connected"],
            "optimized": optimized["optimized"]
        }