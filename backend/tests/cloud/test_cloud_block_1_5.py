import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.cloud.core import CloudCore
from backend.app.cloud.account_sync import AccountSync
from backend.app.cloud.device_sync import DeviceSync
from backend.app.cloud.file_sync import FileSync
from backend.app.cloud.workspace_sync import WorkspaceSync



def test_cloud_foundation():


    assert CloudCore().connect()["cloud_connected"]


    assert AccountSync().sync(
        "user"
    )["synced"]


    assert DeviceSync().sync(
        "desktop"
    )["synced"]


    assert FileSync().sync(
        "file.py"
    )["synced"]


    assert WorkspaceSync().sync(
        "AtherOS"
    )["synced"]




if __name__ == "__main__":

    test_cloud_foundation()


    print(
        "✅ Phase 20 Block 1 (Features 1-5) Cloud Tests Passed"
    )