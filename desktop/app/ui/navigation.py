class Navigation:


    def __init__(self):

        self.routes = []



    def add_route(self, route):

        self.routes.append(
            route
        )

        return True



    def get_routes(self):

        return self.routes