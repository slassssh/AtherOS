import os
import sys

sys.path.append(
    os.path.abspath(".")
)

from backend.app.marketplace.core import MarketplaceCore
from backend.app.marketplace.registry import PackageRegistry
from backend.app.marketplace.search import PackageSearch
from backend.app.marketplace.metadata import PackageMetadata
from backend.app.marketplace.installer import PackageInstaller


def test_marketplace_core():

    assert MarketplaceCore().status()["marketplace"]

    registry = PackageRegistry()

    registry.register("plugin")

    assert "plugin" in registry.all()

    assert PackageSearch().find("plugin")["found"]

    assert PackageMetadata().read("plugin")["metadata"]

    assert PackageInstaller().install("plugin")["installed"]


if __name__ == "__main__":

    test_marketplace_core()

    print(
        "✅ Phase 22 Block 1 (Features 1-5) Marketplace Tests Passed"
    )