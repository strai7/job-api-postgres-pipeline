from extract import fetch_all_jobs
from database import create_table
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
    create_table()
    pages = fetch_all_jobs()
    load_raw_pages(pages)

    logger.info("Job API pipeline completed successfully")

if __name__ == "__main__":
    main()
