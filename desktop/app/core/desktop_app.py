class DesktopApp:


    def __init__(self):

        self.running = False



    def start(self):

        self.running = True

        return {
            "desktop": "AtherOS",
            "running": self.running
        }



    def stop(self):

        self.running = False

        return True