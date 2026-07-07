import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.workflow.agent_binding import AgentWorkflowBinding
from app.workflow.tool_binding import ToolWorkflowBinding
from app.workflow.memory_binding import MemoryWorkflowBinding
from app.workflow.intelligence_binding import IntelligenceWorkflowBinding
from app.workflow.optimizer import WorkflowOptimizer



def test_phase9_bindings():


    agent = AgentWorkflowBinding()

    agent.bind(
        "scan-flow",
        "security-agent"
    )

    assert agent.get_agent(
        "scan-flow"
    ) == "security-agent"



    tool = ToolWorkflowBinding()

    tool.attach(
        "scan-flow",
        "scanner"
    )

    assert tool.get_tool(
        "scan-flow"
    ) == "scanner"



    memory = MemoryWorkflowBinding()

    memory.save(
        "execution data"
    )

    assert len(
        memory.recall()
    ) == 1



    intelligence = IntelligenceWorkflowBinding()

    result = intelligence.analyze(
        "workflow"
    )

    assert result["optimized"]



    optimizer = WorkflowOptimizer()

    result = optimizer.optimize(
        [
            "scan",
            "scan",
            "repair"
        ]
    )

    assert result["after"] == 2



if __name__ == "__main__":

    test_phase9_bindings()

    print(
        "✅ Phase 9 Block 4 (Features 16-20) Binding Tests Passed"
    )