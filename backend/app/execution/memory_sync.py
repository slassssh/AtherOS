class MemoryExecutionSync:


    def __init__(self):

        self.records = []


    def sync(self, data):

        self.records.append(
            data
        )

        return True


    def history(self):

        return self.records