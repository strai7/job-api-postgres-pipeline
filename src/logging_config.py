import logging
import os
from config import LOGS_DIR
from datetime import datetime

def setup_logging():
    """Configure logging for the pipeline."""

    logger = logging.getLogger("job_api_pipeline")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if setup is accidentally called again.
    if logger.handlers:
        return

    # Create logs directory if it doesn't exist
    logger.info(f"Creating logs directory if it doesn't exist at {LOGS_DIR}")
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Create a timestamped log file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Set up file and console handlers for logging
    file_handler = logging.FileHandler(
        filename=LOGS_DIR / f"job_api_pipeline_{timestamp}.log",
        mode="a",
        encoding="utf-8",
    )
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    for handler in (file_handler, console_handler):
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Prevent log messages from being propagated to the root logger
    logger.propagate = False

