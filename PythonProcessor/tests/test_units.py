from __future__ import annotations

import sys
from pathlib import Path

import trimesh

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from bimto3dprint.utils.units import detect_mesh_units, normalize_to_millimeters  # noqa: E402


def test_detect_units_millimeters() -> None:
    mesh = trimesh.creation.box(extents=[30000, 20000, 10000])
    assert detect_mesh_units(mesh) == "millimeters"
    _, scale_factor = normalize_to_millimeters(mesh)
    assert scale_factor == 1.0


def test_detect_units_meters() -> None:
    mesh = trimesh.creation.box(extents=[30, 20, 10])
    assert detect_mesh_units(mesh) == "meters"
    _, scale_factor = normalize_to_millimeters(mesh)
    assert scale_factor == 1000.0
