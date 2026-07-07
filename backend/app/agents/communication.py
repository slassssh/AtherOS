from datetime import datetime


class AgentCommunication:

    def __init__(self):

        self.messages = []


    def send(self, sender, receiver, message):

        packet = {
            "from": sender,
            "to": receiver,
            "message": message,
            "time": datetime.utcnow()
        }

        self.messages.append(packet)

        return packet


    def history(self):

        return self.messages