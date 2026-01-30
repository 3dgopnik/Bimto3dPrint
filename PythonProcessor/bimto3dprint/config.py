"""Configuration loader for the pipeline.

Example:
    from pathlib import Path
    config = load_config(Path("config.json"))
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def load_config(path: Path) -> Dict[str, Any]:
    """Load a JSON configuration file.

    Args:
        path: Path to the JSON config.

    Returns:
        Parsed configuration dictionary.
    """
    # TODO: Add schema validation.
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)
