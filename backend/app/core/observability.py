class Observability:


    def __init__(self):

        self.signals = []



    def emit(self, signal):

        self.signals.append(
            signal
        )

        return True



    def metrics(self):

        return self.signals