class ExecutionRecovery:


    def __init__(self):

        self.errors = []


    def capture(self, error):

        self.errors.append(
            str(error)
        )

        return True


    def recover(self):

        return {
            "recovered": len(self.errors) > 0
        }