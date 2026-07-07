import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.execution.metrics import ExecutionMetrics
from app.execution.logs import ExecutionLogs
from app.execution.security import ExecutionSecurity
from app.execution.controller import ExecutionController
from app.execution.integration import ExecutionIntegration



def test_phase10_execution_final():


    metrics = ExecutionMetrics()

    metrics.record(
        "runs",
        100
    )

    assert metrics.get(
        "runs"
    ) == 100



    logs = ExecutionLogs()

    logs.add(
        "started"
    )

    assert len(
        logs.history()
    ) == 1



    security = ExecutionSecurity()

    security.block(
        "unsafe"
    )

    assert security.allowed(
        "unsafe"
    ) == False



    controller = ExecutionController()

    assert controller.enable()

    assert controller.status()



    layer = ExecutionIntegration()

    result = layer.launch()

    assert result["running"]

    assert result["secure"]



if __name__ == "__main__":

    test_phase10_execution_final()

    print(
        "✅ Phase 10 Block 5 (Features 21-25) Final Tests Passed"
    )