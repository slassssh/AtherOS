import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.intelligence.reflection import ReflectionEngine
from backend.app.intelligence.evaluation import SelfEvaluation
from backend.app.intelligence.retry import RetryEngine
from backend.app.intelligence.feedback import FeedbackLoop
from backend.app.intelligence.learning import LearningLoop


reflection = ReflectionEngine()

evaluation = SelfEvaluation()

retry = RetryEngine()

feedback = FeedbackLoop()

learning = LearningLoop()


print(
    reflection.reflect(
        "run_tool",
        "success"
    )
)


print(
    evaluation.evaluate(
        True
    )
)


print(
    retry.should_retry(
        1
    )
)


print(
    feedback.process(
        "good result"
    )
)


print(
    learning.learn(
        "completed task"
    )
)