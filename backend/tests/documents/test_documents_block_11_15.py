import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.documents.semantic import SemanticAnalyzer
from backend.app.documents.entity_extractor import EntityExtractor
from backend.app.documents.qa import DocumentQA
from backend.app.documents.knowledge_linker import KnowledgeLinker
from backend.app.documents.timeline import DocumentTimeline



def test_document_intelligence():


    semantic = SemanticAnalyzer()

    assert semantic.analyze(
        "AI document"
    )["meaning_found"]



    entity = EntityExtractor()

    assert "AtherOS" in entity.extract(
        "AtherOS system"
    )["entities"]



    qa = DocumentQA()

    assert qa.answer(
        "what?",
        "answer"
    )["answer"] == "answer"



    linker = KnowledgeLinker()

    assert linker.link(
        "doc",
        "memory"
    )



    timeline = DocumentTimeline()

    timeline.add(
        "created"
    )


    assert "created" in timeline.history()




if __name__ == "__main__":

    test_document_intelligence()


    print(
        "✅ Phase 15 Block 3 (Features 11-15) Document Tests Passed"
    )