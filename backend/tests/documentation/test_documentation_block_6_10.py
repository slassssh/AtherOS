import os
import sys


sys.path.append(
    os.path.abspath(".")
)


from backend.app.documentation.changelog import ChangelogGenerator
from backend.app.documentation.release_notes import ReleaseNotes
from backend.app.documentation.code_docs import CodeDocumentation
from backend.app.documentation.search import DocumentationSearch
from backend.app.documentation.versioning import DocumentationVersioning



def test_documentation_automation_layer():


    assert ChangelogGenerator().generate()["changelog_created"]


    assert ReleaseNotes().generate()["release_notes_created"]


    assert CodeDocumentation().generate()["code_docs_created"]


    assert DocumentationSearch().search(
        "AtherOS"
    )["results_found"]


    assert DocumentationVersioning().version()["version_control"]




if __name__ == "__main__":

    test_documentation_automation_layer()


    print(
        "✅ Phase 25 Block 2 (Features 6-10) Documentation Tests Passed"
    )