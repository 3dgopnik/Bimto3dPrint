"""Mesh optimization module.

Example:
    from pathlib import Path

    optimizer = MeshOptimizer()
    mesh = trimesh.load(Path("model.stl"))
    cleaned = optimizer.remove_internal_geometry(mesh)
    smoothed = optimizer.smooth_surface(cleaned, iterations=3)
    report = optimizer.validate_for_printing(smoothed)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import trimesh
from loguru import logger


@dataclass
class MeshOptimizer:
    """Optimize meshes for 3D printing workflows."""

    def remove_internal_geometry(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Remove internal faces, keeping only the outer shell.

        Args:
            mesh: Input mesh.

        Returns:
            Mesh approximating the external shell.
        """
        if mesh.is_empty:
            raise ValueError("Input mesh is empty.")

        max_extent = float(np.max(mesh.extents))
        pitch = max(max_extent / 200.0, 1.0)
        logger.info("Removing internal geometry via voxel shell (pitch={:.3f})", pitch)

        voxel_grid = mesh.voxelized(pitch)
        voxel_grid = voxel_grid.fill()
        shell = voxel_grid.marching_cubes
        shell.remove_unreferenced_vertices()
        return shell

    def thicken_walls(self, mesh: trimesh.Trimesh, min_thickness_mm: float = 2.0) -> trimesh.Trimesh:
        """Thicken thin walls using voxel dilation.

        Args:
            mesh: Input mesh.
            min_thickness_mm: Minimum wall thickness in millimeters.

        Returns:
            Thickened mesh.
        """
        if min_thickness_mm <= 0:
            raise ValueError("min_thickness_mm must be positive.")

        if mesh.is_empty:
            raise ValueError("Input mesh is empty.")

        pitch = max(min_thickness_mm / 2.0, 0.5)
        steps = max(int(np.ceil(min_thickness_mm / pitch)), 1)
        logger.info("Thickening walls via voxel dilation (pitch={:.3f}, steps={})", pitch, steps)

        voxel_grid = mesh.voxelized(pitch)
        voxel_grid = voxel_grid.fill()
        voxel_grid = voxel_grid.dilate(steps)
        thickened = voxel_grid.marching_cubes
        thickened.remove_unreferenced_vertices()
        return thickened

    def smooth_surface(self, mesh: trimesh.Trimesh, iterations: int = 3) -> trimesh.Trimesh:
        """Apply Laplacian smoothing for cleaner surfaces.

        Args:
            mesh: Input mesh.
            iterations: Number of smoothing iterations.

        Returns:
            Smoothed mesh.
        """
        if iterations <= 0:
            raise ValueError("iterations must be a positive integer.")

        if mesh.is_empty:
            raise ValueError("Input mesh is empty.")

        smoothed = mesh.copy()
        trimesh.smoothing.filter_laplacian(smoothed, iterations=iterations)
        return smoothed

    def ensure_watertight(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Attempt to repair mesh to become watertight.

        Args:
            mesh: Input mesh.

        Returns:
            Repaired mesh.
        """
        repaired = mesh.copy()
        repaired.remove_degenerate_faces()
        repaired.remove_duplicate_faces()
        repaired.remove_infinite_values()
        repaired.remove_unreferenced_vertices()
        repaired.fix_normals()

        holes_filled = trimesh.repair.fill_holes(repaired)
        logger.info("Filled {} holes during watertight repair", holes_filled)

        if not repaired.is_watertight:
            logger.warning("Mesh is still not watertight after repair")

        return repaired

    def validate_for_printing(self, mesh: trimesh.Trimesh) -> dict[str, Any]:
        """Validate mesh readiness for printing.

        Args:
            mesh: Input mesh.

        Returns:
            Dictionary with validation metrics.
        """
        if mesh.is_empty:
            raise ValueError("Input mesh is empty.")

        has_correct_normals = bool(mesh.is_winding_consistent)
        min_wall_thickness = self._estimate_min_wall_thickness(mesh)
        bounds = tuple(float(value) for value in mesh.bounds.reshape(-1))
        volume = float(mesh.volume) if mesh.is_volume else 0.0

        report = {
            "is_watertight": bool(mesh.is_watertight),
            "has_correct_normals": has_correct_normals,
            "min_wall_thickness": float(min_wall_thickness),
            "bounding_box": bounds,
            "volume": volume,
        }
        logger.info("Validation report: {}", report)
        return report

    def _estimate_min_wall_thickness(self, mesh: trimesh.Trimesh) -> float:
        if mesh.edges_unique_length.size == 0:
            return 0.0
        return float(np.min(mesh.edges_unique_length))
