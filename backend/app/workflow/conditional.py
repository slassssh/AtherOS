class ConditionalStep:


    def run_if(self, condition, action):

        if condition:

            return {
                "executed": True,
                "action": action
            }


        return {
            "executed": False
        }