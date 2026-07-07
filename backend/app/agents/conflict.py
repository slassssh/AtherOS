class ConflictResolver:

    def __init__(self):

        self.conflicts = []


    def detect(self, conflict):

        self.conflicts.append(conflict)

        return True


    def resolve(self):

        if self.conflicts:

            return {
                "resolved": True,
                "conflict": self.conflicts.pop()
            }

        return {
            "resolved": False
        }