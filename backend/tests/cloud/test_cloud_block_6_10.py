import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.cloud.memory_sync import MemorySync
from backend.app.cloud.agent_sync import AgentSync
from backend.app.cloud.workflow_sync import WorkflowSync
from backend.app.cloud.plugin_sync import PluginSync
from backend.app.cloud.conflict_resolver import ConflictResolver



def test_cloud_sync_layer():


    assert MemorySync().sync(
        "memory"
    )["synced"]


    assert AgentSync().sync(
        "agent"
    )["synced"]


    assert WorkflowSync().sync(
        "workflow"
    )["synced"]


    assert PluginSync().sync(
        "plugin"
    )["synced"]


    assert ConflictResolver().resolve(
        "version mismatch"
    )["resolved"]




if __name__ == "__main__":

    test_cloud_sync_layer()


    print(
        "✅ Phase 20 Block 2 (Features 6-10) Cloud Tests Passed"
    )