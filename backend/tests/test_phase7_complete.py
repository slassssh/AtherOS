import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.runtime.integration import RuntimeIntegration
from app.runtime.cycle_runner import AutonomousCycleRunner
from app.runtime.memory_bridge import MemoryIntegration
from app.runtime.event_stream import EventStream
from app.runtime.goal_tracker import GoalTracker



def test_phase7_complete_runtime():


    # boot complete runtime

    runtime = RuntimeIntegration()

    boot = runtime.boot()

    assert boot["running"]
    assert boot["safe"]



    # autonomous cycle

    agent = AutonomousCycleRunner()

    cycle = agent.run_cycle(
        "protect system"
    )

    assert cycle["completed"]



    # memory layer

    memory = MemoryIntegration()

    memory.store(
        cycle
    )

    assert len(memory.recall()) == 1



    # goal system

    goals = GoalTracker()

    goals.add_goal(
        "autonomy"
    )

    goals.complete_goal(
        "autonomy"
    )

    assert goals.status(
        "autonomy"
    ) == "completed"



    # event stream

    stream = EventStream()

    event = stream.emit(
        "phase7_complete"
    )

    assert event["event"] == "phase7_complete"



if __name__ == "__main__":

    test_phase7_complete_runtime()

    print(
        "🎉 AtherOS v0.7 Autonomous Agent Runtime Complete"
    )