import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.workflow.metrics import WorkflowMetrics
from app.workflow.logs import WorkflowLogs
from app.workflow.security import WorkflowSecurity
from app.workflow.controller import WorkflowController
from app.workflow.integration import WorkflowIntegration



def test_phase9_final_layer():


    metrics = WorkflowMetrics()

    metrics.record(
        "runs",
        10
    )

    assert metrics.get(
        "runs"
    ) == 10



    logs = WorkflowLogs()

    logs.add(
        "started"
    )

    assert len(
        logs.history()
    ) == 1



    security = WorkflowSecurity()

    security.block(
        "danger-flow"
    )

    assert security.allowed(
        "danger-flow"
    ) == False



    controller = WorkflowController()

    assert controller.start()

    assert controller.status()



    engine = WorkflowIntegration()

    result = engine.launch()

    assert result["running"]

    assert result["secure"]



if __name__ == "__main__":

    test_phase9_final_layer()

    print(
        "✅ Phase 9 Block 5 (Features 21-25) Final Tests Passed"
    )