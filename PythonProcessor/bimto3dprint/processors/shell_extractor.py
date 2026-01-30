"""Building shell extraction module.

Example:
    from pathlib import Path

    extractor = ShellExtractor()
    shell = extractor.extract_from_ifc(Path("model.ifc"), {"categories": ["IfcWall", "IfcRoof"]})
    shell = extractor.ensure_watertight(shell)
    shell = extractor.simplify_shell(shell, "medium")
    shell = extractor.scale_for_printer(shell, 450.0)
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import ifcopenshell
import ifcopenshell.geom
import numpy as np
import trimesh
from loguru import logger

from bimto3dprint.integrations.ifc_env_extractor import IfcEnvExtractorRunner


DEFAULT_CATEGORIES: tuple[str, ...] = (
    "IfcWall",
    "IfcWallStandardCase",
    "IfcCurtainWall",
    "IfcSlab",
    "IfcRoof",
    "IfcCovering",
    "IfcColumn",
    "IfcBeam",
)


@dataclass
class ShellExtractor:
    """Extract a simplified building envelope mesh from IFC geometry."""

    def extract_from_ifc(self, ifc_path: Path | str, config: Mapping[str, Any]) -> trimesh.Trimesh:
        """Load IFC and extract a building envelope mesh.

        Args:
            ifc_path: Path to the IFC file.
            config: Configuration mapping with extraction options.

        Returns:
            Envelope mesh as trimesh.Trimesh.

        Raises:
            FileNotFoundError: If the IFC file does not exist.
            ValueError: If no geometry could be extracted.
        """
        path = Path(ifc_path)
        if not path.exists():
            raise FileNotFoundError(f"IFC file not found: {path}")

        logger.info("Opening IFC file: {}", path)
        if "tudelft_extractor" in config:
            return self._extract_with_tudelft(path, config["tudelft_extractor"])

        model = ifcopenshell.open(str(path))

        categories: Sequence[str] | Mapping[str, Any] = config.get("categories", DEFAULT_CATEGORIES)
        if isinstance(categories, Mapping):
            categories = categories.get("include", DEFAULT_CATEGORIES)
        mesh_list = self._collect_meshes(model, categories)
        if not mesh_list:
            raise ValueError("No geometry extracted from IFC elements.")

        combined = trimesh.util.concatenate(mesh_list)
        logger.info("Combined mesh: vertices={}, faces={}", len(combined.vertices), len(combined.faces))

        envelope = self._extract_envelope(combined, config)
        logger.info("Envelope mesh: vertices={}, faces={}", len(envelope.vertices), len(envelope.faces))
        return envelope

    def simplify_shell(self, mesh: trimesh.Trimesh, level: str | float) -> trimesh.Trimesh:
        """Simplify the shell mesh using quadratic decimation.

        Args:
            mesh: Input mesh.
            level: "low", "medium", "high" or ratio in (0, 1].

        Returns:
            Simplified mesh.
        """
        ratio_map = {"low": 0.25, "medium": 0.5, "high": 0.75}
        if isinstance(level, str):
            ratio = ratio_map.get(level.lower())
            if ratio is None:
                raise ValueError(f"Unsupported simplification level: {level}")
        else:
            ratio = float(level)

        ratio = min(max(ratio, 0.05), 1.0)
        target_faces = max(int(len(mesh.faces) * ratio), 100)
        logger.info("Simplifying mesh to ~{} faces (ratio={:.2f})", target_faces, ratio)

        simplified = mesh.simplify_quadratic_decimation(target_faces)
        simplified.remove_unreferenced_vertices()
        return simplified

    def ensure_watertight(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Repair mesh to make it watertight when possible.

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
        logger.info("Filled {} holes", holes_filled)

        if not repaired.is_watertight:
            logger.warning("Mesh is still not watertight after repair")

        return repaired

    def scale_for_printer(self, mesh: trimesh.Trimesh, target_size_mm: float | Sequence[float]) -> trimesh.Trimesh:
        """Scale and center mesh to fit printer volume.

        Args:
            mesh: Input mesh.
            target_size_mm: Single value or (x, y, z) build volume in mm.

        Returns:
            Scaled mesh centered around origin.
        """
        if isinstance(target_size_mm, (int, float)):
            target = np.array([target_size_mm] * 3, dtype=float)
        else:
            target = np.array(list(target_size_mm), dtype=float)

        extents = np.array(mesh.extents, dtype=float)
        if np.any(extents <= 0):
            raise ValueError("Mesh extents are invalid for scaling")

        scale_factor = float(np.min(target / extents))
        logger.info("Scaling mesh by factor {:.4f}", scale_factor)

        scaled = mesh.copy()
        scaled.apply_translation(-scaled.centroid)
        scaled.apply_scale(scale_factor)
        return scaled

    def _collect_meshes(self, model: ifcopenshell.file, categories: Sequence[str]) -> list[trimesh.Trimesh]:
        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)
        settings.set(settings.INCLUDE_CURVES, False)

        meshes: list[trimesh.Trimesh] = []
        for category in categories:
            elements = model.by_type(category)
            logger.info("Collecting elements: {} (count={})", category, len(elements))
            for element in elements:
                try:
                    shape = ifcopenshell.geom.create_shape(settings, element)
                except Exception as exc:  # noqa: BLE001 - IFC geometry failures are expected
                    logger.warning("Failed to create shape for {}: {}", element.GlobalId, exc)
                    continue

                geometry = shape.geometry
                vertices = np.array(geometry.verts, dtype=float).reshape(-1, 3)
                faces = np.array(geometry.faces, dtype=int).reshape(-1, 3)
                if len(vertices) == 0 or len(faces) == 0:
                    continue

                mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
                mesh.remove_unreferenced_vertices()
                meshes.append(mesh)

        return meshes

    def _extract_envelope(self, mesh: trimesh.Trimesh, config: Mapping[str, Any]) -> trimesh.Trimesh:
        method = str(config.get("method", "voxel")).lower()

        if method == "convex_hull":
            logger.info("Using convex hull for envelope extraction")
            return mesh.convex_hull

        max_extent = float(np.max(mesh.extents))
        pitch = float(config.get("voxel_pitch", max(max_extent / 200.0, 1.0)))
        logger.info("Using voxel envelope with pitch {:.3f}", pitch)

        voxel_grid = mesh.voxelized(pitch)
        voxel_grid = voxel_grid.fill()
        envelope = voxel_grid.marching_cubes
        envelope.remove_unreferenced_vertices()
        return envelope

    def _extract_with_tudelft(self, ifc_path: Path, config: Mapping[str, Any]) -> trimesh.Trimesh:
        extractor_path = Path(config.get("extractor_path", ""))
        output_dir = Path(config.get("output_dir", ifc_path.parent / "tudelft_envelope"))
        output_dir.mkdir(parents=True, exist_ok=True)

        runner = IfcEnvExtractorRunner(extractor_path)
        lod = float(config.get("lod", 2.2))
        voxel_size = float(config.get("voxel_size", 1.0))
        threads = int(config.get("threads", 8))

        config_payload = runner.build_config(
            ifc_path=ifc_path,
            output_dir=output_dir,
            lods=[lod],
            voxel_size=voxel_size,
            threads=threads,
        )
        config_path = output_dir / "envelope_config.json"
        runner.write_config(config_payload, config_path)
        runner.run(config_path, ifc_path)

        obj_path = runner.find_output_obj(output_dir)
        mesh = trimesh.load(obj_path, force="mesh")
        if not isinstance(mesh, trimesh.Trimesh):  # pragma: no cover - defensive
            raise ValueError(f"Extractor output is not a mesh: {obj_path}")
        extents = np.array(mesh.extents, dtype=float)
        extents_valid = (
            extents.shape == (3,)
            and np.all(np.isfinite(extents))
            and np.all(extents > 0)
        )
        if mesh.is_empty or len(mesh.faces) <= 100 or not extents_valid:
            logger.error(
                "Invalid TU Delft mesh detected (empty={}, faces={}, extents={})",
                mesh.is_empty,
                len(mesh.faces),
                extents,
            )
            raise RuntimeError(
                "TU Delft extractor returned invalid mesh. "
                "Check IFC schema, LoD, voxel size, or extractor executable."
            )
        logger.info("Loaded TU Delft envelope mesh: vertices={}, faces={}", len(mesh.vertices), len(mesh.faces))
        return mesh
