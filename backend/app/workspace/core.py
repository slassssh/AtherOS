class WorkspaceCore:


    def __init__(self):

        self.active = False



    def start(self):

        self.active = True


        return {
            "workspace": True,
            "active": self.active
        }