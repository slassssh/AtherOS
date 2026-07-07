import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.workspace.agent_binding import AgentWorkspaceBinding
from backend.app.workspace.workflow_binding import WorkflowWorkspaceBinding
from backend.app.workspace.tool_binding import ToolWorkspaceBinding
from backend.app.workspace.document_binding import DocumentBinding
from backend.app.workspace.code_binding import CodeBinding



def test_workspace_bindings():


    agents = AgentWorkspaceBinding()

    agents.bind("agent-1")

    assert "agent-1" in agents.all()



    workflow = WorkflowWorkspaceBinding()

    workflow.bind("auto-flow")

    assert "auto-flow" in workflow.all()



    tools = ToolWorkspaceBinding()

    tools.bind("terminal")

    assert "terminal" in tools.all()



    docs = DocumentBinding()

    docs.attach("readme.md")

    assert "readme.md" in docs.all()



    code = CodeBinding()

    code.attach("AtherOS")

    assert "AtherOS" in code.all()




if __name__ == "__main__":

    test_workspace_bindings()


    print(
        "✅ Phase 14 Block 4 (Features 16-20) Workspace Tests Passed"
    )