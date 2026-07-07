class ActivityFeed:


    def __init__(self):

        self.activities = []



    def add(self, activity):

        self.activities.append(activity)

        return True



    def all(self):

        return self.activities