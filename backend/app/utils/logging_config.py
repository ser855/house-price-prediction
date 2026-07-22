"""
utils/logging_config.py

Minimal logging setup so startup/prediction messages show up cleanly
in the terminal running uvicorn.
"""

import logging


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
