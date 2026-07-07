import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.workspace.metrics import WorkspaceMetrics
from backend.app.workspace.security import WorkspaceSecurity
from backend.app.workspace.settings import WorkspaceSettings
from backend.app.workspace.controller import WorkspaceController
from backend.app.workspace.integration import WorkspaceIntegration



def test_workspace_final():


    metrics = WorkspaceMetrics()

    metrics.record(
        "tasks",
        5
    )

    assert metrics.report()["tasks"] == 5



    security = WorkspaceSecurity()

    assert security.verify()["secure"]



    settings = WorkspaceSettings()

    settings.set(
        "mode",
        "auto"
    )

    assert settings.get("mode") == "auto"



    controller = WorkspaceController()

    assert controller.start()



    final = WorkspaceIntegration()

    result = final.launch()


    assert result["running"]

    assert result["secure"]




if __name__ == "__main__":

    test_workspace_final()


    print(
        "✅ Phase 14 Block 5 (Features 21-25) Workspace Tests Passed"
    )