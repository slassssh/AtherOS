from backend.app.plugins.controller import PluginController
from backend.app.plugins.security import PluginSecurity



class PluginIntegration:


    def __init__(self):

        self.controller = PluginController()
        self.security = PluginSecurity()



    def launch(self):

        self.controller.start()


        return {
            "running": self.controller.active,
            "secure": self.security.scan(
                "system"
            )["secure"]
        }