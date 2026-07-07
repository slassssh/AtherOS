import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.execution.action_engine import ActionEngine
from app.execution.command_runner import CommandRunner
from app.execution.runtime_executor import RuntimeExecutor
from app.execution.agent_executor import AgentExecutor
from app.execution.workflow_executor import WorkflowExecutor



def test_phase10_execution_engines():


    action = ActionEngine()

    result = action.run(
        "scan"
    )

    assert result["success"]



    command = CommandRunner()

    result = command.execute(
        "start"
    )

    assert result["executed"]



    runtime = RuntimeExecutor()

    result = runtime.execute_runtime(
        "runtime-core"
    )

    assert result["status"] == "executed"



    agent = AgentExecutor()

    result = agent.execute_agent(
        "agent1",
        "repair"
    )

    assert result["completed"]



    workflow = WorkflowExecutor()

    result = workflow.execute_workflow(
        "auto-flow"
    )

    assert result["success"]



if __name__ == "__main__":

    test_phase10_execution_engines()

    print(
        "✅ Phase 10 Block 2 (Features 6-10) Execution Engine Tests Passed"
    )