import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.execution.integration import ExecutionIntegration
from app.execution.core import ExecutionCore
from app.execution.action_engine import ActionEngine
from app.execution.agent_executor import AgentExecutor
from app.execution.workflow_executor import WorkflowExecutor
from app.execution.adaptive import AdaptiveExecution



def test_phase10_complete_system():


    # launch execution layer

    execution = ExecutionIntegration()

    launch = execution.launch()

    assert launch["running"]
    assert launch["secure"]



    # core engine

    core = ExecutionCore()

    assert core.start()



    # action execution

    action = ActionEngine()

    result = action.run(
        "autonomous-action"
    )

    assert result["success"]



    # agent execution

    agent = AgentExecutor()

    result = agent.execute_agent(
        "agent-alpha",
        "mission"
    )

    assert result["completed"]



    # workflow execution

    workflow = WorkflowExecutor()

    result = workflow.execute_workflow(
        "self-healing-flow"
    )

    assert result["success"]



    # adaptive layer

    adaptive = AdaptiveExecution()

    result = adaptive.adapt(
        "runtime-feedback"
    )

    assert result["adapted"]



if __name__ == "__main__":

    test_phase10_complete_system()

    print(
        "🎉 AtherOS v1.0 Autonomous Execution Layer Complete"
    )