import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.agents.communication import AgentCommunication
from app.agents.message_bus import MessageBus
from app.agents.event_router import EventRouter
from app.agents.discovery import AgentDiscovery
from app.agents.heartbeat import AgentHeartbeat



def test_phase8_agent_network():


    comm = AgentCommunication()

    msg = comm.send(
        "agent1",
        "agent2",
        "hello"
    )

    assert msg["message"] == "hello"



    bus = MessageBus()

    bus.publish(
        "event"
    )

    assert bus.consume() == "event"



    router = EventRouter()

    router.add_route(
        "scan",
        "scanner"
    )

    assert router.route(
        "scan"
    ) == "scanner"



    discovery = AgentDiscovery()

    discovery.announce(
        "agent1"
    )

    assert "agent1" in discovery.discover()



    heartbeat = AgentHeartbeat()

    heartbeat.ping(
        "agent1"
    )

    assert heartbeat.status(
        "agent1"
    )



if __name__ == "__main__":

    test_phase8_agent_network()

    print(
        "✅ Phase 8 Block 2 (Features 6-10) Agent Network Tests Passed"
    )