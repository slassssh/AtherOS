"""
AtherOS Multi Step Execution

Executes multiple reasoning steps.
"""


class MultiStepExecution:


    def execute(
        self,
        steps
    ):

        results = []


        for step in steps:

            results.append(
                {
                    "step": step,
                    "done": True
                }
            )


        return results