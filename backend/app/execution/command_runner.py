class CommandRunner:


    def __init__(self):

        self.history = []


    def execute(self, command):

        result = {
            "command": command,
            "executed": True
        }

        self.history.append(result)

        return result