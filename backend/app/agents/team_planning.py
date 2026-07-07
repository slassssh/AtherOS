class TeamPlanning:

    def __init__(self):

        self.plans = []


    def create(self, agents, goal):

        plan = {
            "agents": agents,
            "goal": goal
        }

        self.plans.append(plan)

        return plan