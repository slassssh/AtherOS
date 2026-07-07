class WorkspaceState:


    def __init__(self):

        self.state = {}



    def set(self, key, value):

        self.state[key] = value

        return True



    def get(self, key):

        return self.state.get(
            key
        )