from abc import ABC, abstractmethod
from typing import Optional, Generator
import sqlite3

from backend.app.config.config import settings
from backend.app.utils.logger import logger

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session, declarative_base
    HAS_SQLALCHEMY = True
    Base = declarative_base()
except ImportError:
    HAS_SQLALCHEMY = False
    Base = object


class Database(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass


class DatabaseConnection(Database):

    def __init__(self, db_url: Optional[str] = None):
        self.db_url = db_url or settings.database_url
        self.connected = False
        self.engine = None
        self._session_factory = None
        self._sqlite_conn = None

    def connect(self):
        try:
            if HAS_SQLALCHEMY:
                connect_args = {"check_same_thread": False} if "sqlite" in self.db_url else {}
                self.engine = create_engine(self.db_url, connect_args=connect_args, pool_pre_ping=True)
                Base.metadata.create_all(bind=self.engine)
                self._session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            else:
                db_file = self.db_url.replace("sqlite:///", "")
                self._sqlite_conn = sqlite3.connect(db_file, check_same_thread=False)
            self.connected = True
            logger.info(f"Database connected to {self.db_url}.")
        except Exception as error:
            logger.error(f"Failed to connect to database: {error}")
            raise

    def disconnect(self):
        if self.engine:
            self.engine.dispose()
        if self._sqlite_conn:
            self._sqlite_conn.close()
        self.connected = False
        logger.info("Database disconnected.")

    def get_session(self):
        if not self.connected:
            self.connect()
        if HAS_SQLALCHEMY and self._session_factory:
            return self._session_factory()
        return self._sqlite_conn

    def session_scope(self):
        if HAS_SQLALCHEMY:
            session = self.get_session()
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()
        else:
            conn = self.get_session()
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise