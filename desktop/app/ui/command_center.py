class CommandCenter:


    def __init__(self):

        self.commands = []



    def execute(self, command):

        self.commands.append(
            command
        )


        return {
            "executed": True,
            "command": command
        }