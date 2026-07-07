import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.agents.integration import MultiAgentIntegration
from app.agents.registry import AgentRegistry
from app.agents.identity import AgentIdentity
from app.agents.swarm import SwarmExecution
from app.agents.consensus import ConsensusSystem
from app.agents.shared_memory import SharedMemory



def test_phase8_complete_system():


    # launch multi-agent system

    system = MultiAgentIntegration()

    launch = system.launch()

    assert launch["running"]
    assert launch["secure"]



    # create agents

    registry = AgentRegistry()

    agent1 = AgentIdentity(
        "planner-agent"
    )

    agent2 = AgentIdentity(
        "worker-agent"
    )


    registry.register(
        agent1.id,
        agent1
    )

    registry.register(
        agent2.id,
        agent2
    )


    assert len(
        registry.all()
    ) == 2



    # swarm execution

    swarm = SwarmExecution()

    result = swarm.execute(
        [
            agent1.name,
            agent2.name
        ],
        "autonomous-task"
    )

    assert result["success"]



    # shared memory

    memory = SharedMemory()

    memory.add(
        result
    )

    assert len(
        memory.recall()
    ) == 1



    # consensus

    consensus = ConsensusSystem()

    consensus.vote(True)
    consensus.vote(True)
    consensus.vote(False)

    assert consensus.consensus()



if __name__ == "__main__":

    test_phase8_complete_system()

    print(
        "🎉 AtherOS v0.8 Multi-Agent System Complete"
    )