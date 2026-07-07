class SecurityCenter:


    def __init__(self):

        self.alerts = []



    def alert(self, message):

        self.alerts.append(
            message
        )

        return True



    def show_alerts(self):

        return self.alerts