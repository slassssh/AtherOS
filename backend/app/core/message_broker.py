class MessageBroker:


    def __init__(self):

        self.messages = []



    def publish(self, message):

        self.messages.append(
            message
        )

        return True



    def consume(self):

        if self.messages:

            return self.messages.pop(0)


        return None