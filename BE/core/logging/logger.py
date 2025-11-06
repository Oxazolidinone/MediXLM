"""Logging setup."""
import logging
import sys
from typing import Optional

from core.config import settings


def setup_logging():
    """Setup application logging."""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get logger instance."""
    return logging.getLogger(name or __name__)
