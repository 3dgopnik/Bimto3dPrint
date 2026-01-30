"""CLI entry point for the IFC processing pipeline."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import click
import trimesh
from loguru import logger

from bimto3dprint.config import load_config
from bimto3dprint.exporters.fbx_exporter import FBXExporter
from bimto3dprint.exporters.obj_exporter import OBJExporter
from bimto3dprint.exporters.stl_exporter import STLExporter
from bimto3dprint.processors.mesh_optimizer import MeshOptimizer
from bimto3dprint.processors.shell_extractor import ShellExtractor
from bimto3dprint.utils.logger import get_logger
from bimto3dprint.utils.units import normalize_to_millimeters

PRESETS_DIR = Path("Config") / "Presets"


def _load_preset(preset: str) -> dict[str, Any]:
    preset_path = Path(preset)
    if preset_path.exists():
        logger.info("Loading preset from path: {}", preset_path)
        return load_config(preset_path)

    preset_path = PRESETS_DIR / f"{preset}.json"
    if not preset_path.exists():
        raise FileNotFoundError(f"Preset not found: {preset}")

    logger.info("Loading preset: {}", preset_path)
    return load_config(preset_path)


def _select_exporter(fmt: str):
    fmt = fmt.lower()
    if fmt == "stl":
        return STLExporter()
    if fmt == "obj":
        return OBJExporter()
    if fmt == "fbx":
        return FBXExporter()
    raise ValueError(f"Unsupported export format: {fmt}")


@click.group()
def cli() -> None:
    """Bimto3dPrint CLI."""
    get_logger()


@cli.command("process")
@click.argument("ifc_file", type=click.Path(path_type=Path, exists=True))
@click.option("--preset", default="shell_only", show_default=True, help="Preset name or path")
@click.option("--output", "output_path", type=click.Path(path_type=Path), required=True)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["fbx", "obj", "stl"], case_sensitive=False),
    default="stl",
    show_default=True,
)
@click.option("--scale", type=float, default=1.0, show_default=True)
@click.option("--simplify", type=str, default=None)
@click.option("--use-tudelft-extractor", is_flag=True, help="Use TU Delft envelope extractor")
@click.option(
    "--extractor-path",
    type=click.Path(path_type=Path),
    help="Path to TU Delft extractor exe or directory with multiple schema builds.",
)
@click.option("--lod", type=float, default=2.2, show_default=True)
@click.option("--voxel", "voxel_size", type=float, default=1.0, show_default=True)
@click.option("--threads", type=int, default=8, show_default=True)
@click.option("--no-thicken", is_flag=True, help="Skip wall thickening step")
@click.option("--min-wall-mm", type=float, default=2.0, show_default=True)
def process_command(
    ifc_file: Path,
    preset: str,
    output_path: Path,
    output_format: str,
    scale: float,
    simplify: str | None,
    use_tudelft_extractor: bool,
    extractor_path: Path | None,
    lod: float,
    voxel_size: float,
    threads: int,
    no_thicken: bool,
    min_wall_mm: float,
) -> None:
    """Process an IFC file and export a printable mesh."""
    logger.info("Starting IFC processing for {}", ifc_file)

    config = _load_preset(preset)
    if use_tudelft_extractor:
        if extractor_path is None:
            raise click.UsageError("--extractor-path is required with --use-tudelft-extractor")

        config["tudelft_extractor"] = {
            "extractor_path": str(extractor_path),
            "lod": lod,
            "voxel_size": voxel_size,
            "threads": threads,
        }
        logger.info("Configured TU Delft extractor: {}", extractor_path)

    extractor = ShellExtractor()
    mesh = extractor.extract_from_ifc(ifc_file, config)
    mesh, unit_scale_factor = normalize_to_millimeters(mesh)
    mesh_units = "meters" if unit_scale_factor == 1000.0 else "millimeters"

    if simplify:
        logger.info("Applying simplification level: {}", simplify)
        mesh = extractor.simplify_shell(mesh, simplify)

    if scale <= 0:
        raise click.UsageError("--scale must be positive")
    if scale != 1.0:
        logger.info("Scaling mesh by factor {:.3f}", scale)
        mesh.apply_scale(scale)

    if min_wall_mm <= 0:
        raise click.UsageError("--min-wall-mm must be positive")

    optimizer = MeshOptimizer()
    mesh = optimizer.ensure_watertight(mesh)
    if no_thicken:
        logger.info("Wall thickening skipped")
    else:
        logger.info("Wall thickening applied: {:.2f} mm", min_wall_mm)
        mesh = optimizer.thicken_walls(mesh, min_thickness_mm=min_wall_mm)
    mesh = optimizer.smooth_surface(mesh)
    report = optimizer.validate_for_printing(mesh)

    exporter = _select_exporter(output_format)
    exporter.export(
        mesh,
        output_path,
        metadata={
            "report": report,
            "mesh_units": mesh_units,
            "unit_scale_factor": unit_scale_factor,
            "user_scale_factor": scale,
        },
    )

    logger.info("Validation report: {}", report)
    logger.info("Processing completed")


@cli.command("validate")
@click.argument("mesh_file", type=click.Path(path_type=Path, exists=True))
def validate_command(mesh_file: Path) -> None:
    """Validate a mesh file for 3D printing."""
    logger.info("Loading mesh for validation: {}", mesh_file)
    mesh = trimesh.load(mesh_file, force="mesh")
    if not isinstance(mesh, trimesh.Trimesh):
        raise click.UsageError("Provided file could not be loaded as a mesh")

    optimizer = MeshOptimizer()
    report = optimizer.validate_for_printing(mesh)
    logger.info("Validation report: {}", report)


@cli.command("list-presets")
def list_presets_command() -> None:
    """List available preset names."""
    presets = sorted(PRESETS_DIR.glob("*.json"))
    if not presets:
        logger.warning("No presets found in {}", PRESETS_DIR)
        return

    for preset_path in presets:
        click.echo(preset_path.stem)


if __name__ == "__main__":
    cli()
