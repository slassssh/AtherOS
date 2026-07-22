from typing import Generator, Optional
from backend.app.core.engine import Engine
from backend.app.database.connection import DatabaseConnection

# Singletons for stateless FastAPI dependency injection
_engine_instance: Optional[Engine] = None
_db_instance: Optional[DatabaseConnection] = None


def get_engine() -> Engine:
    """
    Dependency injection provider for the core Engine.
    Ensures API routes interact solely with the Engine interface.
    """
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = Engine()
    return _engine_instance


def set_engine(engine: Engine) -> None:
    """
    Override engine instance (useful for testing or initialization).
    """
    global _engine_instance
    _engine_instance = engine


def get_db() -> DatabaseConnection:
    """
    Dependency injection provider for DatabaseConnection.
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseConnection()
    return _db_instance


def get_current_user() -> Optional[dict]:
    """
    Authentication hook placeholder.
    Allows adding authentication without altering endpoint signatures.
    """
    return None
