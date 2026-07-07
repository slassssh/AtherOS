class StatePersistence:


    def __init__(self):

        self.state = {}



    def save(self, key, value):

        self.state[key] = value

        return True



    def load(self, key):

        return self.state.get(
            key
        )