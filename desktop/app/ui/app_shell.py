class AppShell:


    def __init__(self):

        self.loaded = False



    def load(self):

        self.loaded = True

        return {
            "shell": "loaded"
        }