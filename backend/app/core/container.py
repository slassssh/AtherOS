class Container:


    def __init__(self):

        self.services = {}


    def register(self, name, service):

        self.services[name] = service

        return True



    def resolve(self, name):

        return self.services.get(
            name
        )