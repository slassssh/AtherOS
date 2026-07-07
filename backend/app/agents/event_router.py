class EventRouter:

    def __init__(self):

        self.routes = {}


    def add_route(self, event, handler):

        self.routes[event] = handler

        return True


    def route(self, event):

        return self.routes.get(event)