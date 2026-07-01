from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "AtherOS")
    version: str = os.getenv("APP_VERSION", "0.1.0")
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "True") == "True"

    def validate(self):

        if not self.app_name:
            raise ValueError("APP_NAME cannot be empty")

        if self.environment not in (
            "development",
            "testing",
            "production",
        ):
            raise ValueError("Invalid environment")