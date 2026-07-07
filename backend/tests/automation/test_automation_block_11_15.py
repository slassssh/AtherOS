import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.automation.history import AutomationHistory
from backend.app.automation.recovery import AutomationRecovery
from backend.app.automation.metrics import AutomationMetrics
from backend.app.automation.security import AutomationSecurity
from backend.app.automation.optimizer import AutomationOptimizer



def test_automation_management():


    history = AutomationHistory()

    history.add(
        "task executed"
    )


    assert "task executed" in history.all()



    recovery = AutomationRecovery()

    assert recovery.recover(
        "error"
    )["recovered"]



    metrics = AutomationMetrics()

    metrics.record(
        "runs",
        10
    )

    assert metrics.report()["runs"] == 10



    security = AutomationSecurity()

    assert security.verify()["automation_secure"]



    optimizer = AutomationOptimizer()

    assert optimizer.optimize(
        "workflow"
    )["optimized"]




if __name__ == "__main__":

    test_automation_management()


    print(
        "✅ Phase 17 Block 3 (Features 11-15) Automation Tests Passed"
    )