class AgentLifecycle:

    def __init__(self):
        self.events = []


    def boot(self):
        self.events.append("boot")
        return True


    def shutdown(self):
        self.events.append("shutdown")
        return True


    def restart(self):

        self.shutdown()
        self.boot()

        return True


    def history(self):
        return self.events