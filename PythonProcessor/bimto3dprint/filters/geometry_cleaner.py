"""Geometry cleanup utilities.

Example:
    cleaned = clean_geometry(mesh)
"""
from __future__ import annotations

from typing import Any


def clean_geometry(mesh: Any) -> Any:
    """Clean mesh geometry for printing.

    Args:
        mesh: Mesh-like object.

    Returns:
        Cleaned mesh.
    """
    # TODO: Remove self-intersections and non-manifold edges.
    return mesh
