from extract import fetch_all_jobs
from database import reset_table
from load import load_raw_pages
from logging_config import setup_logging
from config import LOGGING_ROOT
import logging

logger = logging.getLogger(f"{LOGGING_ROOT}.main")

def main():
    """Main function to run the job API pipeline."""
    # Set up logging
    setup_logging()
    logger.info("Starting job API pipeline")

    # Create the table, fetch all jobs, and load them into the database
    try:
        reset_table()
        pages = fetch_all_jobs()
        load_raw_pages(pages)

    except Exception as e:
        logger.exception(f"An error occurred during the job API pipeline execution: {e}")
        raise

    logger.info("Job API pipeline completed successfully")

if __name__ == "__main__":
    main()
