class TestMetrics:


    def __init__(self):

        self.metrics = {}



    def record(self, key, value):

        self.metrics[key] = value

        return True



    def report(self):

        return self.metrics