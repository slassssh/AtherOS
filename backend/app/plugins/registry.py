class PluginRegistry:


    def __init__(self):

        self.registry = {}



    def register(self, name, plugin):

        self.registry[name] = plugin

        return True



    def get(self, name):

        return self.registry.get(name)