import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.plugins.installer import PluginInstaller
from backend.app.plugins.sandbox import PluginSandbox
from backend.app.plugins.permissions import PluginPermissions
from backend.app.plugins.events import PluginEvents
from backend.app.plugins.communication import PluginCommunication



def test_plugin_runtime():


    installer = PluginInstaller()

    assert installer.install(
        "plugin"
    )["installed"]



    sandbox = PluginSandbox()

    assert sandbox.isolate(
        "plugin"
    )["sandboxed"]



    permissions = PluginPermissions()

    assert permissions.check(
        "read"
    )["allowed"]



    events = PluginEvents()

    events.emit(
        "started"
    )

    assert "started" in events.all()



    communication = PluginCommunication()

    assert communication.send(
        "pluginA",
        "pluginB"
    )["sent"]




if __name__ == "__main__":

    test_plugin_runtime()


    print(
        "✅ Phase 18 Block 2 (Features 6-10) Plugin Tests Passed"
    )