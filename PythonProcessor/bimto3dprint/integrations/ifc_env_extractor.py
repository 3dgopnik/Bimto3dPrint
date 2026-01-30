"""Integration for TU Delft IFC Building Envelope Extractor."""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any

from loguru import logger


@dataclass
class IfcEnvExtractorRunner:
    """Run the TU Delft IFC envelope extractor executable."""

    extractor_path: Path

    def __post_init__(self) -> None:
        self.extractor_path = Path(self.extractor_path)
        if not self.extractor_path.exists():
            raise FileNotFoundError(f"Extractor executable not found: {self.extractor_path}")

    def build_config(
        self,
        ifc_path: Path,
        output_dir: Path,
        lods: list[float] | None = None,
        voxel_size: float = 1.0,
        threads: int = 8,
        generate_exterior: bool = True,
        generate_interior: bool = False,
        output_obj: bool = True,
        output_step: bool = False,
    ) -> dict[str, Any]:
        """Build configuration dictionary for the extractor.

        Args:
            ifc_path: Path to the IFC file.
            output_dir: Output directory for extractor artifacts.
            lods: List of target LoD values.
            voxel_size: Voxel size for envelope generation.
            threads: Number of threads.
            generate_exterior: Whether to output exterior JSON geometry.
            generate_interior: Whether to output interior JSON geometry.
            output_obj: Whether to output OBJ mesh.
            output_step: Whether to output STEP file.

        Returns:
            Configuration dictionary aligned with TU Delft extractor schema.
        """
        ifc_path = Path(ifc_path)
        output_dir = Path(output_dir)
        lods = lods or [2.2]

        config: dict[str, Any] = {
            "Filepaths": {
                "Input": [str(ifc_path)],
                "Output": str(output_dir / "envelope.city.json"),
                "Report": str(output_dir / "envelope_report.json"),
            },
            "LoD output": lods,
            "Voxel": {"Size": float(voxel_size)},
            "IFC": {},
            "JSON": {
                "Generate exterior": int(generate_exterior),
                "Generate interior": int(generate_interior),
            },
            "Output format": {
                "OBJ file": int(output_obj),
                "STEP file": int(output_step),
            },
            "Tolerances": {
                "Spatial": 0.01,
                "Angular": 1.0,
                "Area": 0.01,
            },
            "Generate report": 1,
            "Threads": int(threads),
        }
        logger.info("Built TU Delft extractor config for {}", ifc_path)
        return config

    def write_config(self, config: dict[str, Any], config_path: Path) -> None:
        """Write configuration dictionary to disk as JSON.

        Args:
            config: Configuration dictionary.
            config_path: Path to write JSON file.
        """
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w", encoding="utf-8") as file:
            json.dump(config, file, indent=2, ensure_ascii=False)
        logger.info("Saved extractor config: {}", config_path)

    def run(self, config_path: Path, timeout_sec: int = 3600) -> CompletedProcess[str]:
        """Run the extractor executable with a configuration file.

        Args:
            config_path: Path to the JSON configuration.
            timeout_sec: Timeout in seconds.

        Returns:
            CompletedProcess instance.

        Raises:
            RuntimeError: If extractor returns a non-zero exit code.
            TimeoutError: If the process times out.
        """
        config_path = Path(config_path)
        logger.info("Running extractor: {} {}", self.extractor_path, config_path)
        try:
            completed = subprocess.run(
                [str(self.extractor_path), str(config_path)],
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            logger.error("Extractor timed out after {}s", timeout_sec)
            raise TimeoutError("Extractor execution timed out") from exc

        if completed.stdout:
            logger.info("Extractor stdout:\n{}", completed.stdout)
        if completed.stderr:
            logger.warning("Extractor stderr:\n{}", completed.stderr)

        if completed.returncode != 0:
            raise RuntimeError(
                f"Extractor failed with code {completed.returncode}: {completed.stderr.strip()}"
            )

        logger.info("Extractor finished successfully")
        return completed

    def find_output_obj(self, output_dir: Path) -> Path:
        """Find the first OBJ file produced by the extractor.

        Args:
            output_dir: Directory where outputs are expected.

        Returns:
            Path to the OBJ file.

        Raises:
            FileNotFoundError: If no OBJ files were found.
        """
        output_dir = Path(output_dir)
        for obj_path in output_dir.rglob("*.obj"):
            logger.info("Found OBJ output: {}", obj_path)
            return obj_path

        raise FileNotFoundError(
            "OBJ output not found: check Output format, output path, and permissions."
        )
