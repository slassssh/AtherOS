class PlanModule:

    def __init__(self):
        self.plans = []


    def create_plan(self, goal):

        plan = {
            "goal": goal,
            "steps": []
        }

        self.plans.append(plan)

        return plan


    def add_step(self, plan, step):

        plan["steps"].append(step)

        return plan