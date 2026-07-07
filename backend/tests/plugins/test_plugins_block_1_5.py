import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.plugins.core import PluginCore
from backend.app.plugins.loader import PluginLoader
from backend.app.plugins.registry import PluginRegistry
from backend.app.plugins.metadata import PluginMetadata
from backend.app.plugins.validator import PluginValidator



def test_plugin_foundation():


    core = PluginCore()

    assert core.status()["plugin_system"]



    loader = PluginLoader()

    loader.load(
        "plugin1"
    )

    assert "plugin1" in loader.all()



    registry = PluginRegistry()

    registry.register(
        "test",
        "plugin"
    )

    assert registry.get(
        "test"
    ) == "plugin"



    metadata = PluginMetadata()

    assert metadata.read(
        "plugin"
    )["metadata"]



    validator = PluginValidator()

    assert validator.validate(
        "plugin"
    )["valid"]




if __name__ == "__main__":

    test_plugin_foundation()


    print(
        "✅ Phase 18 Block 1 (Features 1-5) Plugin Tests Passed"
    )