from typing import Any, Dict
from PyQt6.QtCore import QThread, pyqtSignal
from backend.app.core.engine import Engine
from backend.app.utils.logger import logger


class GoalExecutionWorker(QThread):
    """
    QThread worker for running high-level goals asynchronously.
    Prevents PyQt6 GUI thread freezing during complex goal execution.
    """

    finished_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def __init__(self, engine: Engine, goal_text: str):
        super().__init__()
        self.engine = engine
        self.goal_text = goal_text

    def run(self):
        try:
            logger.info(f"GoalExecutionWorker starting for goal: '{self.goal_text}'")
            result = self.engine.execute_autonomous_goal(self.goal_text)
            self.finished_signal.emit(result)
        except Exception as err:
            logger.error(f"GoalExecutionWorker error: {err}")
            self.error_signal.emit(str(err))
