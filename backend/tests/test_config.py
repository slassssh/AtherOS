import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.config.config import settings
from backend.app.config.constants import PROJECT_NAME
from backend.app.utils.logger import logger

print(PROJECT_NAME)
print(settings.environment)

logger.info("Logger initialized successfully.")
print(settings.app_name)
print(settings.version)
print(settings.debug)