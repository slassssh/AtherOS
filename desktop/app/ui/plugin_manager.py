class PluginManagerUI:


    def __init__(self):

        self.plugins = []



    def install(self, plugin):

        self.plugins.append(
            plugin
        )

        return True



    def list_plugins(self):

        return self.plugins