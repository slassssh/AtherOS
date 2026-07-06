import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.runtime.observe import ObserveModule
from app.runtime.think import ThinkModule
from app.runtime.plan import PlanModule
from app.runtime.act import ActModule
from app.runtime.reflect import ReflectModule



def test_phase7_runtime_brain():

    observer = ObserveModule()

    obs = observer.observe(
        "system event"
    )

    assert obs["data"] == "system event"



    thinker = ThinkModule()

    thought = thinker.think(obs)

    assert thought["analysis"] == "processed"



    planner = PlanModule()

    plan = planner.create_plan(
        "protect system"
    )

    planner.add_step(
        plan,
        "scan"
    )

    assert len(plan["steps"]) == 1



    actor = ActModule()

    action = actor.execute(
        "scan"
    )

    assert action["success"]



    reflector = ReflectModule()

    reflection = reflector.reflect(
        action
    )

    assert reflection["learning"] == "stored"



if __name__ == "__main__":

    test_phase7_runtime_brain()

    print(
        "✅ Phase 7 Block 2 (Features 6-10) Runtime Brain Tests Passed"
    )