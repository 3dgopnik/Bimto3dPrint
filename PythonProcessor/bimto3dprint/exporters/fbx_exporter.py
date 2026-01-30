"""FBX export utilities.

Example:
    export_fbx(mesh, Path("out.fbx"))
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def export_fbx(mesh: Any, output_path: Path) -> None:
    """Export mesh to FBX.

    Args:
        mesh: Mesh-like object.
        output_path: Output FBX path.
    """
    # TODO: Implement FBX export.
    output_path.write_text("", encoding="utf-8")
