class PluginLoader:


    def __init__(self):

        self.plugins = []



    def load(self, plugin):

        self.plugins.append(plugin)

        return True



    def all(self):

        return self.plugins