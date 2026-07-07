class MessageBus:

    def __init__(self):

        self.queue = []


    def publish(self, message):

        self.queue.append(message)

        return True


    def consume(self):

        if self.queue:

            return self.queue.pop(0)

        return None