class ExecutionContext:


    def __init__(self):

        self.context = {}


    def set(self, key, value):

        self.context[key] = value

        return True


    def get(self, key):

        return self.context.get(key)