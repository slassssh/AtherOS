from app.runtime.observe import ObserveModule
from app.runtime.think import ThinkModule
from app.runtime.plan import PlanModule
from app.runtime.act import ActModule
from app.runtime.reflect import ReflectModule


class AutonomousCycleRunner:

    def __init__(self):

        self.observe = ObserveModule()
        self.think = ThinkModule()
        self.plan = PlanModule()
        self.act = ActModule()
        self.reflect = ReflectModule()


    def run_cycle(self, goal):

        observation = self.observe.observe(goal)

        thought = self.think.think(
            observation
        )

        plan = self.plan.create_plan(
            thought
        )

        action = self.act.execute(
            plan
        )

        reflection = self.reflect.reflect(
            action
        )

        return {
            "completed": True,
            "reflection": reflection
        }