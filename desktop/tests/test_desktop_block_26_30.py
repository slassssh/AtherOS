import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from desktop.app.ui.settings import SettingsUI
from desktop.app.ui.plugin_manager import PluginManagerUI
from desktop.app.ui.security_center import SecurityCenter
from desktop.app.ui.logs_viewer import LogsViewer
from desktop.app.ui.performance_dashboard import PerformanceDashboard



def test_management_ui():


    settings = SettingsUI()

    settings.update(
        "theme",
        "dark"
    )

    assert settings.get(
        "theme"
    ) == "dark"



    plugins = PluginManagerUI()

    plugins.install(
        "ai-plugin"
    )

    assert "ai-plugin" in plugins.list_plugins()



    security = SecurityCenter()

    security.alert(
        "safe"
    )

    assert "safe" in security.show_alerts()



    logs = LogsViewer()

    logs.add_log(
        "started"
    )

    assert "started" in logs.view()



    perf = PerformanceDashboard()

    perf.record(
        "speed",
        "fast"
    )

    assert perf.report()["speed"] == "fast"



if __name__ == "__main__":

    test_management_ui()


    print(
        "✅ v1.3 Desktop UI Block 6 (Features 26-30) Tests Passed"
    )