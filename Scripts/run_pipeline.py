"""Run the IFC processing pipeline.

Example:
    python Scripts/run_pipeline.py --ifc data/model.ifc --config config.json --output out/model.stl
"""
from __future__ import annotations

import argparse
from pathlib import Path

from bimto3dprint.main import cli


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Run Bimto3dPrint pipeline")
    parser.add_argument("--ifc", dest="ifc_path", required=True, type=Path)
    parser.add_argument("--config", dest="config_path", required=True, type=Path)
    parser.add_argument("--output", dest="output_path", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    """Entry point wrapper."""
    args = parse_args()
    cli.main(
        args=[
            "--ifc-path",
            str(args.ifc_path),
            "--config",
            str(args.config_path),
            "--output",
            str(args.output_path),
        ],
        standalone_mode=False,
    )


if __name__ == "__main__":
    main()
