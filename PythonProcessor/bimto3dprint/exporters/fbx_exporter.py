"""FBX export utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import trimesh
from loguru import logger


class FBXExporter:
    """Export trimesh meshes to FBX when supported."""

    def export(self, mesh: trimesh.Trimesh, output_path: str | Path, metadata: dict[str, Any]) -> None:
        """Export mesh to FBX.

        Args:
            mesh: Trimesh mesh to export.
            output_path: Output FBX path.
            metadata: Export metadata (unused, reserved for future use).

        Raises:
            RuntimeError: If FBX export is not supported.
            FileNotFoundError: If the output file was not created.
            ValueError: If the exported file is empty.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Exporting FBX to {}", output_path)
        try:
            export_data = trimesh.exchange.export.export_mesh(mesh, file_type="fbx")
        except Exception as exc:  # noqa: BLE001 - depends on trimesh backend
            raise RuntimeError(
                "FBX export not supported in this environment; use OBJ"
            ) from exc

        if not export_data:
            raise RuntimeError("FBX export not supported in this environment; use OBJ")

        if isinstance(export_data, str):
            export_bytes = export_data.encode("utf-8")
        else:
            export_bytes = export_data

        output_path.write_bytes(export_bytes)
        if not output_path.exists():
            raise FileNotFoundError(f"FBX file was not created: {output_path}")
        if output_path.stat().st_size <= 0:
            raise ValueError(f"FBX file is empty: {output_path}")
        logger.info("FBX export completed ({} bytes)", output_path.stat().st_size)
