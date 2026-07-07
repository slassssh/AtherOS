class AtherSDK:


    def __init__(self):

        self.modules = {}



    def add_module(self, name, module):

        self.modules[name] = module

        return True



    def get(self, name):

        return self.modules.get(
            name
        )