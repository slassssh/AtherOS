class ResourceLimiter:


    def __init__(self, limit):

        self.limit = limit



    def allow(self, usage):

        return usage <= self.limit