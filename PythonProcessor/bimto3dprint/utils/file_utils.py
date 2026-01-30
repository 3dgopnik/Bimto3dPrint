"""File helper utilities.

Example:
    ensure_dir(Path("output"))
"""
from __future__ import annotations

from pathlib import Path


def ensure_dir(path: Path) -> None:
    """Ensure directory exists.

    Args:
        path: Directory path.
    """
    path.mkdir(parents=True, exist_ok=True)
