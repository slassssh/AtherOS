import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.workspace.file_binding import FileBinding
from backend.app.workspace.folder_index import FolderIndex
from backend.app.workspace.search import WorkspaceSearch
from backend.app.workspace.resource_manager import ResourceManager
from backend.app.workspace.memory import WorkspaceMemory



def test_workspace_resources():


    files = FileBinding()

    files.bind(
        "main.py"
    )

    assert "main.py" in files.all()



    folders = FolderIndex()

    folders.add_folder(
        "src"
    )

    assert "src" in folders.folders()



    search = WorkspaceSearch()

    search.add(
        "agent_runtime.py"
    )

    assert "agent_runtime.py" in search.find(
        "agent"
    )



    resources = ResourceManager()

    resources.allocate(
        "cpu",
        10
    )

    assert resources.get(
        "cpu"
    ) == 10



    memory = WorkspaceMemory()

    memory.remember(
        "project context"
    )

    assert "project context" in memory.recall()




if __name__ == "__main__":

    test_workspace_resources()


    print(
        "✅ Phase 14 Block 2 (Features 6-10) Workspace Tests Passed"
    )