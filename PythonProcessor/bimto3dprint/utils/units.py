"""Mesh unit detection and normalization helpers."""
from __future__ import annotations

from typing import Literal

import numpy as np
import trimesh
from loguru import logger


def detect_mesh_units(mesh: trimesh.Trimesh) -> Literal["meters", "millimeters"]:
    """Detect mesh units using bounding box heuristics.

    Args:
        mesh: Input mesh.

    Returns:
        "meters" or "millimeters" based on bounding box size.
    """
    if mesh.is_empty:
        raise ValueError("Input mesh is empty.")

    max_extent = float(np.max(mesh.extents))
    if max_extent > 50.0:
        units: Literal["meters", "millimeters"] = "meters"
        reason = "max_extent > 50"
    elif max_extent < 5.0:
        units = "millimeters"
        reason = "max_extent < 5"
    else:
        units = "meters"
        reason = "ambiguous range, defaulting to meters"

    logger.info(
        "Detected mesh units: {} (max_extent={:.3f}, reason={})",
        units,
        max_extent,
        reason,
    )
    return units


def normalize_to_millimeters(mesh: trimesh.Trimesh) -> tuple[trimesh.Trimesh, float]:
    """Normalize mesh units to millimeters.

    Args:
        mesh: Input mesh.

    Returns:
        Tuple of (normalized mesh, scale factor applied).
    """
    units = detect_mesh_units(mesh)
    scale_factor = 1000.0 if units == "meters" else 1.0

    normalized = mesh.copy()
    if scale_factor != 1.0:
        normalized.apply_scale(scale_factor)
    logger.info("Normalized mesh to millimeters (scale_factor={:.3f})", scale_factor)
    return normalized, scale_factor
