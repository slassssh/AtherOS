import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.automation.conditional import ConditionalAutomation
from backend.app.automation.chain import ChainAutomation
from backend.app.automation.agent import AgentAutomation
from backend.app.automation.workflow import WorkflowAutomation
from backend.app.automation.tool import ToolAutomation



def test_automation_connections():


    condition = ConditionalAutomation()

    assert condition.check(
        "cpu < 80"
    )["allowed"]



    chain = ChainAutomation()

    chain.add(
        "step1"
    )

    assert "step1" in chain.steps()



    agent = AgentAutomation()

    assert agent.run(
        "agent1"
    )["automated"]



    workflow = WorkflowAutomation()

    assert workflow.execute(
        "flow"
    )["executed"]



    tool = ToolAutomation()

    assert tool.activate(
        "terminal"
    )["active"]




if __name__ == "__main__":

    test_automation_connections()


    print(
        "✅ Phase 17 Block 2 (Features 6-10) Automation Tests Passed"
    )