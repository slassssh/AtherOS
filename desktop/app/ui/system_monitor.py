class SystemMonitorUI:


    def __init__(self):

        self.metrics = {}



    def update(self, key, value):

        self.metrics[key] = value

        return True



    def status(self):

        return self.metrics