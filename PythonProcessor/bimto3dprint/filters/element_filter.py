"""Element filtering logic.

Example:
    filtered = filter_elements(elements, config)
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List


def filter_elements(elements: Iterable[Any], config: Dict[str, Any]) -> List[Any]:
    """Filter elements based on config rules.

    Args:
        elements: IFC elements iterable.
        config: Configuration dictionary.

    Returns:
        Filtered list of elements.
    """
    # TODO: Apply category and parameter filters.
    return list(elements)
