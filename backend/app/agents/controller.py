class MultiAgentController:

    def __init__(self):

        self.active = False


    def start(self):

        self.active = True

        return True


    def stop(self):

        self.active = False

        return True


    def status(self):

        return self.active