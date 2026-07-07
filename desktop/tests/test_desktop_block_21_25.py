import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from desktop.app.ui.graph_view import GraphView
from desktop.app.ui.agent_network import AgentNetworkView
from desktop.app.ui.workflow_builder import WorkflowBuilder
from desktop.app.ui.timeline_viewer import TimelineViewer
from desktop.app.ui.system_monitor import SystemMonitorUI



def test_visual_layer():


    graph = GraphView()

    graph.add_node(
        "memory"
    )

    assert graph.connect(
        "memory",
        "agent"
    )



    network = AgentNetworkView()

    network.register(
        "agent-1"
    )

    assert "agent-1" in network.view()



    builder = WorkflowBuilder()

    builder.add_step(
        "execute"
    )

    assert "execute" in builder.build()["workflow"]



    timeline = TimelineViewer()

    timeline.add_event(
        "started"
    )

    assert "started" in timeline.timeline()



    monitor = SystemMonitorUI()

    monitor.update(
        "cpu",
        "10%"
    )

    assert monitor.status()["cpu"] == "10%"



if __name__ == "__main__":

    test_visual_layer()


    print(
        "✅ v1.3 Desktop UI Block 5 (Features 21-25) Tests Passed"
    )