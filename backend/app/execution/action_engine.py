class ActionEngine:


    def __init__(self):

        self.actions = []


    def run(self, action):

        result = {
            "action": action,
            "success": True
        }

        self.actions.append(result)

        return result