class PluginManager:


    def __init__(self):

        self.plugins = {}


    def load(self, name, plugin):

        self.plugins[name] = plugin

        return True



    def get(self, name):

        return self.plugins.get(
            name
        )



    def all(self):

        return list(
            self.plugins.keys()
        )