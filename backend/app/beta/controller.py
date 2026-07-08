class BetaController:


    def __init__(self):

        self.running = False



    def start(self):

        self.running = True


        return {
            "running": self.running
        }