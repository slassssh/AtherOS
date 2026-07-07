class WorkflowOptimizer:


    def optimize(self, steps):

        return {
            "before": len(steps),
            "after": len(set(steps)),
            "steps": list(set(steps))
        }