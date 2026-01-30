"""CLI entry point for the IFC processing pipeline.

Example:
    python -m bimto3dprint.main --ifc-path data/model.ifc --config config.json
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import click

from bimto3dprint.config import load_config
from bimto3dprint.processors.ifc_loader import load_ifc
from bimto3dprint.processors.shell_extractor import extract_shell
from bimto3dprint.processors.mesh_optimizer import optimize_mesh
from bimto3dprint.exporters.stl_exporter import export_stl
from bimto3dprint.utils.logger import get_logger


@click.command()
@click.option("--ifc-path", required=True, type=click.Path(path_type=Path))
@click.option("--config", "config_path", required=True, type=click.Path(path_type=Path))
@click.option("--output", "output_path", required=True, type=click.Path(path_type=Path))
def cli(ifc_path: Path, config_path: Path, output_path: Path) -> None:
    """Run the IFC processing pipeline."""
    logger = get_logger()
    logger.info("Loading configuration")
    config = load_config(config_path)

    logger.info("Loading IFC")
    model = load_ifc(ifc_path)

    logger.info("Extracting shell")
    mesh = extract_shell(model, config)

    logger.info("Optimizing mesh")
    optimized = optimize_mesh(mesh, config)

    logger.info("Exporting STL")
    export_stl(optimized, output_path)


if __name__ == "__main__":
    cli()
