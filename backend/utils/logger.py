"""
Structured logging configuration for the application.
"""

import logging
import sys


def setup_logger(name: str = "review_generator") -> logging.Logger:
    """Create and configure the application logger."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Console handler with structured format
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# Shared logger instance used across all modules
logger = setup_logger()
