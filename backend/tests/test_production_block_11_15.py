import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


from app.core.agent_loop import AgentRuntimeLoop
from app.core.dag_engine import WorkflowDAG
from app.core.workers import BackgroundWorker
from app.core.message_broker import MessageBroker
from app.core.task_store import TaskStore



def test_phase11_engine_layer():


    loop = AgentRuntimeLoop()

    assert loop.start()

    assert loop.tick()["executed"]



    dag = WorkflowDAG()

    dag.add_node(
        "A"
    )

    dag.add_node(
        "B"
    )

    assert dag.connect(
        "A",
        "B"
    )



    worker = BackgroundWorker()

    worker.add_job(
        "scan"
    )

    assert worker.run_next() == "scan"



    broker = MessageBroker()

    broker.publish(
        "hello"
    )

    assert broker.consume() == "hello"



    store = TaskStore()

    store.save(
        "1",
        "mission"
    )

    assert store.get(
        "1"
    ) == "mission"



if __name__ == "__main__":

    test_phase11_engine_layer()

    print(
        "✅ Phase 11 Block 3 (Features 11-15) Engine Tests Passed"
    )