class ResourceManager:


    def __init__(self):

        self.resources = {}



    def allocate(self, name, value):

        self.resources[name] = value

        return True



    def get(self, name):

        return self.resources.get(
            name
        )