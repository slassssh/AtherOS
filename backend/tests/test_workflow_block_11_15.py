import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.workflow.scheduler import WorkflowScheduler
from app.workflow.queue import WorkflowQueue
from app.workflow.events import WorkflowEvents
from app.workflow.history import WorkflowHistory
from app.workflow.recovery import WorkflowRecovery



def test_phase9_workflow_management():


    scheduler = WorkflowScheduler()

    scheduler.schedule(
        "daily_scan"
    )

    assert scheduler.count() == 1



    queue = WorkflowQueue()

    queue.add(
        "scan"
    )

    assert queue.next() == "scan"



    events = WorkflowEvents()

    event = events.emit(
        "started"
    )

    assert event["event"] == "started"



    history = WorkflowHistory()

    history.add(
        "completed"
    )

    assert len(
        history.get_all()
    ) == 1



    recovery = WorkflowRecovery()

    recovery.capture(
        Exception("failed")
    )

    assert recovery.recover()["recovered"]



if __name__ == "__main__":

    test_phase9_workflow_management()

    print(
        "✅ Phase 9 Block 3 (Features 11-15) Workflow Management Tests Passed"
    )