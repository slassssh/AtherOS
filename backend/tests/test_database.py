import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.database.connection import DatabaseConnection

db = DatabaseConnection()

print(db.connected)

db.connect()

print(db.connected)

db.disconnect()

print(db.connected)