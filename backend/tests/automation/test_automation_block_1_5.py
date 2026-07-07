import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.automation.core import AutomationCore
from backend.app.automation.trigger import TriggerEngine
from backend.app.automation.event import EventAutomation
from backend.app.automation.scheduler import TaskScheduler
from backend.app.automation.rules import RuleEngine



def test_automation_core():


    core = AutomationCore()

    assert core.start()["automation"]



    trigger = TriggerEngine()

    assert trigger.trigger(
        "startup"
    )["triggered"]



    event = EventAutomation()

    assert event.execute(
        "deploy"
    )["executed"]



    scheduler = TaskScheduler()

    scheduler.add(
        "backup"
    )

    assert "backup" in scheduler.all()



    rules = RuleEngine()

    assert rules.evaluate(
        "safe"
    )["passed"]




if __name__ == "__main__":

    test_automation_core()


    print(
        "✅ Phase 17 Block 1 (Features 1-5) Automation Tests Passed"
    )