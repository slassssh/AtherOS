class PluginCore:


    def __init__(self):

        self.enabled = True



    def status(self):

        return {
            "plugin_system": self.enabled
        }