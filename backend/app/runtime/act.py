class ActModule:

    def __init__(self):
        self.actions = []


    def execute(self, action):

        result = {
            "action": action,
            "success": True
        }

        self.actions.append(result)

        return result


    def history(self):

        return self.actions