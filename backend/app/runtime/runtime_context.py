class RuntimeContext:

    def __init__(self):
        self.context = {}


    def set(self, key, value):

        self.context[key] = value

        return True


    def get(self, key):

        return self.context.get(key)


    def remove(self, key):

        if key in self.context:
            del self.context[key]
            return True

        return False


    def all(self):
        return self.context