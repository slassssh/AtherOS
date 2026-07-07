class ExecutionCore:


    def __init__(self):

        self.running = False


    def start(self):

        self.running = True

        return True


    def stop(self):

        self.running = False

        return True


    def status(self):

        return self.running