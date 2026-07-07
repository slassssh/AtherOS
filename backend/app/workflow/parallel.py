class ParallelSteps:


    def execute_all(self, steps):

        results = []

        for step in steps:

            results.append(
                {
                    "step": step,
                    "success": True
                }
            )


        return results