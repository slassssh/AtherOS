class StreamingUI:


    def __init__(self):

        self.stream = []



    def push(self, token):

        self.stream.append(
            token
        )


        return True



    def output(self):

        return "".join(
            self.stream
        )