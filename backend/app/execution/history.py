class ExecutionHistory:


    def __init__(self):

        self.records = []


    def add(self, record):

        self.records.append(record)

        return True


    def all(self):

        return self.records