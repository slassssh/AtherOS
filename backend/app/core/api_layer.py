class APILayer:


    def __init__(self):

        self.routes = {}


    def route(self, path, handler):

        self.routes[path] = handler

        return True



    def execute(self, path):

        handler = self.routes.get(
            path
        )


        if handler:

            return handler()


        return None