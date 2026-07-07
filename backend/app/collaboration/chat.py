class TeamChat:


    def __init__(self):

        self.messages = []



    def send(self, message):

        self.messages.append(message)

        return True



    def history(self):

        return self.messages