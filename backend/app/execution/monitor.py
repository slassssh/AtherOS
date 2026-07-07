class ExecutionMonitor:


    def __init__(self):

        self.events = []


    def track(self, event):

        self.events.append(event)

        return True


    def status(self):

        return self.events