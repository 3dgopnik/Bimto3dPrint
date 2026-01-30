"""IFC schema detection utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Literal


def detect_ifc_schema(ifc_path: Path) -> Literal["IFC2X3", "IFC4", "IFC4X3"]:
    """Detect IFC schema from the FILE_SCHEMA header.

    Args:
        ifc_path: Path to the IFC file.

    Returns:
        IFC schema identifier.

    Raises:
        ValueError: If the schema is missing or unsupported.
    """
    ifc_path = Path(ifc_path)
    with ifc_path.open("r", encoding="utf-8", errors="ignore") as file:
        for _ in range(50):
            line = file.readline()
            if not line:
                break
            if "FILE_SCHEMA" not in line.upper():
                continue

            upper_line = line.upper()
            if "IFC2X3" in upper_line:
                return "IFC2X3"
            if "IFC4X3" in upper_line:
                return "IFC4X3"
            if "IFC4" in upper_line:
                return "IFC4"

    raise ValueError("Unsupported or unknown IFC schema")
