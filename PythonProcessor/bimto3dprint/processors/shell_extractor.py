"""Building shell extractor.

Example:
    shell_mesh = extract_shell(model, config)
"""
from __future__ import annotations

from typing import Any, Dict


def extract_shell(model: Any, config: Dict[str, Any]) -> Any:
    """Extract the building shell geometry from IFC.

    Args:
        model: IFC model instance.
        config: Configuration dictionary.

    Returns:
        Mesh-like object.
    """
    # TODO: Integrate IFC_BuildingEnvExtractor logic.
    return {"shell": True}
