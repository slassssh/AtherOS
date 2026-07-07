class PluginMarketplace:


    def __init__(self):

        self.plugins = []



    def publish(self, plugin):

        self.plugins.append(plugin)

        return True



    def all(self):

        return self.plugins