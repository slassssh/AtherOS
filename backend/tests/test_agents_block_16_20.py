import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.agents.shared_memory import SharedMemory
from app.agents.shared_context import SharedContext
from app.agents.knowledge_exchange import KnowledgeExchange
from app.agents.team_planning import TeamPlanning
from app.agents.swarm import SwarmExecution



def test_phase8_swarm_layer():


    memory = SharedMemory()

    memory.add(
        "threat data"
    )

    assert len(memory.recall()) == 1



    context = SharedContext()

    context.update(
        "mission",
        "defense"
    )

    assert context.get(
        "mission"
    ) == "defense"



    exchange = KnowledgeExchange()

    data = exchange.share(
        "agent1",
        "new pattern"
    )

    assert data["info"] == "new pattern"



    planner = TeamPlanning()

    plan = planner.create(
        ["a1", "a2"],
        "protect"
    )

    assert plan["goal"] == "protect"



    swarm = SwarmExecution()

    result = swarm.execute(
        ["a1", "a2"],
        "scan"
    )

    assert result["success"]



if __name__ == "__main__":

    test_phase8_swarm_layer()

    print(
        "✅ Phase 8 Block 4 (Features 16-20) Swarm Tests Passed"
    )