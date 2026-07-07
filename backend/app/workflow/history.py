class WorkflowHistory:


    def __init__(self):

        self.records = []


    def add(self, record):

        self.records.append(record)

        return True


    def get_all(self):

        return self.records