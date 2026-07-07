class WorkspaceSecurity:


    def __init__(self):

        self.allowed = True



    def verify(self):

        return {
            "secure": self.allowed
        }