class AutomationController:


    def __init__(self):

        self.active = False



    def start(self):

        self.active = True

        return {
            "controller": self.active
        }