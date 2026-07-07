import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.documents.core import DocumentCore
from backend.app.documents.loader import DocumentLoader
from backend.app.documents.search import DocumentSearch
from backend.app.documents.integration import DocumentIntegration



def test_phase15_complete():


    core = DocumentCore()

    assert core.status()["document_engine"]



    loader = DocumentLoader()

    loader.load(
        "research.pdf"
    )


    assert "research.pdf" in loader.all()



    search = DocumentSearch()

    search.add(
        "AtherOS document intelligence"
    )


    assert "AtherOS document intelligence" in search.search(
        "AtherOS"
    )



    final = DocumentIntegration()

    result = final.start()


    assert result["running"]

    assert result["secure"]




if __name__ == "__main__":

    test_phase15_complete()


    print(
        "🎉 Phase 15 Document Intelligence Complete"
    )