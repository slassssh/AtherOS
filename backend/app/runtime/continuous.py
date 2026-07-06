class ContinuousExecution:

    def __init__(self):

        self.running = False
        self.cycles = 0


    def start(self):

        self.running = True

        return True


    def execute(self):

        if not self.running:
            return False

        self.cycles += 1

        return self.cycles


    def stop(self):

        self.running = False

        return True