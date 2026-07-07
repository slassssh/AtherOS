import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.workspace.activity import ActivityTracker
from backend.app.workspace.timeline import HistoryTimeline
from backend.app.workspace.snapshot import SnapshotManager
from backend.app.workspace.restore import RestorePoint
from backend.app.workspace.sync import WorkspaceSync



def test_workspace_history():


    activity = ActivityTracker()

    activity.track(
        "opened project"
    )

    assert "opened project" in activity.history()



    timeline = HistoryTimeline()

    timeline.add_event(
        "created"
    )

    assert "created" in timeline.show()



    snapshot = SnapshotManager()

    snapshot.create(
        "v1",
        {"files": 10}
    )


    assert snapshot.get(
        "v1"
    )["files"] == 10



    restore = RestorePoint()

    restore.save(
        "safe",
        "state"
    )


    assert restore.restore(
        "safe"
    ) == "state"



    sync = WorkspaceSync()

    assert sync.sync()["synced"]




if __name__ == "__main__":

    test_workspace_history()


    print(
        "✅ Phase 14 Block 3 (Features 11-15) Workspace Tests Passed"
    )