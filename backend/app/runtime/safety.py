class RuntimeSafety:

    def __init__(self):

        self.blocked = []


    def block(self, action):

        self.blocked.append(action)

        return True


    def allowed(self, action):

        return action not in self.blocked