"""OBJ export utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import trimesh
from loguru import logger


class OBJExporter:
    """Export trimesh meshes to OBJ format."""

    def export(self, mesh: trimesh.Trimesh, output_path: str | Path, metadata: dict[str, Any]) -> None:
        """Export mesh to OBJ.

        Args:
            mesh: Trimesh mesh to export.
            output_path: Output OBJ path.
            metadata: Export metadata (unused, reserved for future use).

        Raises:
            FileNotFoundError: If the output file was not created.
            ValueError: If the exported file is empty.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Exporting OBJ to {}", output_path)
        export_data = trimesh.exchange.export.export_mesh(
            mesh,
            file_type="obj",
            include_normals=True,
        )
        if not export_data:
            raise ValueError("OBJ export produced empty data.")

        if isinstance(export_data, bytes):
            export_text = export_data.decode("utf-8")
        else:
            export_text = export_data

        output_path.write_text(export_text, encoding="utf-8")
        if not output_path.exists():
            raise FileNotFoundError(f"OBJ file was not created: {output_path}")
        if output_path.stat().st_size <= 0:
            raise ValueError(f"OBJ file is empty: {output_path}")
        logger.info("OBJ export completed ({} bytes)", output_path.stat().st_size)
