import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.config.settings import Settings

# Valid settings
settings = Settings()
settings.validate()
print("✓ Valid settings passed")

# Invalid app name
try:
    invalid = Settings(app_name="")
    invalid.validate()
except ValueError as e:
    print(e)

# Invalid environment
try:
    invalid = Settings(environment="abc")
    invalid.validate()
except ValueError as e:
    print(e)