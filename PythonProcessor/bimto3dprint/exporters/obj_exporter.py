"""OBJ export utilities.

Example:
    export_obj(mesh, Path("out.obj"))
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def export_obj(mesh: Any, output_path: Path) -> None:
    """Export mesh to OBJ.

    Args:
        mesh: Mesh-like object.
        output_path: Output OBJ path.
    """
    # TODO: Implement OBJ export.
    output_path.write_text("", encoding="utf-8")
