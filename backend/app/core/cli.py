class AtherCLI:


    def __init__(self):

        self.commands = {}



    def register(self, name, handler):

        self.commands[name] = handler

        return True



    def run(self, name):

        command = self.commands.get(
            name
        )


        if command:

            return command()


        return None