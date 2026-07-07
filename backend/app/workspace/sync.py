class WorkspaceSync:


    def __init__(self):

        self.synced = False



    def sync(self):

        self.synced = True


        return {
            "synced": self.synced
        }