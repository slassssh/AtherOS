import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.workflow.integration import WorkflowIntegration
from app.workflow.core import WorkflowCore
from app.workflow.step_executor import StepExecutor
from app.workflow.agent_binding import AgentWorkflowBinding
from app.workflow.optimizer import WorkflowOptimizer



def test_phase9_complete_system():


    # launch workflow engine

    engine = WorkflowIntegration()

    launch = engine.launch()

    assert launch["running"]
    assert launch["secure"]



    # create workflow

    workflow = WorkflowCore(
        "autonomous-defense"
    )

    workflow.add_step(
        "observe"
    )

    workflow.add_step(
        "act"
    )

    assert workflow.info()["steps"] == 2



    # execute step

    executor = StepExecutor()

    result = executor.execute(
        "observe"
    )

    assert result["success"]



    # bind agent

    binding = AgentWorkflowBinding()

    binding.bind(
        "autonomous-defense",
        "agent-alpha"
    )

    assert binding.get_agent(
        "autonomous-defense"
    ) == "agent-alpha"



    # optimize

    optimizer = WorkflowOptimizer()

    optimized = optimizer.optimize(
        [
            "scan",
            "scan",
            "repair"
        ]
    )

    assert optimized["after"] == 2



if __name__ == "__main__":

    test_phase9_complete_system()

    print(
        "🎉 AtherOS v0.9 Autonomous Workflow Engine Complete"
    )