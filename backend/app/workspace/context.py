class WorkspaceContext:


    def __init__(self):

        self.context = {}



    def update(self, key, value):

        self.context[key] = value

        return True



    def get_context(self):

        return self.context