from .database import create_postgres_env, validate_sql_files, validate_config
from .logging_config import setup_logging
from .config import POSTGRES_ENV_FILES, LOGGING_ROOT

import logging

logger = logging.getLogger(f"{LOGGING_ROOT}.main")

def main():
    """Main function to set up posgres environment for the job API pipeline."""
    # Set up logging
    setup_logging()

    logger.info("Starting Validation and Postgres Environment Setup for Job API Pipeline")
    try:
        validate_config()
        validate_sql_files(POSTGRES_ENV_FILES)
        create_postgres_env(POSTGRES_ENV_FILES)

    except Exception as e:
        logger.exception(f"An error occurred during the job API pipeline execution: {e}")
        raise

if __name__ == "__main__":
    main()
