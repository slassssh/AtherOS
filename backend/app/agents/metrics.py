class MultiAgentMetrics:

    def __init__(self):

        self.data = {}


    def record(self, name, value):

        self.data[name] = value

        return True


    def get(self, name):

        return self.data.get(name)