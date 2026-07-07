class PluginEvents:


    def __init__(self):

        self.events = []



    def emit(self, event):

        self.events.append(event)

        return True



    def all(self):

        return self.events