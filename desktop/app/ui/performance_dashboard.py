class PerformanceDashboard:


    def __init__(self):

        self.metrics = {}



    def record(self, name, value):

        self.metrics[name] = value

        return True



    def report(self):

        return self.metrics