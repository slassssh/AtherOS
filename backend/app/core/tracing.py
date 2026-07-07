class ErrorTracer:


    def __init__(self):

        self.errors = []



    def capture(self, error):

        self.errors.append(
            str(error)
        )

        return True



    def all(self):

        return self.errors