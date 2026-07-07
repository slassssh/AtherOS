class WorkspaceSettings:


    def __init__(self):

        self.settings = {}



    def set(self, key, value):

        self.settings[key] = value

        return True



    def get(self, key):

        return self.settings.get(key)