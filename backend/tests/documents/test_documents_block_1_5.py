import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.documents.core import DocumentCore
from backend.app.documents.loader import DocumentLoader
from backend.app.documents.pdf_parser import PDFParser
from backend.app.documents.text_extractor import TextExtractor
from backend.app.documents.metadata import MetadataExtractor



def test_document_core():


    core = DocumentCore()

    assert core.status()["document_engine"]



    loader = DocumentLoader()

    loader.load("paper.pdf")

    assert "paper.pdf" in loader.all()



    parser = PDFParser()

    assert parser.parse(
        "file.pdf"
    )["parsed"]



    text = TextExtractor()

    assert text.extract(
        "doc"
    ) == "text extracted from doc"



    meta = MetadataExtractor()

    assert meta.extract(
        "doc"
    )["metadata"]




if __name__ == "__main__":

    test_document_core()


    print(
        "✅ Phase 15 Block 1 (Features 1-5) Document Tests Passed"
    )