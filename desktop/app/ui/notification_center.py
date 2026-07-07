class NotificationCenter:


    def __init__(self):

        self.notifications = []



    def notify(self, message):

        self.notifications.append(
            message
        )


        return True



    def all(self):

        return self.notifications