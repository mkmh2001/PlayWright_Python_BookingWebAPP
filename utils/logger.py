import logging
import os
from datetime import datetime

def setup_logger(name: str = "TestLogger") -> logging.Logger:
    """
    Creates a logger that writes to both console and file.
    Logs are stored under test_results/logs with timestamped filenames.
    """
    # Ensure logs directory exists
    log_dir = os.path.join(os.getcwd(), "test_results", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Timestamped log filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"run_{timestamp}.log")

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding handlers twice
    if not logger.handlers:
        # File handler
        fh = logging.FileHandler(log_file, mode="a")
        fh.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Format
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add handlers
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger
