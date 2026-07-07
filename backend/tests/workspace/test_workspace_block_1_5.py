import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.workspace.core import WorkspaceCore
from backend.app.workspace.project_manager import ProjectManager
from backend.app.workspace.state import WorkspaceState
from backend.app.workspace.sessions import WorkspaceSession
from backend.app.workspace.context import WorkspaceContext



def test_workspace_foundation():


    core = WorkspaceCore()

    assert core.start()["active"]



    projects = ProjectManager()

    projects.create(
        "AtherOS"
    )

    assert "AtherOS" in projects.list_projects()



    state = WorkspaceState()

    state.set(
        "mode",
        "active"
    )

    assert state.get(
        "mode"
    ) == "active"



    session = WorkspaceSession()

    session.create(
        "session-1"
    )

    assert "session-1" in session.all()



    context = WorkspaceContext()

    context.update(
        "goal",
        "autonomy"
    )


    assert context.get_context()["goal"] == "autonomy"




if __name__ == "__main__":

    test_workspace_foundation()


    print(
        "✅ Phase 14 Block 1 (Features 1-5) Workspace Tests Passed"
    )