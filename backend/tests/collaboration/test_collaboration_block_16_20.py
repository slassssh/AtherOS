import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.collaboration.agent_sharing import AgentSharing
from backend.app.collaboration.workflow_sharing import WorkflowSharing
from backend.app.collaboration.document_sharing import DocumentSharing
from backend.app.collaboration.intelligence import TeamIntelligence
from backend.app.collaboration.controller import CollaborationController



def test_team_intelligence():


    assert AgentSharing().share(
        "agent"
    )["shared"]


    assert WorkflowSharing().share(
        "workflow"
    )["shared"]


    assert DocumentSharing().share(
        "document"
    )["shared"]


    assert TeamIntelligence().analyze()["team_ai"]


    assert CollaborationController().start()["running"]




if __name__ == "__main__":

    test_team_intelligence()


    print(
        "✅ Phase 21 Block 4 (Features 16-20) Collaboration Tests Passed"
    )