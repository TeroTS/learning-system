"""Logging configuration shared by repository scripts."""

import logging
import os
import sys

DEFAULT_LEVEL = "WARNING"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def configure_logging() -> None:
    """Send logs to stderr, keeping stdout for command output. The level comes from LOG_LEVEL (default WARNING)."""
    level_name = os.environ.get("LOG_LEVEL", DEFAULT_LEVEL).upper()
    level = logging.getLevelNamesMapping().get(level_name)
    if level is None:
        raise ValueError(f"Invalid LOG_LEVEL: {level_name}")
    logging.basicConfig(level=level, format=LOG_FORMAT, stream=sys.stderr, force=True)
