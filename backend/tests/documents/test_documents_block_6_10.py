import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.documents.chunker import DocumentChunker
from backend.app.documents.indexer import DocumentIndexer
from backend.app.documents.search import DocumentSearch
from backend.app.documents.summarizer import DocumentSummarizer
from backend.app.documents.memory import DocumentMemory



def test_document_processing():


    chunker = DocumentChunker()

    assert chunker.chunk(
        "AtherOS"
    )[0] == "Ather"



    index = DocumentIndexer()

    index.add(
        "doc1",
        "content"
    )

    assert index.get(
        "doc1"
    ) == "content"



    search = DocumentSearch()

    search.add(
        "ai document"
    )

    assert "ai document" in search.search(
        "ai"
    )



    summary = DocumentSummarizer()

    assert summary.summarize(
        "abcdefghijklmnopqrstuvwxyz"
    ) == "abcdefghijklmnopqrst"



    memory = DocumentMemory()

    memory.store(
        "knowledge"
    )

    assert "knowledge" in memory.recall()




if __name__ == "__main__":

    test_document_processing()


    print(
        "✅ Phase 15 Block 2 (Features 6-10) Document Tests Passed"
    )