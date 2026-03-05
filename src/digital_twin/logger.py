"""
Shared logging configuration for the Digital Twin application.
Import `get_logger` in each module to get a named logger.
"""
import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Returns a named logger. Call once per module:
        logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
            datefmt="%H:%M:%S"
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

    return logger
