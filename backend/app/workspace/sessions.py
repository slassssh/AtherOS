class WorkspaceSession:


    def __init__(self):

        self.sessions = []



    def create(self, session):

        self.sessions.append(
            session
        )


        return True



    def all(self):

        return self.sessions