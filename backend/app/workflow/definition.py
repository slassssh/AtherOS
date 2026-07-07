class WorkflowDefinition:


    def __init__(self):

        self.definition = {}


    def define(self, key, value):

        self.definition[key] = value

        return True


    def get(self, key):

        return self.definition.get(key)