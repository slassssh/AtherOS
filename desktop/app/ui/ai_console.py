class AIConsole:


    def __init__(self):

        self.outputs = []



    def run_prompt(self, prompt):

        response = f"Processed: {prompt}"


        self.outputs.append(
            response
        )


        return response