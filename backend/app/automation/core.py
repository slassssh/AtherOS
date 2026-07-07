class AutomationCore:


    def __init__(self):

        self.running = False



    def start(self):

        self.running = True

        return {
            "automation": self.running
        }