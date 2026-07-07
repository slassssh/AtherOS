import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.agents.coordinator import MultiAgentCoordinator
from app.agents.delegation import TaskDelegation
from app.agents.collaboration import CollaborationEngine
from app.agents.conflict import ConflictResolver
from app.agents.consensus import ConsensusSystem



def test_phase8_agent_coordination():


    coordinator = MultiAgentCoordinator()

    coordinator.add_agent(
        "agent1"
    )

    result = coordinator.coordinate()

    assert result["coordinated"]



    delegation = TaskDelegation()

    delegation.assign(
        "agent1",
        "scan"
    )

    assert delegation.owner(
        "scan"
    ) == "agent1"



    collab = CollaborationEngine()

    session = collab.collaborate(
        ["a1", "a2"],
        "security"
    )

    assert session["goal"] == "security"



    conflict = ConflictResolver()

    conflict.detect(
        "resource clash"
    )

    assert conflict.resolve()["resolved"]



    consensus = ConsensusSystem()

    consensus.vote(True)
    consensus.vote(True)
    consensus.vote(False)

    assert consensus.consensus()



if __name__ == "__main__":

    test_phase8_agent_coordination()

    print(
        "✅ Phase 8 Block 3 (Features 11-15) Coordination Tests Passed"
    )