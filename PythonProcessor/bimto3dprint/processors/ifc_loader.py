"""IFC loader module.

Example:
    model = load_ifc(Path("model.ifc"))
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def load_ifc(path: Path) -> Any:
    """Load an IFC file.

    Args:
        path: Path to IFC file.

    Returns:
        IFC model instance.
    """
    # TODO: Use ifcopenshell to load the model.
    return {"path": str(path)}
