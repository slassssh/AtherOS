class AgentRuntimeLoop:


    def __init__(self):

        self.running = False
        self.cycles = 0



    def start(self):

        self.running = True

        return True



    def tick(self):

        if not self.running:

            return False


        self.cycles += 1


        return {
            "cycle": self.cycles,
            "executed": True
        }