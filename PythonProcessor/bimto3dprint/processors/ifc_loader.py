"""IFC loader module.

Example:
    from pathlib import Path

    loader = IFCLoader()
    model = loader.load_ifc(Path("model.ifc"))
    elements = loader.get_elements_by_categories(["BuiltInCategory.OST_Walls"])
    mesh = loader.to_trimesh(elements)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import ifcopenshell
import ifcopenshell.geom
import numpy as np
import trimesh
from loguru import logger


DEFAULT_CATEGORY_MAP: Mapping[str, Sequence[str]] = {
    "BuiltInCategory.OST_Walls": ("IfcWall", "IfcWallStandardCase"),
    "BuiltInCategory.OST_Roofs": ("IfcRoof",),
    "BuiltInCategory.OST_Floors": ("IfcSlab",),
    "BuiltInCategory.OST_CurtainWallPanels": ("IfcCurtainWall",),
    "BuiltInCategory.OST_CurtainWallMullions": ("IfcCurtainWall",),
    "BuiltInCategory.OST_StructuralWall": ("IfcWall", "IfcWallStandardCase"),
    "BuiltInCategory.OST_Columns": ("IfcColumn",),
    "BuiltInCategory.OST_StructuralColumns": ("IfcColumn",),
    "BuiltInCategory.OST_Beams": ("IfcBeam",),
    "BuiltInCategory.OST_StructuralFraming": ("IfcBeam",),
}


@dataclass
class IFCLoader:
    """Load IFC files and convert selected elements to trimesh."""

    category_map: Mapping[str, Sequence[str]] = field(default_factory=lambda: DEFAULT_CATEGORY_MAP)
    model: ifcopenshell.file | None = None
    _settings: ifcopenshell.geom.settings = field(default_factory=ifcopenshell.geom.settings)

    def __post_init__(self) -> None:
        self._settings.set(self._settings.USE_WORLD_COORDS, True)
        self._settings.set(self._settings.INCLUDE_CURVES, False)

    def load_ifc(self, path: Path | str) -> ifcopenshell.file:
        """Load an IFC file from disk.

        Args:
            path: Path to the IFC file.

        Returns:
            Opened IFC model.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        ifc_path = Path(path)
        if not ifc_path.exists():
            raise FileNotFoundError(f"IFC file not found: {ifc_path}")

        logger.info("Opening IFC file: {}", ifc_path)
        self.model = ifcopenshell.open(str(ifc_path))
        return self.model

    def get_elements_by_categories(self, categories: Iterable[str]) -> list[ifcopenshell.entity_instance]:
        """Collect IFC elements by category names.

        Args:
            categories: Category labels from configuration or IFC class names.

        Returns:
            List of IFC elements to process.

        Raises:
            ValueError: If IFC model is not loaded.
        """
        if self.model is None:
            raise ValueError("IFC model is not loaded. Call load_ifc() first.")

        elements: list[ifcopenshell.entity_instance] = []
        for category in categories:
            ifc_types = self.category_map.get(category, (category,))
            for ifc_type in ifc_types:
                matched = self.model.by_type(ifc_type)
                logger.info("Category {} -> {} (count={})", category, ifc_type, len(matched))
                elements.extend(matched)

        unique = {element.id(): element for element in elements}
        logger.info("Collected {} unique elements", len(unique))
        return list(unique.values())

    def extract_geometry(self, element: ifcopenshell.entity_instance) -> trimesh.Trimesh | None:
        """Extract element geometry as a trimesh.

        Args:
            element: IFC entity instance.

        Returns:
            trimesh.Trimesh or None if geometry could not be created.
        """
        try:
            shape = ifcopenshell.geom.create_shape(self._settings, element)
        except Exception as exc:  # noqa: BLE001 - IFC geometry failures are expected
            logger.warning("Failed to create geometry for {}: {}", element.GlobalId, exc)
            return None

        geometry = shape.geometry
        vertices = np.array(geometry.verts, dtype=float).reshape(-1, 3)
        faces = np.array(geometry.faces, dtype=int).reshape(-1, 3)
        if len(vertices) == 0 or len(faces) == 0:
            logger.warning("Empty geometry for {}", element.GlobalId)
            return None

        mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
        mesh.remove_unreferenced_vertices()
        return mesh

    def to_trimesh(self, elements: Iterable[ifcopenshell.entity_instance]) -> trimesh.Trimesh:
        """Convert IFC elements into a single trimesh mesh.

        Args:
            elements: Iterable of IFC elements.

        Returns:
            Combined mesh.

        Raises:
            ValueError: If no geometry was produced.
        """
        meshes: list[trimesh.Trimesh] = []
        for element in elements:
            mesh = self.extract_geometry(element)
            if mesh is None:
                continue
            meshes.append(mesh)

        if not meshes:
            raise ValueError("No geometry could be extracted from IFC elements.")

        combined = trimesh.util.concatenate(meshes)
        logger.info("Combined mesh: vertices={}, faces={}", len(combined.vertices), len(combined.faces))
        return combined


def load_ifc(path: Path | str) -> ifcopenshell.file:
    """Backward-compatible wrapper for loading IFC files.

    Args:
        path: Path to IFC file.

    Returns:
        IFC model instance.
    """
    return IFCLoader().load_ifc(path)
