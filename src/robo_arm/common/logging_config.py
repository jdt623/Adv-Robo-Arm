"""Logging setup used by all driver `__main__` test harnesses."""
from __future__ import annotations

import logging
import sys


def configure(level: int = logging.INFO) -> None:
    """Install a sensible root logger configuration for CLI test harnesses."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )
