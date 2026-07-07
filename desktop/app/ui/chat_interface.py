class ChatInterface:


    def __init__(self):

        self.messages = []



    def send(self, message):

        self.messages.append(
            message
        )


        return {
            "sent": True,
            "message": message
        }



    def history(self):

        return self.messages