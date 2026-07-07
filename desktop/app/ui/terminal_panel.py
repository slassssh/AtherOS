class TerminalPanel:


    def __init__(self):

        self.history = []



    def execute(self, command):

        self.history.append(
            command
        )


        return {
            "command": command,
            "status": "completed"
        }