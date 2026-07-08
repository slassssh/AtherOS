import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.marketplace.core import MarketplaceCore
from backend.app.marketplace.registry import PackageRegistry
from backend.app.marketplace.installer import PackageInstaller
from backend.app.marketplace.integration import MarketplaceIntegration



def test_phase22_complete():


    assert MarketplaceCore().status()["marketplace"]



    registry = PackageRegistry()

    registry.register(
        "AtherOS-plugin"
    )


    assert "AtherOS-plugin" in registry.all()



    assert PackageInstaller().install(
        "plugin"
    )["installed"]



    result = MarketplaceIntegration().launch()


    assert result["running"]

    assert result["intelligent"]

    assert result["secure"]




if __name__ == "__main__":

    test_phase22_complete()


    print(
        "🎉 Phase 22 Marketplace Complete"
    )