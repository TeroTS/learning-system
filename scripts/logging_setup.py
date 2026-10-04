# Logging configuration shared by repository scripts.
# Call configure_logging() once at each script entry point.

import logging
import os
import sys

DEFAULT_LEVEL = "WARNING"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


# Configure the root logger to write to stderr, keeping stdout free for command output.
# Input: the LOG_LEVEL environment variable (case-insensitive, default WARNING).
# Effect: replaces any existing root handlers. Raises ValueError if LOG_LEVEL is not a known level.
def configure_logging() -> None:
    level_name = os.environ.get("LOG_LEVEL", DEFAULT_LEVEL).upper()
    level = logging.getLevelNamesMapping().get(level_name)
    if level is None:
        raise ValueError(f"Invalid LOG_LEVEL: {level_name}")
    logging.basicConfig(level=level, format=LOG_FORMAT, stream=sys.stderr, force=True)
