import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.execution.core import ExecutionCore
from app.execution.graph import ExecutionGraph
from app.execution.node import ExecutionNode
from app.execution.state import ExecutionState
from app.execution.context import ExecutionContext



def test_phase10_execution_core():


    core = ExecutionCore()

    assert core.start()

    assert core.status()



    graph = ExecutionGraph()

    graph.add_node(
        "node1"
    )

    assert len(
        graph.all_nodes()
    ) == 1



    node = ExecutionNode(
        "scan"
    )

    result = node.execute()

    assert result["completed"]



    state = ExecutionState()

    state.change(
        "running"
    )

    assert state.current() == "running"



    context = ExecutionContext()

    context.set(
        "mode",
        "auto"
    )

    assert context.get(
        "mode"
    ) == "auto"



if __name__ == "__main__":

    test_phase10_execution_core()

    print(
        "✅ Phase 10 Block 1 (Features 1-5) Execution Core Tests Passed"
    )