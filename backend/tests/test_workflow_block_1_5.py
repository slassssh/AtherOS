import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.workflow.core import WorkflowCore
from app.workflow.definition import WorkflowDefinition
from app.workflow.parser import WorkflowParser
from app.workflow.state import WorkflowState
from app.workflow.context import WorkflowContext



def test_phase9_workflow_core():


    workflow = WorkflowCore(
        "security-flow"
    )

    workflow.add_step(
        "scan"
    )

    assert workflow.info()["steps"] == 1



    definition = WorkflowDefinition()

    definition.define(
        "goal",
        "protect"
    )

    assert definition.get(
        "goal"
    ) == "protect"



    parser = WorkflowParser()

    result = parser.parse(
        workflow.info()
    )

    assert result["parsed"]



    state = WorkflowState()

    state.update(
        "running"
    )

    assert state.current() == "running"



    context = WorkflowContext()

    context.set(
        "agent",
        "alpha"
    )

    assert context.get(
        "agent"
    ) == "alpha"



if __name__ == "__main__":

    test_phase9_workflow_core()

    print(
        "✅ Phase 9 Block 1 (Features 1-5) Workflow Core Tests Passed"
    )