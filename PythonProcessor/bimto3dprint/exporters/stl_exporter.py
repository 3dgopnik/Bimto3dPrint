"""STL export utilities.

Example:
    export_stl(mesh, Path("out.stl"))
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def export_stl(mesh: Any, output_path: Path) -> None:
    """Export mesh to STL.

    Args:
        mesh: Mesh-like object.
        output_path: Output STL path.
    """
    # TODO: Implement STL export.
    output_path.write_text("", encoding="utf-8")
