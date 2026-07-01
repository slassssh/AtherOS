from backend.app.config.config import settings
from backend.app.database.connection import DatabaseConnection
from backend.app.utils.logger import logger
from backend.app.utils.exceptions import AtherOSError

def main():

    logger.info(f"Starting {settings.app_name} v{settings.version}")

    db = DatabaseConnection()

    db.connect()

    logger.info("Application started successfully.")

    db.disconnect()


if __name__ == "__main__":
    try:
        main()

    except AtherOSError as error:
        logger.error(error)

    except Exception as error:
        logger.exception(error)