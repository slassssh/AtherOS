class SessionViewer:


    def __init__(self):

        self.sessions = []



    def add(self, session):

        self.sessions.append(
            session
        )


        return True



    def all(self):

        return self.sessions