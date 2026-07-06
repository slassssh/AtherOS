import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.runtime.cycle_runner import AutonomousCycleRunner
from app.runtime.continuous import ContinuousExecution
from app.runtime.goal_tracker import GoalTracker
from app.runtime.task_queue import TaskQueue
from app.runtime.scheduler import TaskScheduler



def test_phase7_runtime_execution():


    cycle = AutonomousCycleRunner()

    result = cycle.run_cycle(
        "secure system"
    )

    assert result["completed"]



    continuous = ContinuousExecution()

    assert continuous.start()

    assert continuous.execute() == 1

    assert continuous.stop()



    goals = GoalTracker()

    goals.add_goal(
        "protect"
    )

    assert goals.status(
        "protect"
    ) == "active"

    goals.complete_goal(
        "protect"
    )

    assert goals.status(
        "protect"
    ) == "completed"



    queue = TaskQueue()

    queue.add_task(
        "scan"
    )

    assert queue.next_task() == "scan"



    scheduler = TaskScheduler()

    scheduler.schedule_task(
        "backup"
    )

    assert scheduler.count() == 1



if __name__ == "__main__":

    test_phase7_runtime_execution()

    print(
        "✅ Phase 7 Block 3 (Features 11-15) Execution Tests Passed"
    )