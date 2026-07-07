class ActivityTracker:


    def __init__(self):

        self.activities = []



    def track(self, activity):

        self.activities.append(
            activity
        )


        return True



    def history(self):

        return self.activities