import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.workspace.core import WorkspaceCore
from backend.app.workspace.project_manager import ProjectManager
from backend.app.workspace.memory import WorkspaceMemory
from backend.app.workspace.integration import WorkspaceIntegration



def test_phase14_complete():


    core = WorkspaceCore()

    assert core.start()["active"]



    projects = ProjectManager()

    projects.create(
        "AtherOS"
    )


    assert "AtherOS" in projects.list_projects()



    memory = WorkspaceMemory()

    memory.remember(
        "workspace context"
    )


    assert "workspace context" in memory.recall()



    final = WorkspaceIntegration()

    result = final.launch()


    assert result["running"]

    assert result["secure"]




if __name__ == "__main__":

    test_phase14_complete()


    print(
        "🎉 Phase 14 Workspace System Complete"
    )