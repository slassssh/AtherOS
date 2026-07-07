class WorkflowRecovery:


    def __init__(self):

        self.failures = []


    def capture(self, error):

        self.failures.append(
            str(error)
        )

        return True


    def recover(self):

        if self.failures:

            return {
                "recovered": True
            }


        return {
            "recovered": False
        }