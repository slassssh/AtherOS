class GoalTracker:

    def __init__(self):

        self.goals = {}


    def add_goal(self, goal):

        self.goals[goal] = "active"

        return True


    def complete_goal(self, goal):

        if goal in self.goals:

            self.goals[goal] = "completed"

            return True

        return False


    def status(self, goal):

        return self.goals.get(goal)