class CodeWorkspaceCore:


    def __init__(self):

        self.active = False



    def start(self):

        self.active = True


        return {
            "developer_workspace": True,
            "active": self.active
        }