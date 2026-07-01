from abc import ABC, abstractmethod

from backend.app.utils.logger import logger


class Database(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass


class DatabaseConnection(Database):

    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True
        logger.info("Database connected.")

    def disconnect(self):
        self.connected = False
        logger.info("Database disconnected.")