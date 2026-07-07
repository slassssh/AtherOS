import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from desktop.app.ui.command_center import CommandCenter
from desktop.app.ui.agent_dashboard import AgentDashboard
from desktop.app.ui.memory_dashboard import MemoryDashboard
from desktop.app.ui.workflow_dashboard import WorkflowDashboard
from desktop.app.ui.tool_dashboard import ToolDashboard



def test_desktop_dashboards():


    command = CommandCenter()

    assert command.execute(
        "scan"
    )["executed"]



    agents = AgentDashboard()

    agents.add_agent(
        "worker-agent"
    )

    assert "worker-agent" in agents.display()



    memory = MemoryDashboard()

    memory.add_memory(
        "context"
    )

    assert "context" in memory.show()



    workflow = WorkflowDashboard()

    workflow.add_workflow(
        "automation"
    )

    assert "automation" in workflow.list()



    tools = ToolDashboard()

    tools.register(
        "terminal"
    )

    assert "terminal" in tools.available()



if __name__ == "__main__":

    test_desktop_dashboards()


    print(
        "✅ v1.3 Desktop UI Block 2 (Features 6-10) Tests Passed"
    )