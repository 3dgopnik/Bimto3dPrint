"""STL export utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import trimesh
from loguru import logger


class STLExporter:
    """Export trimesh meshes to binary STL."""

    def export(self, mesh: trimesh.Trimesh, output_path: str | Path, metadata: dict[str, Any]) -> None:
        """Export mesh to binary STL.

        Args:
            mesh: Trimesh mesh to export.
            output_path: Target file path.
            metadata: Export metadata (unused, reserved for future use).

        Raises:
            FileNotFoundError: If the output file was not created.
            ValueError: If the exported file is empty.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Exporting STL to {}", output_path)
        export_data = trimesh.exchange.export.export_mesh(mesh, file_type="stl")
        if not export_data:
            raise ValueError("STL export produced empty data.")

        if isinstance(export_data, str):
            export_bytes = export_data.encode("utf-8")
        else:
            export_bytes = export_data

        output_path.write_bytes(export_bytes)
        if not output_path.exists():
            raise FileNotFoundError(f"STL file was not created: {output_path}")
        if output_path.stat().st_size <= 0:
            raise ValueError(f"STL file is empty: {output_path}")
        logger.info("STL export completed ({} bytes)", output_path.stat().st_size)
