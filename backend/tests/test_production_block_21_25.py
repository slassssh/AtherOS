import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


from app.core.cli import AtherCLI
from app.core.sdk import AtherSDK
from app.core.docs import DocumentationGenerator
from app.core.packaging import PackageBuilder
from app.core.production import ProductionCore



def test_phase11_final_layer():


    cli = AtherCLI()

    cli.register(
        "status",
        lambda: "running"
    )


    assert cli.run(
        "status"
    ) == "running"



    sdk = AtherSDK()

    sdk.add_module(
        "agents",
        object()
    )


    assert sdk.get(
        "agents"
    )



    docs = DocumentationGenerator()

    result = docs.generate(
        [
            "core",
            "runtime"
        ]
    )


    assert result["generated"]



    package = PackageBuilder()

    assert package.build()["ready"]



    production = ProductionCore()

    result = production.launch()

    assert result["production"]

    assert result["secure"]



if __name__ == "__main__":

    test_phase11_final_layer()

    print(
        "✅ Phase 11 Block 5 (Features 21-25) Production Tests Passed"
    )