import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.plugins.core import PluginCore
from backend.app.plugins.loader import PluginLoader
from backend.app.plugins.marketplace import PluginMarketplace
from backend.app.plugins.integration import PluginIntegration



def test_phase18_complete():


    core = PluginCore()

    assert core.status()["plugin_system"]



    loader = PluginLoader()

    loader.load(
        "ai-plugin"
    )


    assert "ai-plugin" in loader.all()



    market = PluginMarketplace()

    market.publish(
        "extension"
    )


    assert "extension" in market.all()



    final = PluginIntegration()

    result = final.launch()


    assert result["running"]

    assert result["secure"]




if __name__ == "__main__":

    test_phase18_complete()


    print(
        "🎉 Phase 18 Plugin SDK Complete"
    )