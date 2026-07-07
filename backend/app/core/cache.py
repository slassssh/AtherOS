class Cache:


    def __init__(self):

        self.storage = {}



    def set(self, key, value):

        self.storage[key] = value

        return True



    def get(self, key):

        return self.storage.get(
            key
        )