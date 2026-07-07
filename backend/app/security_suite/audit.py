class AuditLogger:


    def __init__(self):

        self.logs = []



    def log(self, event):

        self.logs.append(event)

        return True



    def all(self):

        return self.logs