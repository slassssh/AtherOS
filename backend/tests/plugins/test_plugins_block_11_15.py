import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.plugins.marketplace import PluginMarketplace
from backend.app.plugins.versioning import PluginVersioning
from backend.app.plugins.updates import PluginUpdater
from backend.app.plugins.metrics import PluginMetrics
from backend.app.plugins.security import PluginSecurity



def test_plugin_marketplace():


    market = PluginMarketplace()

    market.publish(
        "theme-plugin"
    )


    assert "theme-plugin" in market.all()



    version = PluginVersioning()

    assert version.set_version(
        "plugin",
        "1.0"
    )["version"] == "1.0"



    updater = PluginUpdater()

    assert updater.update(
        "plugin"
    )["updated"]



    metrics = PluginMetrics()

    metrics.record(
        "downloads",
        100
    )


    assert metrics.report()["downloads"] == 100



    security = PluginSecurity()

    assert security.scan(
        "plugin"
    )["secure"]




if __name__ == "__main__":

    test_plugin_marketplace()


    print(
        "✅ Phase 18 Block 3 (Features 11-15) Plugin Tests Passed"
    )