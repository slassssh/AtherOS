class RestorePoint:


    def __init__(self):

        self.points = {}



    def save(self, name, state):

        self.points[name] = state


        return True



    def restore(self, name):

        return self.points.get(
            name
        )