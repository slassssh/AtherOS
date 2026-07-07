import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.execution.queue import ExecutionQueue
from app.execution.scheduler import ExecutionScheduler
from app.execution.monitor import ExecutionMonitor
from app.execution.history import ExecutionHistory
from app.execution.recovery import ExecutionRecovery



def test_phase10_execution_management():


    queue = ExecutionQueue()

    queue.add(
        "scan"
    )

    assert queue.next() == "scan"



    scheduler = ExecutionScheduler()

    job = scheduler.schedule(
        "repair"
    )

    assert job["task"] == "repair"



    monitor = ExecutionMonitor()

    monitor.track(
        "running"
    )

    assert "running" in monitor.status()



    history = ExecutionHistory()

    history.add(
        "completed"
    )

    assert len(
        history.all()
    ) == 1



    recovery = ExecutionRecovery()

    recovery.capture(
        Exception("failure")
    )

    assert recovery.recover()["recovered"]



if __name__ == "__main__":

    test_phase10_execution_management()

    print(
        "✅ Phase 10 Block 3 (Features 11-15) Management Tests Passed"
    )