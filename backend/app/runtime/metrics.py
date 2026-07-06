class RuntimeMetrics:

    def __init__(self):
        self.metrics = {}


    def record(self, key, value):

        self.metrics[key] = value

        return True


    def get(self, key):

        return self.metrics.get(key)


    def all(self):

        return self.metrics