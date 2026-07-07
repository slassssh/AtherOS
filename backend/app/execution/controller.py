class ExecutionController:


    def __init__(self):

        self.enabled = False


    def enable(self):

        self.enabled = True

        return True


    def disable(self):

        self.enabled = False

        return True


    def status(self):

        return self.enabled