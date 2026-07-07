class LogsViewer:


    def __init__(self):

        self.logs = []



    def add_log(self, log):

        self.logs.append(
            log
        )

        return True



    def view(self):

        return self.logs