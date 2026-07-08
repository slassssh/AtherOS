import os
import sys


sys.path.append(
    os.path.abspath(".")
)


from backend.app.documentation.core import DocumentationCore
from backend.app.documentation.api_docs import APIDocumentation
from backend.app.documentation.user_guide import UserGuideGenerator
from backend.app.documentation.developer_guide import DeveloperGuide
from backend.app.documentation.architecture import ArchitectureDocs



def test_documentation_foundation():


    assert DocumentationCore().status()["documentation_enabled"]


    assert APIDocumentation().generate()["api_docs_created"]


    assert UserGuideGenerator().generate()["user_guide_created"]


    assert DeveloperGuide().generate()["developer_guide_created"]


    assert ArchitectureDocs().generate()["architecture_docs_created"]




if __name__ == "__main__":

    test_documentation_foundation()


    print(
        "✅ Phase 25 Block 1 (Features 1-5) Documentation Tests Passed"
    )