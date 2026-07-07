class WorkflowMetrics:


    def __init__(self):

        self.metrics = {}


    def record(self, key, value):

        self.metrics[key] = value

        return True


    def get(self, key):

        return self.metrics.get(key)