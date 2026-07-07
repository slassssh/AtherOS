class CollaborationEngine:

    def __init__(self):

        self.sessions = []


    def collaborate(self, agents, goal):

        session = {
            "agents": agents,
            "goal": goal
        }

        self.sessions.append(session)

        return session


    def history(self):

        return self.sessions