class RuntimeErrorRecovery:

    def __init__(self):

        self.errors = []


    def capture(self, error):

        self.errors.append(
            str(error)
        )

        return True


    def recover(self):

        if self.errors:

            return {
                "recovered": True,
                "error": self.errors[-1]
            }

        return {
            "recovered": False
        }